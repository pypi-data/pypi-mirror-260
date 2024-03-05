from PIL import Image
import threading
from playsound import playsound

def play_sound(sound_path):
    try:
        playsound(sound_path)
    except:
        print("Error in audio")

def RunFun(sound_path, image_path):
    try:
        threading.Thread(target=lambda: play_sound(sound_path)).start()
        img = Image.open(image_path)
        img = img.resize((300, 300))
        img.show()

    except:
        print("Error in image")


def start():
    
    sound_path = "Audio.wav"
    image_path = "abdo.png"

    # Button to load and display the image
    RunFun(sound_path, image_path)

start()