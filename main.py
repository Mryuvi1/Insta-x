from flask import Flask, request, render_template_string, jsonify
from instagrapi import Client
from threading import Thread, Event, Lock
import os
import time

app = Flask(name)

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
  <div class='owner-tag'>🔥 By LEGEND YUVII INSIDE</div>  <div class='container'>
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
"""clients = {}  # username: Client active_users = {}  # username: thread stop_events = {}

