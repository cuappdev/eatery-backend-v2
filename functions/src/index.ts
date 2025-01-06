import * as functions from "firebase-functions/v1";
import * as admin from "firebase-admin";

admin.initializeApp();

const firestore = admin.firestore();
const messaging = admin.messaging();

// Schedules daily notifications
exports.scheduleDailyNotifications = functions.pubsub
  .schedule("0 0 * * *") // Runs daily at midnight
  .timeZone("America/New_York")
  .onRun(async (context) => {
    const eateriesSnapshot = await firestore.collection("eateries").get();
    const now = new Date();

    eateriesSnapshot.forEach((doc) => {
      const eatery = doc.data();
      eatery.events.forEach((event: { event_description: string; start: number; end: number }) => {
        const notifyStartTime = new Date(event.start * 1000 - 30 * 60 * 1000); // 30 mins before start
        const notifyEndTime = new Date(event.end * 1000 - 30 * 60 * 1000); // 30 mins before end

        if (notifyStartTime > now) {
          scheduleNotification(eatery.name, event.event_description, notifyStartTime, "opening", eatery.user_tokens);
        }

        if (notifyEndTime > now) {
          scheduleNotification(eatery.name, event.event_description, notifyEndTime, "closing", eatery.user_tokens);
        }
      });
    });

    console.log("Scheduled all notifications for the day.");
  });

function scheduleNotification(
  eateryName: string,
  eventName: string,
  notifyTime: Date,
  action: string,
  userTokens: string[]
) {
  console.log(`Scheduling notification for ${eventName} (${action}) at ${notifyTime}`);
  
  const payload = {
    notification: {
      title: `${eventName} ${action} Soon`,
      body: `${eventName} at ${eateryName} is happening in 30 minutes!`,
    },
  };

  userTokens.forEach((token) => {
    messaging
      .send({
        token: token,
        notification: payload.notification,
      })
      .then((response) => {
        console.log(`Notification sent to ${token}: ${response}`);
      })
      .catch((error) => {
        console.error(`Error sending notification to ${token}:`, error);
      });
  });
}
