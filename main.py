from flask import Flask, request, jsonify
from instagrapi import Client
import os
import time
from threading import Thread, Event

app = Flask(__name__)

# Store user sessions
user_sessions = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>🔥 HATERS FUCKER TOOL BY YUVI 🐼</title>
</head>
<body style="background:#000;color:#0f0;font-family:Courier New;text-align:center;padding:30px;">
  <h2>🔥 HATERS FUCKER TOOL BY YUVI 🐼</h2>
  <form action='/' method='post' enctype='multipart/form-data'>
    <input type='text' name='username' placeholder='Instagram Username' required><br><br>
    <input type='password' name='password' placeholder='Password' required><br><br>
    <input type='text' name='targetUsername' placeholder='Target Username'><br><br>
    <input type='text' name='groupThreadId' placeholder='OR Group Thread ID'><br><br>
    <input type='file' name='txtFile' accept='.txt' required><br><br>
    <input type='number' name='timeInterval' placeholder='Interval (sec)' value='2'><br><br>
    <button type='submit'>🔥 Start Messaging</button>
  </form>

  <br>
  <form action='/stop' method='post'>
    <input type='text' name='username' placeholder='Username to stop' required>
    <button type='submit'>🛑 Stop Messaging</button>
  </form>

  <br><br>
  <a href="/status" target="_blank" style="color:#0f0;">🔄 Live Status</a>
</body>
</html>
"""

def start_sending_messages(username, password, messages, user_id=None, thread_id=None, interval=2):
    stop_event = user_sessions[username]["stop_event"]
    count = 0
    cl = Client()
    cl.login(username, password)

    while not stop_event.is_set():
        msg = messages[count % len(messages)]
        try:
            if thread_id:
                cl.direct_send(msg, thread_ids=[thread_id])
            else:
                cl.direct_send(msg, [user_id])
            count += 1
            user_sessions[username]["message_count"] = count
            time.sleep(interval)
        except Exception as e:
            print(f"❌ Error: {e}")
            break

def launch_thread(username, password, messages, user_id, thread_id, interval):
    stop_event = Event()
    user_sessions[username] = {
        "stop_event": stop_event,
        "message_count": 0,
        "thread": None
    }
    thread = Thread(target=start_sending_messages, args=(username, password, messages, user_id, thread_id, interval))
    user_sessions[username]["thread"] = thread
    thread.start()

@app.route('/', methods=['GET', 'POST'])
def instagram_bot():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        target_username = request.form.get('targetUsername')
        group_thread_id = request.form.get('groupThreadId')
        time_interval = int(request.form.get('timeInterval'))
        txt_file = request.files['txtFile']

        file_path = os.path.join('/tmp', 'uploaded_messages.txt')
        txt_file.save(file_path)

        with open(file_path, 'r') as f:
            messages = f.read().splitlines()

        try:
            cl = Client()
            cl.login(username, password)

            if group_thread_id:
                launch_thread(username, password, messages, None, group_thread_id, time_interval)
                return f"<h3>✅ Group messaging started for {username}</h3>"

            elif target_username:
                user_id = cl.user_id_from_username(target_username)
                launch_thread(username, password, messages, user_id, None, time_interval)
                return f"<h3>✅ DM messaging started for {username}</h3>"

            else:
                return "<h3>❌ Please enter a username or group thread ID</h3>"

        except Exception as e:
            return f"<h3>❌ Error: {str(e)}</h3>"

    return HTML_TEMPLATE

@app.route('/stop', methods=['POST'])
def stop():
    username = request.form.get("username")
    if username in user_sessions:
        user_sessions[username]["stop_event"].set()
        return f"🛑 Sending stopped for {username}"
    return "❌ No session found"

@app.route('/status', methods=['GET'])
def status():
    data = {
        "users": list(user_sessions.keys()),
        "counts": {u: user_sessions[u]["message_count"] for u in user_sessions}
    }
    return jsonify(data)

# ✅ PORT FIX FOR RENDER
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
