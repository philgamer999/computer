import ollama
import pyttsx3
import speech_recognition as sr
#import winsound
import os

# Define your keyword(s)
KEYWORDS = ["computer", "musik modus", "steuer modus", "stop", "test"]

# models
MODELS = ["llama3.2", "llama2-uncensored"]

# Variables
arguments = "Du bist ein hilfreicher Assistent und kannst nur wahrheitsgemäße Antworten geben. Halte deine Antworten kurz und prägnannt. Schreibe Zahlen aus und nutze keine Abkürzungen. "
text = "Bitte wiederhole folgenden Text: 'Hallo Welt!'"
engine_language = "de_DE"

# Beep properties
#frequency = 750  
#duration = 100  

# Initialize recognizer
keyword_recognizer = sr.Recognizer()


# create new voice_engine
def new_voice_engine():
    print("New instance of voice_engine created!")
    return pyttsx3.init()

# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(voice_engine, language, gender='VoiceGenderFemale'):
    engine_language = language
    print("Language changed to: "+engine_language)
    for voice in voice_engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            voice_engine.setProperty('voice', voice.id)
            return True
        #else:
            #raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

# change the rate to given value
def change_rate(voice_engine, new_rate):
    voice_engine.setProperty('rate', new_rate)
    print("Rate changed to: "+str(new_rate))

# change the volume to given value
def change_volume(voice_engine, new_volume):
    voice_engine.setProperty('volume', new_volume)
    print("Volume changed to: "+str(new_volume))

# recognize speech and translate to text
def speech_to_text():
    recognizer = sr.Recognizer()

    # List available microphones (optional)
    #print("Available microphones:")
    #print(sr.Microphone.list_microphone_names())

    # Select a specific microphone (optional)
    # with sr.Microphone(device_index=1) as source:
    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language=engine_language)
        print(f"User Input: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Error connecting to Google API: {e}")

# create ollama chat request and return responce
def ollama_chat_request(input_text):
    response = ollama.chat(model=MODELS[0], messages=[
        {
            'role': 'user',
            'content': arguments + input_text,
        },
    ])
    print(response['message']['content'])
    return response

# processing user input
def process_input(user_input):
    if user_input.lower() == '/bye':
        return False  # signal to stop looping
    else:
        # get ollama answer to input
        text = ollama_chat_request(user_input)['message']['content']

        voice_engine.say(text)
        voice_engine.runAndWait()
        return True # signal to continue looping

# await user input loop
def await_message():
    print("Awaiting Input!")
#    winsound.Beep(frequency, duration)
    user_input = speech_to_text()
    process_input(user_input)


def listen_for_keywords():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        keyword_recognizer.adjust_for_ambient_noise(source)
        print("Listening for keywords...")

        try:
            while True:
                # Listen to the audio from the microphone
                print("Listening...")
                audio = keyword_recognizer.listen(source)  # timeout=5 Timeout if no input in 5 seconds
                try:
                    # Recognize speech using Google Web Speech API
                    transcript = keyword_recognizer.recognize_google(audio, language=engine_language)
                    print(f"Transcript: {transcript}")

                    # Check if any keyword is present
                    for keyword in KEYWORDS:
                        if keyword.lower() in transcript.lower():
                            print(f"Keyword detected: {keyword}")
                            if keyword.lower() == "stop":
                                print("Exiting...")
                                return  # Exit the loop if 'exit' is detected
                            if keyword.lower() == "computer":
                                await_message()
                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError as e:
                    print(f"Request error: {e}")

        except KeyboardInterrupt:
            print("Stopping...")

#def setup_voice_engine(rate, volume, language, gender):

# setup new voice_engine
voice_engine = new_voice_engine()
change_rate(voice_engine, 200)
change_volume(voice_engine, 0.50)
change_voice(voice_engine, "de_DE", "VoiceGenderFemale")


if __name__ == "__main__":
    listen_for_keywords()