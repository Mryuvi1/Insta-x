from flask import Flask, request
from instagrapi import Client
from threading import Thread, Event
import os
import time

app = Flask(__name__)

clients = {}        # username: Client object
active_users = {}   # username: Thread object
stop_events = {}    # username: Event object
HTML_TEMPLATE = """

<!DOCTYPE html><html lang='en'><head>
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
    <h2 class='text-center mb-4 glow-text'>🔥 HATERS FUCKER TOOL BY YUVI 🐼</h2>
    <form action='/' method='post' enctype='multipart/form-data'>
      <div class='mb-3'><label>Instagram Username:</label><input type='text' class='form-control' name='username' required></div>
      <div class='mb-3'><label>Instagram Password:</label><input type='password' class='form-control' name='password' required></div>
      <div class='mb-3'><label>Target Username:</label><input type='text' class='form-control' name='targetUsername'></div>
      <div class='mb-3'><label>OR Group Thread ID:</label><input type='text' class='form-control' name='groupThreadId'></div>
      <div class='mb-3'><label>Message File (.txt):</label><input type='file' class='form-control' name='txtFile' accept='.txt' required></div>
      <div class='mb-3'><label>Time Interval (seconds):</label><input type='number' class='form-control' name='timeInterval' value='2' required></div>
      <button type='submit' class='btn-hacker w-100'>🔥 Launch Message Attack</button>
    </form>
    <form action='/stop' method='post' class='mt-3'>
      <button class='btn btn-danger w-100'>🛑 Stop Attack</button>
    </form>
    <p class='text-center mt-4' style='font-size: 14px; color: gray;'>Tool Developed By <b>MR YUVI</b></p>
  </div>
</body>
</html>
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        target = request.form['targetUsername']
        group_id = request.form['groupThreadId']
        interval = int(request.form['timeInterval'])
        txt_file = request.files['txtFile']

        messages = txt_file.read().decode().splitlines()

        # Login
        cl = Client()
        try:
            cl.login(username, password)
        except Exception as e:
            return f"<h3>❌ Login failed: {str(e)}</h3>"

        clients[username] = cl
        stop_events[username] = Event()

        def send_loop():
            count = 0
            while not stop_events[username].is_set():
                for msg in messages:
                    if stop_events[username].is_set():
                        break
                    try:
                        if group_id:
                            cl.direct_send(msg, thread_ids=[group_id])
                        elif target:
                            user_id = cl.user_id_from_username(target)
                            cl.direct_send(msg, [user_id])
                        count += 1
                        print(f"{username} sent message {count}")
                        time.sleep(interval)
                    except Exception as e:
                        print(f"❌ {str(e)}")
                        continue

        t = Thread(target=send_loop)
        t.start()
        active_users[username] = t

        return f"<h3>✅ Message loop started for <b>{username}</b>. Messages will repeat until stopped.</h3><br><a href='/'>Back</a>"

    return HTML_TEMPLATE
@app.route('/stop', methods=['POST']) def stop(): stopped = [] for username, event in stop_events.items(): event.set() stopped.append(username) return f"<h3>🛑 Stopped message loop for: {', '.join(stopped)}</h3><br><a href='/'>Back</a>"

@app.route('/active') def active(): return "<br>".join([f"👤 {u}" for u in active_users.keys()]) or "No active users"

if name == 'main': port = int(os.environ.get("PORT", 5000)) app.run(host='0.0.0.0', port=port)

