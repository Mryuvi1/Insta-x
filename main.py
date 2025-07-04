from flask import Flask, request
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h2 style="color: green;">✅ Tool Loaded Successfully!</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Enter your name">
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        return f"<h3>Hello, {username}!</h3><br><a href='/'>Back</a>"
    return HTML_TEMPLATE

# Render-compatible port binding
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # For Render
    app.run(host='0.0.0.0', port=port)
