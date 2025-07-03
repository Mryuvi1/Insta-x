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
  <title>🩷 Group/DM Messenger | LEGEND YUVI 🐼</title>
  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css' rel='stylesheet'>
  <style>
    body {
      background-image: url('https://i.postimg.cc/Wbc2fG9y/b7ae332981e970d9221a8d4e193e4c1e.jpg');
      background-size: cover;
      background-repeat: no-repeat;
      background-position: center;
      height: 100vh;
      margin: 0;
    }
    .container {
      max-width: 500px;
      background-color: rgba(255, 255, 255, 0.95);
      border-radius: 10px;
      padding: 20px;
      margin: 0 auto;
      margin-top: 50px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .owner-tag {
      position: fixed;
      top: 10px;
      left: 10px;
      color: white;
      font-weight: bold;
      z-index: 999;
      text-shadow: 1px 1px 3px black;
    }
  </style>
</head>
<body>
  <div class='owner-tag'>🔥 By LEGEND YUVII INSIDE</div>

  <div class='container'>
    <h2 class='text-center mb-4'>Instagram DM / Group Messenger</h2>
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
      <button type='submit' class='btn btn-success w-100'>Send Messages</button>
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

            if group_thread_id:
                for msg in messages:
                    cl.direct_send(msg, [], thread=group_thread_id)
                    time.sleep(time_interval)
                return f"<h3>✅ Messages sent to Instagram Group (Thread ID: {group_thread_id})</h3>"

            elif target_username:
                user_id = cl.user_id_from_username(target_username)
                for msg in messages:
                    cl.direct_send(msg, [user_id])
                    time.sleep(time_interval)
                return f"<h3>✅ Messages sent to {target_username}</h3>"

            else:
                return "<h3>❌ Please enter a username or group thread ID</h3>"

        except Exception as e:
            return f"<h3>❌ Error: {str(e)}</h3>"

    return HTML_TEMPLATE

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
