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
  <title>🩷𝐇𝐀𝐓𝐄𝐑𝐒 𝐅𝐔𝐂𝐊𝐄𝐑 𝐓𝐎𝐎𝐋 BY | 𝐋𝐄𝐆𝐄𝐍𝐃 𝐘𝐔𝐕𝐈 🐼</title>
  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css' rel='stylesheet'>
<style>
  body {
    background-image: url('https://i.postimg.cc/Wbc2fG9y/b7ae332981e970d9221a8d4e193e4c1e.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    height: 100vh;
    margin: 0;
    backdrop-filter: blur(6px);
  }
  .container {
    max-width: 500px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 20px;
    padding: 25px;
    margin: 0 auto;
    margin-top: 60px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
  }
  .btn-primary {
    background-color: #90ee90 !important;
    color: black !important;
    border: none !important;
    font-weight: bold;
  }
</style>
</head>
<body>
  <!-- 🔥 Owner Branding Top Left -->
  <div class='owner-tag'>🔥 By LEGEND YUVII INSIDE</div>

  <div class='container'>
    <h2 class='text-center mb-4'>Instagram Messaging Bot</h2>
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
        <input type='text' class='form-control' id='targetUsername' name='targetUsername' required>
      </div>
      <div class='mb-3'>
        <label for='txtFile'>Message File (.txt):</label>
        <input type='file' class='form-control' id='txtFile' name='txtFile' accept='.txt' required>
      </div>
      <div class='mb-3'>
        <label for='timeInterval'>Time Interval (seconds):</label>
        <input type='number' class='form-control' id='timeInterval' name='timeInterval' value='2' required>
      </div>
      <button type='submit' class='btn btn-primary w-100'>Send Messages</button>
    </form>

    <!-- 🔻 Footer Branding -->
    <p class='text-center mt-4' style='font-size: 14px; color: gray;'>
      Tool Developed By <b>MR YUVI</b>
    </p>
  </div>
  <script>
  document.querySelector('form').addEventListener('submit', function() {
    alert('Sending messages... Please wait!');
  });
</script>
</body>
</html>
"""
from flask import Response

def check_auth(username, Mryuvi):
    return username == "admin" and password == "yuvihere"

def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.before_request
def require_auth():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
      
@app.route('/', methods=['GET', 'POST'])
def instagram_bot():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        target_username = request.form.get('targetUsername')
        time_interval = int(request.form.get('timeInterval'))
        txt_file = request.files['txtFile']

        file_path = os.path.join('/tmp', 'uploaded_messages.txt')
        txt_file.save(file_path)

        with open(file_path, 'r') as f:
            messages = f.read().splitlines()
        
        if len(messages) > 20:
            return "<h3>❌ You can only send up to 20 messages at once.</h3>"

        try:
            cl = Client()
            cl.login(username, password)
            user_id = cl.user_id_from_username(target_username)

            for msg in messages:
                cl.direct_send(msg, [user_id])
                time.sleep(time_interval)

            return f"<h3>✅ Messages sent successfully to {target_username}</h3>"
        except Exception as e:
            return f"""
                <h3 style='color:red;'>❌ Error Occurred</h3>
                <p>{str(e)}</p>
                <a href='/'>Go Back</a>
            """
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
    return HTML_TEMPLATE

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
