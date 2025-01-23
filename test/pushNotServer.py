from flask import Flask, request, jsonify
from pywebpush import webpush, WebPushException
from flask_cors import CORS
import time
import threading

app = Flask(__name__)

CORS(app)

VAPID_PUBLIC_KEY = "BCcugnAXkyYu6Ci9G0FbmeYD3EzvUoNTCxqpFo1TCHSB9-iErdH2v3FYYWHNngZKXVRVFP-D00m5li1g_DAmCe4"
VAPID_PRIVATE_KEY = "DHn5rO6TzClhtOisl1LTOTiiZ2uSkB_GYFVKOGRjH0w"
VAPID_CLAIMS = {
    "sub": "mailto:example@example.com"
}


# Die Subscription infos sind: 
# {
#     'endpoint': 'https://fcm.googleapis.com/fcm/send/e8KaETkV-GA:APA91bHzu4z6BoQIiaenAVTSL-NNAyU-9OclB5o81pPx54MmhDmHKgk-F0Cr37evPTgg-xYJomduoH9npii8_WBZHI7KssbAmJWz8Se14ZWl5DQ4VsYTeOa6_FnFyN6uQjg1XtI7TAdf', 
#     'expirationTime': None, 
#     'keys': {
#         'p256dh': 'BI1RCOjvqfRQzbRJNzMPcX5oALXg4kN_bqxceIydAqgzi92KHA79JcYBzhJHcIM3srInmFTM7D_LzlnaI-vWC9Q', 
#         'auth': 'oDcDHYsaBebQIP2RXAOgGQ'
#     }
# }


subscriptions = []

@app.route('/subscribe', methods=['POST'])
def subscribe():
    subscription_info = request.get_json()
    print(f"Die Subscription infos sind: {subscription_info}")
    print(f"Der Type der Subscription ist: {type(subscription_info)}")
    subscriptions.append(subscription_info)
    return jsonify({"message": "Subscription successful."}), 201

def send_push_notification():
    while True:
        time.sleep(60)  # Wait 1 minute
        
        for i in range(1,10,1):        # Die Banner werden einzeln angezeigt
            for subscription in subscriptions:
                try:
                    webpush(
                        subscription_info=subscription,
                        data="Eine Minute ist abgelaufen! Das ist ein längerer Text, den ich zum ausgebe um zu testen wie gross so eine maximale Ausgabe werden darf oder ich mehrere machen soll.",
                        vapid_private_key=VAPID_PRIVATE_KEY,
                        vapid_claims=VAPID_CLAIMS
                    )
                except WebPushException as ex:
                    print(f"Push notification failed: {ex}")

if __name__ == '__main__':
    threading.Thread(target=send_push_notification, daemon=True).start()
    app.run(debug=True, port=5000)
