import os
import subprocess
import sys
import time
import datetime

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import ensurepip
    ensurepip.bootstrap()
except ImportError:
    pass

try:
    import setuptools
except ImportError:
    install("setuptools")
    import setuptools

try:
    import speech_recognition as sr
except ImportError:
    install("SpeechRecognition")
    import speech_recognition as sr

try:
    import pyttsx3
except ImportError:
    install("pyttsx3")
    import pyttsx3

try:
    import pywhatkit
except ImportError:
    install("pywhatkit")
    import pywhatkit

try:
    import pyaudio
except ImportError:
    install("pyaudio")
    import pyaudio

# Initialize recognizer and text-to-speech engine
r = sr.Recognizer()
machine = pyttsx3.init()

# List all available microphones and select the correct one
def list_microphones():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"Device {i}: {info['name']}")
    p.terminate()

# Test microphone input
def test_microphone(device_index):
    try:
        with sr.Microphone(device_index=device_index) as source:
            r.energy_threshold = 300  # Lower the threshold to capture quieter sounds
            r.adjust_for_ambient_noise(source, duration=2)  # Increased calibration time
            print(f"Testing microphone: {device_index}")
            print("Listening...")
            audio = r.listen(source)
            print("Captured audio successfully!")
            
            try:
                instruction = r.recognize_google(audio)  # Attempt Google Speech Recognition
                print(f"Recognized instruction: {instruction}")
                return instruction
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            
            # Try using Sphinx as a fallback if Google fails
            try:
                instruction = r.recognize_sphinx(audio)  # Offline Sphinx recognition
                print(f"Recognized instruction (Sphinx): {instruction}")
                return instruction
            except sr.UnknownValueError:
                print("Sphinx could not understand the audio.")
            except sr.RequestError as e:
                print(f"Sphinx error; {e}")

    except Exception as e:
        print(f"Error accessing the microphone: {e}")
    
    return None

# Text-to-speech function
def talk(text):
    machine.say(text)
    machine.runAndWait()

# Get instruction via microphone
def get_instruction(device_index):
    instruction = test_microphone(device_index)
    if instruction is not None and "jarvis" in instruction:
        instruction = instruction.replace('jarvis', "")
        return instruction
    return None

# Execute the instruction
def play_instruction(device_index):
    instruction = get_instruction(device_index)
    if instruction is not None and "play" in instruction:
        song = instruction.replace('play', "") 
        talk("Playing " + song)   
        pywhatkit.playonyt(song)
    elif instruction is not None and 'time' in instruction:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk('The current time is ' + current_time)

# Main program flow
if __name__ == "__main__":
    # List all microphones and select one
    list_microphones()
    device_index = int(input("Enter the device index of your microphone: "))
    
    # Execute the virtual assistant's functionalities
    play_instruction(device_index)