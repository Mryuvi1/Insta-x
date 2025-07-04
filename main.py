import traceback
from flask import Flask, request
from instagrapi import Client
from threading import Thread, Event
import os
import time

app = Flask(__name__)

clients = {}
stop_flags = {}
active_users = set()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
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
    <h2 class='text-center mb-4'>🔥 HATERS FUCKER TOOL BY YUVI 🐼</h2>
    <form action='/' method='post' enctype='multipart/form-data'>
      <input type='text' class='form-control mb-2' name='username' placeholder='Instagram Username' required>
      <input type='password' class='form-control mb-2' name='password' placeholder='Instagram Password' required>
      <input type='text' class='form-control mb-2' name='victimName' placeholder='Victim Name (e.g. X-Boyfriend)' required>
      <input type='text' class='form-control mb-2' name='targetUsername' placeholder='Target Username (optional)'>
      <input type='text' class='form-control mb-2' name='groupThreadId' placeholder='OR Group Thread ID'>
      <input type='file' class='form-control mb-2' name='txtFile' accept='.txt' required>
      <input type='number' class='form-control mb-2' name='timeInterval' placeholder='Time Interval (sec)' value='2' required>
      <button type='submit' class='btn-hacker w-100'>🔥 Launch Message Attack</button>
    </form>
    <form method='POST' class='mt-3'>
      <input type='text' class='form-control mb-2' name='username' placeholder='Username to Stop' required>
      <button name='stop' value='true' class='btn btn-danger w-100'>🛑 Stop Message Loop</button>
    </form>
    <div class='text-center mt-4'>
      <small style='color: gray;'>Tool Developed By <b>MR YUVI</b></small>
    </div>
  </div>
</body>
</html>
"""

@app.route('/', methods=["GET", "POST"])
def instagram_bot():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # do login, send messages, etc.
        return "✅ Message sending started!"

    return render_template("index.html")  # for GET request
  
@app.route('/', methods=['GET', 'POST'])
def instagram_bot():
    if request.method == 'POST':
        if 'stop' in request.form:
            username = request.form.get('username')
            if username in stop_flags:
                stop_flags[username].set()
                return f"<h3>🛑 Stopped messaging for <b>{username}</b></h3><a href='/'>Back</a>"
            else:
                return f"<h3>❌ No active loop for <b>{username}</b></h3><a href='/'>Back</a>"

        # Start Attack
        username = request.form['username']
        password = request.form['password']
        victim_name = request.form.get('victimName', '')
        target_username = request.form.get('targetUsername')
        group_thread_id = request.form.get('groupThreadId')
        time_interval = int(request.form['timeInterval'])
        txt_file = request.files['txtFile']

        file_path = os.path.join('/tmp', f'{username}_messages.txt')
        txt_file.save(file_path)

        with open(file_path, 'r') as f:
            messages = f.read().splitlines()

        stop_flags[username] = Event()

def send_loop():
    try:
        cl = Client()
        cl.login(username, password)
        print("✅ Login successful for:", username)

        clients[username] = cl
        active_users.add(username)

        print("✅ Loop started for:", username)
        print("📨 Messages loaded:", messages)

        while not stop_flags[username].is_set():
            print("🔁 Loop running...")

            for msg in messages:
                if stop_flags[username].is_set():
                    print("⛔️ Stop flag detected, breaking loop.")
                    break

                try:
                    full_msg = f"{victim_name}: {msg}" if victim_name else msg
                    print("📤 Message to send:", full_msg)

                    if group_thread_id:
                        print("➡️ Sending to group:", group_thread_id)
                        cl.direct_send(full_msg, thread_ids=[group_thread_id])
                    elif target_username:
                        print("➡️ Sending to user:", target_username)
                        user_id = cl.user_id_from_username(target_username)
                        print("👤 Resolved user ID:", user_id)
                        cl.direct_send(full_msg, [user_id])

                    print("✅ Sent successfully!")
                    time.sleep(time_interval)

                except Exception as e:
                    print("❌ Send error:")
                    traceback.print_exc()

    except Exception as e:
        print("❌ Login error:")
        traceback.print_exc()

    except Exception as e:
        print("❌ Login error:")
        traceback.print_exc()

        Thread(target=send_loop).start()
        return f"<h3>✅ Message loop started for <b>{username}</b>. You can stop anytime.</h3><a href='/'>Back</a>"

    return HTML_TEMPLATE

@app.route('/active')
def active():
    return "<br>".join([f"👤 {u}" for u in active_users]) or "No active users"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
