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
      margin: 0;
      padding: 0;
      height: 100vh;
      background: url('https://i.postimg.cc/Wbc2fG9y/b7ae332981e970d9221a8d4e193e4c1e.jpg') no-repeat center center/cover;
      position: relative;
      font-family: 'Segoe UI', sans-serif;
    }
    body::before {
      content: "";
      position: absolute;
      inset: 0;
      background: rgba(0, 0, 0, 0.6); /* dark overlay */
      z-index: 0;
    }
    .branding {
      text-align: center;
      margin-top: 20px;
      color: #00FF99;
      font-weight: bold;
      font-size: 28px;
      z-index: 2;
      position: relative;
    }
    .branding img {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      border: 2px solid #00FF99;
      margin-bottom: 10px;
    }
    .container {
      max-width: 500px;
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 20px;
      padding: 30px;
      margin: 30px auto;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
      position: relative;
      z-index: 2;
      color: white;
    }
    label, input {
      color: white !important;
    }
    .btn-custom {
      background-color: #00FF99;
      border: none;
      color: black;
      font-weight: bold;
    }
    .btn-custom:hover {
      background-color: #00cc77;
      color: white;
    }
  </style>
</head>
<body>
  <!-- 🔝 Logo and Brand Name -->
  <div class='branding'>
    <img src='https://i.postimg.cc/3w8nGHST/king-icon.png' alt='logo'>
    <div>KING MAKER YUVI</div>
  </div>

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
      <button type='submit' class='btn btn-custom w-100'>🚀 Send Messages</button>
    </form>

    <p class='text-center mt-4' style='font-size: 14px; color: #ccc;'>Tool Developed By <b>KING MAKER YUVI</b></p>
  </div>
</body>
</html>
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
