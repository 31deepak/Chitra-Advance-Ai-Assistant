web: gunicorn app:app
web: uvicorn main:app --host 0.0.0.0 --port ${PORT}
web: Xvfb :99 -screen 0 1024x768x24 & python main.py
web: DISPLAY=:99 python main.py

