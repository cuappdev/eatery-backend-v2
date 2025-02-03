import * as functions from "firebase-functions/v1";
import * as admin from "firebase-admin";

admin.initializeApp();

const firestore = admin.firestore();
const messaging = admin.messaging();

const PROJECT_ID = "eatery-a4ad1";
const LOCATION = "us-central1";
const QUEUE_NAME = "eatery-notification-queue";
const SERVICE_ACCOUNT_EMAIL = "cloud-tasks-sa@eatery-a4ad1.iam.gserviceaccount.com";

exports.scheduleDailyNotifications = functions.pubsub
  .schedule("0 6 * * *") // Runs daily at 6 AM UTC
  .timeZone("UTC")
  .onRun(async () => {
    const { CloudTasksClient } = await import("@google-cloud/tasks");
    const client = new CloudTasksClient();
    
    const now = Math.floor(Date.now() / 1000); 
    const parent = client.queuePath(PROJECT_ID, LOCATION, QUEUE_NAME);

    console.log("Fetching all eatery events for today...");

    const eateriesSnapshot = await firestore.collection("eateries").get();

    for (const doc of eateriesSnapshot.docs) {
      const eatery = doc.data();
      const userTokens = eatery.user_tokens || [];

      eatery.events.forEach(async (event: any) => {
        const notifyTimeOpen = event.start - 30 * 60;
        const notifyTimeClose = event.end - 30 * 60;

        if (notifyTimeOpen > now) {
          await scheduleTask(client, parent, eatery.name, event.event_description, userTokens, notifyTimeOpen, "Opening Soon");
        }

        if (notifyTimeClose > now) {
          await scheduleTask(client, parent, eatery.name, event.event_description, userTokens, notifyTimeClose, "Closing Soon");
        }
      });
    }

    console.log("All notifications scheduled via Cloud Tasks.");
  });

async function scheduleTask(client: any, parent: string, eateryName: string, eventName: string, userTokens: string[], notifyTime: number, action: string) {
  const task = {
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
  console.log(`Scheduled task for ${eventName} (${action}) at ${new Date(notifyTime * 1000).toISOString()}`);
}

exports.sendNotification = functions.https.onRequest(async (req, res) => {
  try {
    const { eateryName, eventName, userTokens, action }: { eateryName: string; eventName: string; userTokens: string[]; action: string } = req.body;

    if (!userTokens || userTokens.length === 0) {
      console.log(`No user tokens found for ${eventName} at ${eateryName}.`);
      res.status(200).send("No notifications sent.");
      return;
    }

    const payload = {
      notification: {
        title: `${eventName} ${action}!`,
        body: `${eventName} at ${eateryName} is happening in 30 minutes!`,
      },
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
