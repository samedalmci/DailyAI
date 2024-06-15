import speech_recognition as sr
import pyttsx3 
import datetime
import os

# Initialize the recognizer 
r = sr.Recognizer() 

# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
    
# Loop infinitely for user to speak
while True: 
    # Exception handling to handle exceptions at the runtime
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source:
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
            r.adjust_for_ambient_noise(source, duration=0.2)
            #listens for the user's input 
            audio = r.listen(source)
            # Using google to recognize audio
            MyText = r.recognize_google(audio)
            MyText = MyText.lower()
            print("Did you say:", MyText)
            SpeakText(MyText)
            
            # Dosya adını ve yolu belirleyin
            file_path = r"C:\Users\Berat Can\Desktop\text to spech"
            # Eğer belirtilen dizin yoksa, oluşturun
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_name = os.path.join(file_path, "recorded_text_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt")

            # Tanımlanan metni dosyaya yazma
            with open(file_name, "w") as file:
                file.write(MyText)

            # Kullanıcıya dosyanın kaydedildiğini bildirin
            print("Recorded text saved as:", file_name)
            
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        
    except sr.UnknownValueError:
        print("unknown error occurred")
