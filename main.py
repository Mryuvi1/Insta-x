import logging
logging.basicConfig(level=logging.INFO)

from flask import Flask, request
from instagrapi import Client
import os
import time
from threading import Thread, Event
app = Flask(__name__)
app.debug = True

HTML_TEMPLATE = """

<!DOCTYPE html><html lang='en'>
<head>
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
  }.container { max-width: 500px; background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border: 1px solid #00ff99; border-radius: 20px; padding: 30px; margin: 60px auto; box-shadow: 0 0 25px #00ff99; }

.owner-tag { position: fixed; top: 10px; left: 10px; color: #00ff99; font-weight: bold; text-shadow: 0 0 10px #00ff99; z-index: 999; }

.btn-hacker { background: transparent; border: 2px solid #00ff99; color: #00ff99; font-weight: bold; border-radius: 10px; padding: 12px; transition: 0.3s ease; box-shadow: 0 0 10px #00ff99, 0 0 20px #00ff99; }

.btn-hacker:hover { background: #00ff99; color: black; box-shadow: 0 0 20px #00ff99, 0 0 40px #00ff99; }

.glow-text { text-align: center; font-size: 22px; color: #00ff99; text-shadow: 0 0 10px #ff4d4d, 0 0 20px #ff4d4d, 0 0 40px #ff4d4d; animation: flicker 1.5s infinite alternate; }

@keyframes flicker { 0% { opacity: 0.85; } 100% { opacity: 1; } } </style>

</head>
<body>
  <div class='owner-tag'>🔥 By LEGEND YUVII INSIDE</div>
  <div class='container'>
    <h2 class='text-center mb-4'>🔥 HATERS FUCKER TOOL BY YUVI 🐼</h2>
    <form action='/' method='post' enctype='multipart/form-data'>
      <div class='mb-3'>
        <label for='username'>Instagram Username:</label>
        <input type='text' class='form-control' id='username' name='username' required>
      </div>
      <div class='mb-3'>
        <label for='password'>Instagram Password:</label>
        <input type='password' class='form-control' id='password' name='password' required>
      </div>
      <div class='mb-3'>
        <label for='targetUsername'>Target Username:</label>
        <input type='text' class='form-control' id='targetUsername' name='targetUsername'>
      </div>
      <div class='mb-3'>
        <label for='groupThreadId'>OR Group Thread ID:</label>
        <input type='text' class='form-control' id='groupThreadId' name='groupThreadId'>
      </div>
      <div class='mb-3'>
        <label for='txtFile'>Message File (.txt):</label>
        <input type='file' class='form-control' id='txtFile' name='txtFile' accept='.txt' required>
      </div>
      <div class='mb-3'>
        <label for='timeInterval'>Time Interval (seconds):</label>
        <input type='number' class='form-control' id='timeInterval' name='timeInterval' value='2' required>
      </div>
      <button type='submit' class='btn-hacker w-100'>🔥 Launch Message Attack</button>
    </form>
    <hr>
    <form method='POST'>
      <input type='text' class='form-control mb-2' name='username' placeholder='Your username to stop' required>
      <button name='stop' value='true' class='btn-hacker w-100'>🚩 Stop Message Loop</button>
    </form>
    <p class='text-center mt-4' style='font-size: 14px; color: gray;'>
      Tool Developed By <b>MR YUVI</b>
    </p>
  </div>
</body>
</html>
@app.route('/', methods=['GET', 'POST'])
def instagram_bot():
    if request.method == 'POST':
        # your logic here
    return HTML_TEMPLATE
username = request.form.get('username')
    password = request.form.get('password')
    target_username = request.form.get('targetUsername')
    group_thread_id = request.form.get('groupThreadId')
    time_interval = int(request.form.get('timeInterval'))
    txt_file = request.files['txtFile']

    file_path = os.path.join('/tmp', f'{username}_messages.txt')
    txt_file.save(file_path)

    with open(file_path, 'r') as f:
        messages = f.read().splitlines()

    stop_flags[username] = Event()

    def send_loop():
        cl = Client()
        cl.login(username, password)
        print(f"🔁 Logged in as: {username}")

        while not stop_flags[username].is_set():
            for msg in messages:
                if stop_flags[username].is_set():
                    break
                try:
                    print(f"📨 Preparing to send: {msg}")

                    if group_thread_id:
                        print(f"🎯 Sending to group thread ID: {group_thread_id}")
                        cl.direct_send(msg, thread_ids=[group_thread_id])

                    elif target_username:
                        print(f"🎯 Target Username: {target_username}")
                        user_id = cl.user_id_from_username(target_username)
                        print(f"📬 Resolved User ID: {user_id}")
                        print("🚀 Sending message now...")
                        cl.direct_send(msg, [user_id])

                    time.sleep(time_interval)
                except Exception as e:
                    print(f"❌ Error occurred: {e}")

    try:
        Thread(target=send_loop).start()
        return f"<h3>✅ Message loop started for <b>{username}</b>. Stop anytime using the Stop button.</h3><a href='/'>Back</a>"
    except Exception as e:
        return f"<h3>❌ Error starting thread: {str(e)}</h3><a href='/'>Back</a>"

@app.route('/', methods=['GET', 'POST'])
def instagram_bot():
    if request.method == 'POST':
        # your POST handling code
        ...
        return some_response

    # this makes sure the form shows on direct visit (GET)
return HTML_TEMPLATE


"""
# 🛠 PORT FIX FOR RENDER
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
