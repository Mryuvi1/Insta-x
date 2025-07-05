from flask import Flask, request, session
from instagrapi import Client
import os
import time
import uuid
from threading import Thread

app = Flask(__name__)
app.secret_key = 'yuvi-king-secret'  # Required for session

clients = {}
stop_flags = {}

HTML_TEMPLATE_HEAD = """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Haters Fucker Tool - KING MAKER YUVI</title>
  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css' rel='stylesheet'>
  <style>
    body {
      background-image: url('https://i.postimg.cc/CLDK8xcp/02f522c98d59a21a4b07ccd96cee09db.jpg');
      background-size: cover;
      background-position: center;
      height: 100vh;
      font-family: monospace;
      color: #00ff99;
    }
    .container {
      background: rgba(0,0,0,0.4);
      padding: 30px;
      margin-top: 60px;
      border-radius: 20px;
      box-shadow: 0 0 25px #00ff99;
      border: 1px solid #00ff99;
    }
    .btn-hacker {
      background: transparent;
      border: 2px solid #00ff99;
      color: #00ff99;
      font-weight: bold;
      border-radius: 10px;
      padding: 12px;
      transition: 0.3s ease;
      box-shadow: 0 0 10px #00ff99, 0 0 20px #00ff99;
    }
    .btn-hacker:hover {
      background: #00ff99;
      color: black;
      box-shadow: 0 0 20px #00ff99, 0 0 40px #00ff99;
    }
  </style>
</head>
<body>
<div class='container'>
<h2 class='text-center'><b>HATERS FUCKER TOOL BY KING MAKER YUVI</b></h2>
"""

HTML_TEMPLATE_FOOT = """
<p class='text-center mt-4' style='font-size: 14px; color: #00ff99; text-shadow: 0 0 5px #00ff99;'>
Created & Powered by <b>KING MAKER YUVI</b>
</p>
</div>
</body>
</html>
"""

def send_messages(thread_key, cl, username, target_username, group_thread_id, messages, time_interval):
    stop_flags[thread_key] = False
    try:
        if group_thread_id:
            for i, msg in enumerate(messages, 1):
                if stop_flags.get(thread_key):
                    break
                cl.direct_send(msg, thread_ids=[group_thread_id])
                time.sleep(time_interval)

        elif target_username:
            user_id = cl.user_id_from_username(target_username)
            for i, msg in enumerate(messages, 1):
                if stop_flags.get(thread_key):
                    break
                cl.direct_send(msg, [user_id])
                time.sleep(time_interval)
    except Exception as e:
        print(f"[ERROR] {username} - {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        target_username = request.form.get('targetUsername')
        group_thread_id = request.form.get('groupThreadId')
        time_interval = int(request.form['timeInterval'])
        txt_file = request.files['txtFile']

        file_path = os.path.join('/tmp', f'{username}_msgs.txt')
        txt_file.save(file_path)

        with open(file_path, 'r') as f:
            messages = f.read().splitlines()

        try:
            cl = Client()
            session_file = f"{username}_session.json"

            if os.path.exists(session_file):
                cl.load_settings(session_file)
                cl.login(username, password)
            else:
                cl.login(username, password)
                cl.dump_settings(session_file)

            thread_key = str(uuid.uuid4())[:8]
            thread = Thread(target=send_messages, args=(thread_key, cl, username, target_username, group_thread_id, messages, time_interval))
            thread.start()

            clients[thread_key] = {
                "username": username,
                "client": cl,
                "thread": thread
            }

            session['username'] = username

            return f"<h3>✅ Message attack started for <b>{username}</b></h3><h5>🗝️ Your STOP Key: <code>{thread_key}</code></h5><br><a href='/'>Back</a>"

        except Exception as e:
            return f"<h3>❌ Error: {e}</h3><br><a href='/'>Back</a>"

    # GET request
    active_keys_html = ""
    session_username = session.get('username')

    if session_username:
        user_keys = [k for k, v in clients.items() if v['username'] == session_username]
        if user_keys:
            active_keys_html += "<div class='mb-3'><label>Your Active Thread Key(s):</label><textarea class='form-control' rows='3' readonly>"
            for key in user_keys:
                active_keys_html += f"{key}\n"
            active_keys_html += "</textarea></div>"

    html = HTML_TEMPLATE_HEAD + """
    <form action='/' method='post' enctype='multipart/form-data'>
      <div class='mb-3'>
        <label>Instagram Username:</label>
        <input type='text' class='form-control' name='username' required>
      </div>
      <div class='mb-3'>
        <label>Instagram Password:</label>
        <input type='password' class='form-control' name='password' required>
      </div>
      <div class='mb-3'>
        <label>Target Username:</label>
        <input type='text' class='form-control' name='targetUsername'>
      </div>
      <div class='mb-3'>
        <label>OR Group Thread ID:</label>
        <input type='text' class='form-control' name='groupThreadId'>
      </div>
      <div class='mb-3'>
        <label>Message File (.txt):</label>
        <input type='file' class='form-control' name='txtFile' accept='.txt' required>
      </div>
      <div class='mb-3'>
        <label>Time Interval (seconds):</label>
        <input type='number' class='form-control' name='timeInterval' value='2' required>
      </div>
      <button type='submit' class='btn-hacker w-100'>Launch Message Attack</button>
    </form>

    <form action='/stop' method='post' class='mt-4'>
      <div class='mb-3'>
        <label>Enter STOP Key:</label>
        <input type='text' class='form-control' name='thread_key' required>
      </div>
      <button type='submit' class='btn-hacker w-100'>STOP Messages</button>
    </form>
    """ + active_keys_html + HTML_TEMPLATE_FOOT

    return html

@app.route('/stop', methods=['POST'])
def stop_messages():
    thread_key = request.form['thread_key']
    if thread_key in stop_flags:
        stop_flags[thread_key] = True
        return f"<h3>🛑 Message sending stopped for key: <code>{thread_key}</code></h3><br><a href='/'>Back</a>"
    return f"<h3>❌ Invalid key: <code>{thread_key}</code></h3><br><a href='/'>Back</a>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
