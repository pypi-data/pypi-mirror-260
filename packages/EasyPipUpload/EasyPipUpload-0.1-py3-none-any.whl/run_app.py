import os
import platform
from app import app
import webbrowser
from waitress import serve
import subprocess

# Remove all old files from static/wheel folder
wheel_files_loc = os.path.join(os.getcwd(), 'static', 'wheel')
for file in os.listdir(wheel_files_loc):
    if file:
        os.remove(os.path.join(wheel_files_loc, file))

# Run the app
def start_server():
    url = "http://127.0.0.1:5000"
    webbrowser.open(url)

    if platform.system() == 'Windows':
        # Use Waitress on Windows
        serve(app, host='127.0.0.1', port=5000)
    else:
        # Use Gunicorn on Unix-based systems
        subprocess.check_call(['gunicorn', 'app:app', '-b', '127.0.0.1:5000'])

if __name__ == '__main__':
    start_server()