from flask import Flask, render_template
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    print(f"Templates folder path: {os.path.abspath(app.template_folder)}")  # Debugging line
    return render_template('index.html')

@socketio.on('my event')
def handle_my_event(json):
    print('Received event: ' + str(json))

if __name__ == '__main__':
    socketio.run(app, debug=True)