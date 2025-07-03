from flask import Flask, request
from instagrapi import Client
from threading import Thread, Event
import time
import os

app = Flask(__name__)
clients = {}
stop_events = {}
active_users = set()
threads = {}

HTML_TEMPLATE = "<h3>Welcome to KING MAKER YUVI Panel</h3>"

@app.route('/start', methods=['POST'])
def start():
    global username, password, group_thread_id, target_username, interval, messages

    username = request.form.get('username')
    password = request.form.get('password')
    group_thread_id = request.form.get('group_thread_id')
    target_username = request.form.get('target_username')
    interval = float(request.form.get('interval', 2))
    messages = request.form.get('messages', '').split('\n')

    stop_events[username] = Event()

    def send_loop():
        try:
            cl = Client()
            cl.login(username, password)

            if username not in active_users:
                active_users.add(username)

            clients[username] = cl

            while not stop_events[username].is_set():
                for msg in messages:
                    if stop_events[username].is_set():
                        break
                    try:
                        if group_thread_id:
                            cl.direct_send(msg, thread_ids=[group_thread_id])
                        elif target_username:
                            user_id = cl.user_id_from_username(target_username)
                            cl.direct_send(msg, user_ids=[user_id])
                        time.sleep(interval)
                    except Exception as e:
                        print(f"Error sending message: {e}")

        except Exception as e:
            print(f"Error in send_loop: {e}")

    # Start the sending thread
    t = Thread(target=send_loop)
    t.start()
    threads[username] = t

    return f"<h3>✅ Message sending started for <b>{username}</b>.</h3><br><a href='/'>Back</a>"

@app.route('/stop', methods=['POST'])
def stop():
    username = request.form.get('username')
    if username in stop_events:
        stop_events[username].set()
        active_users.discard(username)
        return f"<h3>🛑 Stopped message loop for <b>{username}</b></h3><br><a href='/'>Back</a>"
    else:
        return "<h3>❌ No active session found for that username</h3><br><a href='/'>Back</a>"

@app.route('/active', methods=['GET'])
def show_active_users():
    if not active_users:
        return "<h3>🟢 No active users currently</h3>"
    return "<h3>🟢 Active Users:</h3><ul>" + "".join([f"<li>{user}</li>" for user in active_users]) + "</ul>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
