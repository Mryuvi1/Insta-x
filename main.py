from flask import Flask, request, render_template_string
from instagrapi import Client
import os
import time
from threading import Thread, Event

app = Flask(__name__)
stop_event = Event()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>🩷 YUVII INSTAGRAM BOT 🐼</title>
  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css' rel='stylesheet'>
  <style>
    body {
      background-image: url('https://i.postimg.cc/Wbc2fG9y/b7ae332981e970d9221a8d4e193e4c1e.jpg');
      background-size: cover;
      background-repeat: no-repeat;
      background-position: center;
      height: 100vh;
      margin: 0;
      color: white;
    }
    .container {
      max-width: 500px;
      background-color: rgba(0, 0, 0, 0.7);
      border-radius: 15px;
      padding: 20px;
      margin-top: 50px;
      box-shadow: 0 0 20px #00ffcc;
    }
    .btn-glow {
      background-color: #00ffff;
      border: none;
      color: black;
      font-weight: bold;
      box-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff;
      transition: 0.3s ease-in-out;
    }
    .btn-glow:hover {
      box-shadow: 0 0 15px #ff00ff, 0 0 25px #ff00ff, 0 0 35px #ff00ff;
      background-color: #ff00ff;
      color: white;
    }
    .owner-tag {
      position: fixed;
      top: 10px;
      left: 10px;
      color: #ffffff;
      font-weight: bold;
      z-index: 999;
      text-shadow: 1px 1px 5px black;
    }
    .logo {
      display: block;
      margin: 0 auto 20px auto;
      width: 100px;
      border-radius: 50%;
      border: 3px solid white;
      box-shadow: 0 0 15px #ff00ff;
    }
  </style>
</head>
<body>
  <div class='owner-tag'>🔥 Tool By LEGEND YUVII INSIDE</div>
  <div class='container'>
    <img src='https://i.postimg.cc/Kcr5V75s/a58f941bc7aaad40797dfe63fcaaa34e.jpg' alt='Logo' class='logo'>
    <h2 class='text-center mb-4'>Instagram Messaging Bot</h2>
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
        <label>Target Username (for DM):</label>
        <input type='text' class='form-control' name='targetUsername'>
      </div>
      <div class='mb-3'>
        <label>Group Chat Name (optional):</label>
        <input type='text' class='form-control' name='groupName'>
      </div>
      <div class='mb-3'>
        <label>Victim Name (prefix for each message):</label>
        <input type='text' class='form-control' name='victimName' required>
      </div>
      <div class='mb-3'>
        <label>Message File (.txt):</label>
        <input type='file' class='form-control' name='txtFile' accept='.txt' required>
      </div>
      <div class='mb-3'>
        <label>Time Interval (seconds):</label>
        <input type='number' class='form-control' name='timeInterval' value='2' required>
      </div>
      <button type='submit' class='btn btn-glow w-100'>🔥 Start Sending</button>
    </form>
    <form action='/stop' method='post' class='mt-3'>
      <button type='submit' class='btn btn-glow w-100'>🛑 Stop Sending</button>
    </form>
    <p class='text-center mt-4' style='font-size: 14px; color: #ccc;'>
      Tool Developed By <b>MR YUVI</b>
    </p>
  </div>
</body>
</html>
"""

def send_messages(username, password, target_username, group_name, victim_name, messages, interval):
    try:
        cl = Client()
        cl.login(username, password)
        print("✅ Logged in successfully")

        user_id = None
        thread_id = None

        if target_username:
            user_id = cl.user_id_from_username(target_username)
            print(f"✅ Fetched user_id: {user_id}")

        if group_name:
            threads = cl.direct_threads()
            for thread in threads:
                print(f"🧵 Found thread: {thread.title}")
                if thread.title and group_name.lower() in thread.title.lower():
                    thread_id = thread.id
                    print(f"✅ Found matching group thread: {thread_id}")
                    break

        for msg in messages:
            if stop_event.is_set():
                break
            full_msg = f"[🔥{victim_name}🔥] {msg}"

            if user_id:
                try:
                    resp_dm = cl.direct_send(full_msg, [user_id])
                    print("📨 DM Send Response:", resp_dm)
                except Exception as e:
                    print("❌ Error sending DM:", str(e))

            if thread_id:
                try:
                    resp_group = cl.direct_send(full_msg, thread_ids=[thread_id])
                    print("📨 Group Send Response:", resp_group)
                except Exception as e:
                    print("❌ Error sending group message:", str(e))

            time.sleep(interval)

    except Exception as e:
        print("❌ Main Error:", str(e))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        stop_event.clear()
        username = request.form.get('username')
        password = request.form.get('password')
        target_username = request.form.get('targetUsername')
        group_name = request.form.get('groupName')
        victim_name = request.form.get('victimName')
        interval = int(request.form.get('timeInterval'))
        txt_file = request.files['txtFile']

        file_path = os.path.join('/tmp', 'messages.txt')
        txt_file.save(file_path)

        with open(file_path, 'r') as f:
            messages = f.read().splitlines()

        thread = Thread(target=send_messages, args=(
            username, password, target_username, group_name, victim_name, messages, interval
        ))
        thread.start()

        return "<h3>✅ Sending started to DM & Group (if provided).<br><a href='/'>🔙 Go Back</a></h3>"

    return render_template_string(HTML_TEMPLATE)

@app.route('/stop', methods=['POST'])
def stop():
    stop_event.set()
    return "<h3>🛑 Message sending stopped!<br><a href='/'>🔙 Go Back</a></h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
