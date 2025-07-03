from flask import Flask, request
from instagrapi import Client
import os
import time

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <h2 class='glow-text mb-4'>🔥 HATERS FUCKER TOOL BY YUVI 🐼</h2>
  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css' rel='stylesheet'>
  <style>
  body {
    background-image: url('https://i.postimg.cc/Wbc2fG9y/b7ae332981e970d9221a8d4e193e4c1e.jpg');
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
    background: rgba(0, 0, 0, 0.3); /* glass effect */
    backdrop-filter: blur(10px); /* glass blur */
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

  .glow-text {
  text-align: center;
  font-size: 22px;
  color: #00ff99;
  text-shadow: 0 0 10px #ff4d4d, 0 0 20px #ff4d4d, 0 0 40px #ff4d4d;
  animation: flicker 1.5s infinite alternate;
}

  @keyframes flicker {
    0% { opacity: 0.85; }
    100% { opacity: 1; }
  }
</style>
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

    <p class='text-center mt-4' style='font-size: 14px; color: gray;'>
      Tool Developed By <b>MR YUVI</b>
    </p>
  </div>
</body>
</html>
"""

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

            log = ""

            if group_thread_id:
                total = len(messages)
                for i, msg in enumerate(messages, 1):
                    cl.direct_send(msg, thread_ids=[group_thread_id])
                    log += f"✅ Sent {i}/{total}<br>\n"
                    time.sleep(time_interval)
                log += f"<br>🎉 All messages sent to group ID: {group_thread_id}"
                return log

            elif target_username:
                user_id = cl.user_id_from_username(target_username)
                total = len(messages)
                for i, msg in enumerate(messages, 1):
                    cl.direct_send(msg, [user_id])
                    log += f"✅ Sent {i}/{total}<br>\n"
                    time.sleep(time_interval)
                log += f"<br>🎉 All messages sent to {target_username}"
                return log

            else:
                return "<h3>❌ Please enter a username or group thread ID</h3>"

        except Exception as e:
            return f"<h3>❌ Error: {str(e)}</h3>"

    return HTML_TEMPLATE

# 🛠 PORT FIX FOR RENDER
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
