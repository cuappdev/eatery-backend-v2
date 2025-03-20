import * as functions from "firebase-functions";
import * as admin from "firebase-admin";

admin.initializeApp();

const firestore = admin.firestore();
const messaging = admin.messaging();

const PROJECT_ID = process.env.PROJECT_ID;
const LOCATION = process.env.LOCATION;
const QUEUE_NAME = process.env.QUEUE_NAME;
const SERVICE_ACCOUNT_EMAIL = process.env.SERVICE_ACCOUNT_EMAIL;

exports.scheduleDailyNotifications = functions.pubsub
  .schedule("0 6 * * *") // Runs daily at 6 AM UTC
  .timeZone("UTC")
  .onRun(async () => {
    const { CloudTasksClient } = await import("@google-cloud/tasks");
    const client = new CloudTasksClient();

    const now = Math.floor(Date.now() / 1000);
    const parent = `projects/${PROJECT_ID}/locations/${LOCATION}/queues/${QUEUE_NAME}`;

    console.log("Fetching all eatery events for today...");

    const eateriesSnapshot = await firestore.collection("eateries").get();

    const batchSize = 10; 
    let batchCounter = 0;
    let existingTasks: any[] = [];

    for (const doc of eateriesSnapshot.docs) {
      const eatery = doc.data();
      const userTokens = eatery.user_tokens || [];

      if (userTokens.length === 0) {
        console.log(`Skipping ${eatery.name}: No user tokens.`);
        continue;
      }

      if (batchCounter % batchSize === 0) {
        console.log(`Fetching existing tasks for batch ${batchCounter / batchSize + 1}...`);
        let [taskResponse] = await client.listTasks({ parent });
        existingTasks = taskResponse || [];
      }

      for (const event of eatery.events) {
        const notifyTimes = [
          { time: event.notify_time_open, action: "Opening Soon" },
          { time: event.notify_time_close, action: "Closing Soon" }
        ];

        for (const { time, action } of notifyTimes) {
          if (time <= now) continue;

          const isDuplicate = existingTasks.some(
            (task: any) => task.name && task.name.includes(`${eatery.name}-${event.event_description}-${action}`)
          );

          if (isDuplicate) {
            console.log(`Skipping duplicate task for ${event.event_description} (${action}) at ${eatery.name}`);
            continue;
          }

          await scheduleTask(client, parent, eatery.name, event.event_description, userTokens, time, action);
        }
      }

      batchCounter++;

      if (batchCounter % batchSize === 0) {
        console.log("⏳ Waiting 2 seconds before processing next batch...");
        await new Promise((resolve) => setTimeout(resolve, 2000));
      }
    }

    console.log("All notifications scheduled.");
  });

async function scheduleTask(client: any, parent: string, eateryName: string, eventName: string, userTokens: string[], notifyTime: number, action: string) {
  const sanitize = (str: string) => str.replace(/[^A-Za-z0-9 _-]/g, "").replace(/\s+/g, "-");
  const sanitizedEateryName = sanitize(eateryName);
  const sanitizedEventName = sanitize(eventName);
  const sanitizedAction = sanitize(action);

  const taskName = `${sanitizedEateryName}-${sanitizedEventName}-${sanitizedAction}-${notifyTime}`;

  const task = {
    name: `${parent}/tasks/${taskName}`,
    httpRequest: {
      httpMethod: "POST" as "POST",
      url: `https://${LOCATION}-${PROJECT_ID}.cloudfunctions.net/sendNotification`,
      headers: { "Content-Type": "application/json" },
      body: Buffer.from(
        JSON.stringify({
          eateryName,
          eventName,
          userTokens,
          action,
        })
      ).toString("base64"),
      oidcToken: {
        serviceAccountEmail: SERVICE_ACCOUNT_EMAIL,
      },
    },
    scheduleTime: { seconds: notifyTime },
  };

  await client.createTask({ parent, task });
  console.log(`Scheduled ${taskName} at ${new Date(notifyTime * 1000).toISOString()}`);
}

export const sendNotification = functions.https.onRequest(async (req, res) => {
  try {
    const { eateryName, eventName, userTokens, action }: { eateryName: string; eventName: string; userTokens: string[]; action: string } = req.body;

    if (!userTokens || userTokens.length === 0) {
      console.log(`No user tokens found for ${eventName} at ${eateryName}.`);
      res.status(200).send("No notifications sent.");
      return;
    }

    let title: string;
    let body: string;
    let generalEvent = eventName.toLowerCase() === "open" || eventName.toLowerCase() === "general"

    if (generalEvent) {
      if (action === "Opening Soon") {
        title = `${eateryName} is opening soon!`;
        body = `${eateryName} opens in 30 minutes! Don't miss out.`;
      } else {
        title = `${eateryName} is closing soon!`;
        body = `${eateryName} closes in 30 minutes! Last chance to grab food.`;
      }
    } 
    else {
      if (action === "Opening Soon") {
        title = `${eateryName} ${eventName} is starting soon!`;
        body = `${eventName} at ${eateryName} starts in 30 minutes! Don't miss out.`;
      } else {
        title = `${eateryName} ${eventName} is ending soon!`;
        body = `${eventName} at ${eateryName} ends in 30 minutes! Last chance to grab food.`;
      }
    }

    const payload = {
      notification: { title, body },
    };

    const sendPromises = userTokens.map((token) =>
      messaging.send({
        token,
        notification: payload.notification,
      })
    );

    await Promise.all(sendPromises);
    console.log(`Notification sent for ${eventName} (${action}) at ${eateryName}`);

    res.status(200).send("Notification sent.");
    return;
  } catch (error) {
    console.error(`Error sending notification:`, error);
    res.status(500).send("Failed to send notification.");
    return;
  }
});
