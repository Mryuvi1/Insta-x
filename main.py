from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h2>🔥 Tool Loaded Successfully on Render!</h2>"

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
