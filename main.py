from flask import Flask, request
from instagrapi import Client
import time
import os
from threading import Thread, Event

app = Flask(__name__)
clients = {}
stop_flags = {}
active_users = set()

@app.route('/', methods=["GET", "POST"])
def instagram_bot():
    if request.method == "POST":
        if 'stop' in request.form:
            username = request.form.get('username')
            if username in stop_flags:
                stop_flags[username].set()
                return f"<h3>🛑 Messaging stopped for <b>{username}</b></h3>"
            else:
                return f"<h3>❌ No active messaging for <b>{username}</b></h3>"

        # Start messaging
        username = request.form.get('username')
        password = request.form.get('password')
        target_username = request.form.get('targetUsername')
        group_thread_id = request.form.get('groupThreadId')
        time_interval = int(request.form.get('timeInterval', 5))
        victim_name = request.form.get('victimName')
        txt_file = request.files['txtFile']

        file_path = os.path.join('/tmp', f"{username}_messages.txt")
        txt_file.save(file_path)

        with open(file_path, 'r') as f:
            messages = f.read().splitlines()

        stop_flags[username] = Event()

        def send_loop():
            try:
                cl = Client()
                cl.login(username, password)
                clients[username] = cl
                active_users.add(username)

                while not stop_flags[username].is_set():
                    for msg in messages:
                        if stop_flags[username].is_set():
                            break
                        try:
                            full_msg = f"{victim_name}: {msg}" if victim_name else msg
                            if group_thread_id:
                                cl.direct_send(full_msg, thread_ids=[group_thread_id])
                            elif target_username:
                                user_id = cl.user_id_from_username(target_username)
                                cl.direct_send(full_msg, [user_id])
                            time.sleep(time_interval)
                        except Exception as e:
                            print(f"Send error: {e}")
            except Exception as e:
                print(f"Login error: {e}")

        Thread(target=send_loop).start()
        return f"<h3>✅ Messaging started for <b>{username}</b></h3>"

    return "<h1>📱 Instagram Bot Tool Panel</h1><p>Use POST to start messaging.</p>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
