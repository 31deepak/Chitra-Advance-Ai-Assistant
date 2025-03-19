web: gunicorn app:app
web: uvicorn main:app --host 0.0.0.0 --port ${PORT}
web: Xvfb :99 -screen 0 1024x768x24 & python main.py
apt-get install -y xvfb
Xvfb :99 -screen 0 1024x768x16 &
export DISPLAY=:99


