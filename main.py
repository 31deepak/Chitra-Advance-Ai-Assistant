import os
import eel
import subprocess
from fastapi import FastAPI
from engine.features import *
from engine.command import *
from engine.auth import recoganize

app = FastAPI()

eel.init("www")

def start():
    playAssistantSound()
    
    @eel.expose
    def init():
        subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Sir, How can I Help You")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Fail")
    
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=False)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
