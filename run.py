from app import app
from app import socketio

app.debug = True
socketio.run(app, host='0.0.0.0', debug=True, port=8890)
