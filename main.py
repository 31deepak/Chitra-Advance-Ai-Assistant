import os
import eel
import subprocess
import threading
from fastapi import FastAPI
from engine.features import 
from engine.command import *
from engine.auth import recoganize
import uvicorn
from pyvirtualdisplay import Display
display = Display(visible=False, size=(1024, 768))
display.start()


app = FastAPI()

# Initialize Eel
eel.init("www")

def start_eel():
    """Function to start Eel in a separate thread."""
    playAssistantSound()

    @eel.expose
    def init():
        try:
            subprocess.call([r'device.bat'])
            eel.hideLoader()
            speak("Ready for Face Authentication")
            flag = recoganize.AuthenticateFace()

            if flag == 1:
                eel.hideFaceAuth()
                speak("Face Authentication Successful")
                eel.hideFaceAuthSuccess()
                speak("Hello, Welcome Sir, How can I help you?")
                eel.hideStart()
                playAssistantSound()
            else:
                speak("Face Authentication Failed")
        except Exception as e:
            print(f"Error in Eel function: {e}")

    # Open in Microsoft Edge as a web app
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    # Start Eel
    try:
        eel.start('index.html', mode=None, host='localhost', block=True)
    except Exception as e:
        print(f"Eel failed to start: {e}")

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

def run_fastapi():
    """Function to run FastAPI server."""
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    # Start Eel in the main thread
    start_eel()
