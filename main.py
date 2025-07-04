from flask import Flask, request
from instagrapi import Client
import os
import time
from threading import Thread

app = Flask(__name__)
clients = {}
stop_flags = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
<meta name="author" content="KING MAKER YUVI">
<!-- Tool coded & owned by KING MAKER YUVI - Legend Inside -->
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css' rel='stylesheet'>
  <style>
  body {
    background-image: url('https://i.postimg.cc/CLDK8xcp/02f522c98d59a21a4b07ccd96cee09db.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh;
    margin: 0;
    font-family: 'Courier New', monospace;
    color: #00ff99;
  }

  .container {
    max-width: 500px;
    background: rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    border: 1px solid #00ff99;
    border-radius: 20px;
    padding: 30px;
    margin: 60px auto;
    box-shadow: 0 0 25px #00ff99;
  }

  .owner-tag {
    position: fixed;
    top: 10px;
    left: 10px;
    color: #00ff99;
    font-weight: bold;
    text-shadow: 0 0 10px #00ff99;
    z-index: 999;
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
<img src="https://i.postimg.cc/Kcr5V75s/a58f941bc7aaad40797dfe63fcaaa34e.jpg" width="120" style="display:block; margin:20px auto;">
  <div class='owner-tag'>🛠 Made by KING MAKER YUVI 👑</div>

  <div class='container'>
    <h2 class='text-center mb-4'>🔥 <b>HATERS FUCKER TOOL BY KING MAKER YUVI 👑</b></h2>
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
      <button type='submit' class='btn-hacker w-100'>🔥 Launch Message Attack</button>
    </form>

    <form action='/stop' method='post' class='mt-4'>
      <div class='mb-3'>
        <label>Enter Username to STOP:</label>
        <input type='text' class='form-control' name='username' required>
      </div>
      <button type='submit' class='btn-hacker w-100'>🛑 STOP Messages</button>
    </form>

    <p class='text-center mt-4' style='font-size: 14px; color: #00ff99; text-shadow: 0 0 5px #00ff99;'>
  🔥 Created & Powered by <b>KING MAKER YUVI 👑</b>
</p>
  </div>
</body>
</html>
"""

def send_messages(username, cl, target_username, group_thread_id, messages, time_interval):
    stop_flags[username] = False
    try:
        if group_thread_id:
            for i, msg in enumerate(messages, 1):
                if stop_flags.get(username): break
                cl.direct_send(msg, thread_ids=[group_thread_id])
                print(f"[{username}] Sent to Group: {i}/{len(messages)}")
                time.sleep(time_interval)

        elif target_username:
            user_id = cl.user_id_from_username(target_username)
            for i, msg in enumerate(messages, 1):
                if stop_flags.get(username): break
                cl.direct_send(msg, [user_id])
                print(f"[{username}] Sent to User: {i}/{len(messages)}")
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
    print("🔐 Loading saved session for:", username)
    cl.load_settings(session_file)
    cl.login(username, password)
else:
    try:
        cl.login(username, password)
        cl.dump_settings(session_file)
        print("✅ Session saved for future logins")
    except Exception as e:
        if "two_factor" in str(e).lower() and otp_code:
            cl.two_factor_login(otp_code)
            cl.dump_settings(session_file)
            print("✅ 2FA login successful, session saved")
        else:
            print("❌ Login failed:", e)
            return
    return HTML_TEMPLATE

@app.route('/stop', methods=['POST'])
def stop_messages():
    username = request.form['username']
    stop_flags[username] = True
    return f"<h3>🛑 Message sending stopped for <b>{username}</b></h3>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
