import customtkinter as ctk
import tkinter
import threading
import pyaudio
import wave
import os.path
import openai  
from PIL import Image, ImageTk
import requests, io
import requests
import pyaudio
import wave
import os
import requests
import re
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import pyttsx3
import time
from googletrans import Translator



###########################################################################################
def text_to_speech():
    
    
    # Türkçe metni al
    turkish_text = prompt_imageentry.get("1.0", "end-1c")
    
    # Metni İngilizce'ye çevir
    translator = Translator()
    translated_text = translator.translate(turkish_text, src='tr', dest='en').text
    
    # İngilizce metni ses olarak oku
    engine = pyttsx3.init()
    engine.say(translated_text)
    engine.runAndWait()
    
###########################################################################################
def generateimage():
    openai.api_key = "API KEY OPEN AI"
    user_prompt = prompt_imageentry.get("0.0", tkinter.END)
    user_prompt += "in style: " + style_imagedropdown.get()

    canvas.delete("all")
    canvas_width = 512  # Canvas genişliğini ayarlayın
    canvas_height = 512  # Canvas yüksekliğini ayarlayın
    canvas.config(width=canvas_width, height=canvas_height)

    response = openai.Image.create(
        prompt=user_prompt,
        n=int(number_imageslider.get()),
        size="512x512"
    )


    image_urls = []
    for i in range(len(response['data'])):
        image_urls.append(response['data'][i]['url'])

    images = []
    for url in image_urls:
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        photo_image = ImageTk.PhotoImage(image)
        images.append(photo_image)

    def update_image(index=0):
        canvas.delete("all")  # Önceki resmi temizle
        canvas.create_image(0, 0, anchor="nw", image=images[index])
        index = (index + 1) % len(images) 
        canvas.after(3000, update_image, index)

    update_image()  # update_image fonksiyonunu çağır
########################################################################################### 



###########################################################################################

def record_button_event():
    global recording  # Declare recording as a global variable
    if recording:
        recording = False
        record_button.configure(fg_color="Red")
        record_button.configure(border_color="Red")
       
    else:
        recording=True
        record_button.configure(fg_color="Green")
        record_button.configure(border_color="Green")
        threading.Thread(target=recorder).start()


def recorder():
    openai.api_key = "API KEY OPEN AI"
    audio=pyaudio.PyAudio()
    stream=audio.open(format=pyaudio.paInt16, channels=1,rate=44100,input=True,frames_per_buffer=1024)
    frames =[]


    while recording:
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()


    exists=True
    i=1
    while exists:
        if os.path.exists(f"myrecording{i}.wav"):
            i+=1
        else:
            exists=False

    sound_file=wave.open(f"myrecording{i}.wav","wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()
    prompt_textentry.delete("1.0","end")

    if  translate.get() == 1:
        audio_file = open(f"myrecording{i}.wav", "rb")
        transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file)
        prompt_textentry.insert(1.0, text=transcript.text)
    else:
        audio_file = open(f"myrecording{i}.wav", "rb")
        transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file)
        prompt_textentry.insert(1.0, text=transcript.text)

###########################################################################################  
def get_exchange_rate(api_key2, base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{api_key2}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    return data['conversion_rates'][target_currency]

# Buraya kendi API anahtarınızı ekleyin
api_key2 = 'EXCHANGE RATE API'


def update_label_with_exchange_rate():
    user_text = prompt_textentry.get("1.0", "end-1c").strip()
    currencies = re.findall(r'\b[A-Z]{3}\b', user_text)

    canvas.delete("all")
    canvas_width = 512  # Canvas genişliğini ayarlayın
    canvas_height = 512  # Canvas yüksekliğini ayarlayın
    canvas.config(width=canvas_width, height=canvas_height)

    # Bayrak ve döviz sembolü dosya yolları (bunları projenizin içine eklemeniz gerekir)
    flag_paths = {
        'USD': 'C:/Users/samed/Desktop/AiGUI/flags/us.png',
        'TRY': 'C:/Users/samed/Desktop/AiGUI/flags/tr.png',
        'EUR': 'C:/Users/samed/Desktop/AiGUI/flags/eu.png',
    }
    symbol_paths = {
        'USD': 'C:/Users/samed/Desktop/AiGUI/symbols/dollar.png',
        'TRY': 'C:/Users/samed/Desktop/AiGUI/symbols/lira.png',
        'EUR': 'C:/Users/samed/Desktop/AiGUI/symbols/euro.png',
        # Diğer para birimleri için sembolleri ekleyin
    }

    if len(currencies) == 2:
        base_currency = currencies[0]
        target_currency = currencies[1]

        try:
            exchange_rate = get_exchange_rate(api_key2, base_currency, target_currency)

            # Canvas'ı temizleyin
            canvas.delete("all")

            # Bayrakları ekleyin
            if base_currency in flag_paths and target_currency in flag_paths:
                base_flag = Image.open(flag_paths[base_currency])
                target_flag = Image.open(flag_paths[target_currency])
                base_flag = base_flag.resize((50, 30))
                target_flag = target_flag.resize((50, 30))
                base_flag_img = ImageTk.PhotoImage(base_flag)
                target_flag_img = ImageTk.PhotoImage(target_flag)
                canvas.create_image(50, 50, image=base_flag_img, anchor="nw")
                canvas.create_image(412, 50, image=target_flag_img, anchor="nw")
                canvas.image1 = base_flag_img  # Referansı tutmak için
                canvas.image2 = target_flag_img  # Referansı tutmak için

            # Döviz sembollerini ekleyin
            if base_currency in symbol_paths and target_currency in symbol_paths:
                base_symbol = Image.open(symbol_paths[base_currency])
                target_symbol = Image.open(symbol_paths[target_currency])
                base_symbol = base_symbol.resize((30, 30))
                target_symbol = target_symbol.resize((30, 30))
                base_symbol_img = ImageTk.PhotoImage(base_symbol)
                target_symbol_img = ImageTk.PhotoImage(target_symbol)
                canvas.create_image(100, 150, image=base_symbol_img, anchor="nw")
                canvas.create_image(350, 150, image=target_symbol_img, anchor="nw")
                canvas.image3 = base_symbol_img  # Referansı tutmak için
                canvas.image4 = target_symbol_img  # Referansı tutmak için

            # Döviz kuru metnini ekleyin
            canvas.create_text(256, 256, text=f"1 {base_currency} = {exchange_rate} {target_currency}", font=("Helvetica", 24), fill="black")

            # Alt metin ekleyin
            canvas.create_text(256, 300, text="Türk Lirası Değer Kaybetmeye devam ediyor", font=("Helvetica", 12), fill="black")

        except KeyError:
            prompt_textentry.delete("1.0", "end")
            prompt_textentry.insert("1.0", "Geçersiz döviz kısaltmaları. Lütfen tekrar deneyin.\n")
    else:
        prompt_textentry.delete("1.0", "end")
        prompt_textentry.insert("1.0", "Lütfen iki geçerli döviz kısaltması girin (örneğin, USD TRY).\n")

########################################################################################### 

###########################################################################################   

def get_interest_rate_based_on_input():
    user_input = prompt_textentry.get("1.0", tkinter.END).lower()
    

    if "federal funds rate" in user_input:
        get_fred_interest_rate("FEDFUNDS")
    elif "discount rate" in user_input:
        get_fred_interest_rate("DISCOUNT")
    elif "prime rate" in user_input:
        get_fred_interest_rate("DPRIME")
    elif "libor" in user_input:
        get_fred_interest_rate("USD3MTD156N")
    elif "t-bill rates" in user_input:
        get_fred_interest_rate("TB3MS")
    elif "mortgage rates" in user_input:
        get_fred_interest_rate("MORTGAGE30US")
    else:
        prompt_textentry.delete("1.0", "end")
        prompt_textentry.insert("1.0", "Lütfen 'Federal Funds Rate', 'Discount Rate', 'Prime Rate', 'LIBOR', 'T-Bill Rates' veya 'Mortgage Rates' içeren bir ifade girin.\n")
        


def get_fred_interest_rate(series_id):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key1}&file_type=json"
    response = requests.get(url)
    data = response.json()
    
    canvas.delete("all")
    canvas_width = 512  # Canvas genişliğini ayarlayın
    canvas_height = 512  # Canvas yüksekliğini ayarlayın
    canvas.config(width=canvas_width, height=canvas_height)

    if 'observations' in data and data['observations']:
        dates = [obs['date'] for obs in data['observations']]
        values = [float(obs['value']) for obs in data['observations']]
        

         # Canvas'ı temizleyin
        canvas.delete("all")
        
        # Grafik oluşturma
        plt.figure(figsize=(10, 6))
        plt.plot(dates, values, marker='o', linestyle='-')
        plt.xlabel('Tarih')
        plt.ylabel('Faiz Oranı (%)')
        plt.title(f'{series_id} Faiz Oranı')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Çizgi grafiğini canvas üzerine yerleştirme
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image = Image.open(buf)
        image = image.resize((512, 512))  # Resmi 512x512 boyutuna yeniden boyutlandır
        photo = ImageTk.PhotoImage(image)

        canvas.delete("all")  # Önceki resmi temizle
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo  # Referansı tutmak için
        

        plt.close()  # Plot penceresini kapat

        # Faiz oranını prompt_textentry'e ekleme
        latest_observation = data['observations'][-1]
        date = latest_observation['date']
        value = latest_observation['value']
        prompt_textentry.delete("1.0", "end")
        prompt_textentry.insert("1.0", f"En son faiz oranı ({date}): {value}%\n")


api_key1 = 'STLOUISFED API'


###########################################################################################

###########################################################################################    
def chat_with_gpt():
    openai.api_key = "API KEY OPEN AI"
    _model = "gpt-3.5-turbo"
    prompt = "sana verilen cümleyi mantıklı bir gazete haberi gibi devam ettir"
    prompt += prompt_textentry.get("1.0", "end-1c")  # Metnin sonundaki '\n' karakterini kaldırmak için 'end-1c' kullanılıyor.

    chat_prompt = [{"role":"user", "content":prompt}]
    response = openai.ChatCompletion.create(model=_model, messages=chat_prompt)
    response_text = response.choices[0].message.content
    prompt_textentry.delete("1.0", "end")
    prompt_imageentry.insert("1.0", response_text)

########################################################################################### 
def chat_with_Hava():
    openai.api_key = "API KEY OPEN AI"
    _model = "gpt-3.5-turbo"
    prompt = "Sana verilen Hava durumlarını yorumla yorumladığın havanın tarihini ve giyilmesi gereken uygun kıyafetleride söyle"
    prompt += prompt_textentry.get("1.0", "end-1c")  # Metnin sonundaki '\n' karakterini kaldırmak için 'end-1c' kullanılıyor.

    chat_prompt = [{"role":"user", "content":prompt}]
    response = openai.ChatCompletion.create(model=_model, messages=chat_prompt)
    response_text = response.choices[0].message.content
    prompt_textentry.delete("1.0", "end")
    prompt_textentry.insert("1.0", response_text)   

########################################################################################### 
def chat_with_Doviz():
    openai.api_key = "API KEY OPEN AI"
    _model = "gpt-3.5-turbo"
    prompt = "Sana verilen Döviz değerlerini yorumla ve tavsiyesi ver"
    prompt += prompt_textentry.get("1.0", "end-1c")  # Metnin sonundaki '\n' karakterini kaldırmak için 'end-1c' kullanılıyor.

    chat_prompt = [{"role":"user", "content":prompt}]
    response = openai.ChatCompletion.create(model=_model, messages=chat_prompt)
    response_text = response.choices[0].message.content
    prompt_textentry.delete("1.0", "end")
    prompt_textentry.insert("1.0", response_text)   


###########################################################################################
########################################################################################### 
def chat_with_Ekonomi():
    openai.api_key = "API KEY OPEN AI"
    _model = "gpt-3.5-turbo"
    prompt = "Kullanıcın verdiği Faiz oranını değerlendir ve tavsiye ver"
    prompt += prompt_textentry.get("1.0", "end-1c")  # Metnin sonundaki '\n' karakterini kaldırmak için 'end-1c' kullanılıyor.

    chat_prompt = [{"role":"user", "content":prompt}]
    response = openai.ChatCompletion.create(model=_model, messages=chat_prompt)
    response_text = response.choices[0].message.content
    prompt_textentry.delete("1.0", "end")
    prompt_textentry.insert("1.0", response_text)   


###########################################################################################


###########################################################################################
def get_forecast(api_key, city):
    url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"
    response = requests.get(url)
    data = response.json()
    return data

# WeatherAPI.com API anahtarınızı buraya ekleyin
api_key = 'WEATHER API'
icon_images = []  # Tüm ikonları saklamak için bir liste oluşturun


def update_label_with_forecast():
    city = prompt_textentry.get("1.0", "end-1c").strip()
    forecast_data = get_forecast(api_key, city)

    canvas.delete("all")
    canvas_width = 800  # Canvas genişliğini ayarlayın
    canvas_height = 200  # Canvas yüksekliğini ayarlayın
    canvas.config(width=canvas_width, height=canvas_height)
    
    canvas.create_text(canvas_width // 2, 20, text=f"Hava Durumu: {city}", font=("Helvetica", 12, "bold"))
    
    prompt_textentry.delete("1.0", "end")  # prompt_textentry'deki mevcut içeriği temizle

    if 'forecast' in forecast_data and 'forecastday' in forecast_data['forecast']:     
        icon_size = 50  # İkon boyutu (piksel)
        x_offset = 30  # Başlangıç x konumu
        y_offset = 60  # Başlangıç y konumu
        rect_width = 200  # Dikdörtgen genişliği
        rect_height = 110  # Dikdörtgen yüksekliği

        for i, day in enumerate(forecast_data['forecast']['forecastday']):
            date = day['date']
            condition = day['day']['condition']['text']
            max_temp = day['day']['maxtemp_c']
            min_temp = day['day']['mintemp_c']
            icon_url = day['day']['condition']['icon']

            x_position = x_offset + i * (rect_width + 20)  # Sabit bir x konumu belirleyin

            # Dikdörtgen çizimi
            canvas.create_rectangle(x_position, y_offset, x_position + rect_width, y_offset + rect_height, outline="black", width=2)

            # Tarih ve hava durumu metnini oluşturun
            text = f"{date}\nCondition: {condition}\nMax Temp: {max_temp}°C\nMin Temp: {min_temp}°C"
            canvas.create_text(x_position + 10, y_offset + 10, text=text, font=("Helvetica", 12), anchor="nw")

            # Hava durumu simgesi
            if i < len(icon_images):  # Eğer ikonlar daha önce yüklenmişse
                icon_photo = icon_images[i]  # Önceden yüklenmiş ikonu kullanın
            else:  # İkon yüklenmemişse
                icon_response = requests.get(f"http:{icon_url}", stream=True)
                icon_image = Image.open(icon_response.raw).resize((icon_size, icon_size))
                icon_photo = ImageTk.PhotoImage(icon_image)
                icon_images.append(icon_photo)  # Yüklenen ikonu listeye ekleyin

            canvas.create_image(x_position + rect_width // 2, y_offset + rect_height // 2 + 40, image=icon_photo, anchor="center")
            
            # prompt_textentry'e bilgileri ekle
            prompt_textentry.insert("end", f"{date} - Condition: {condition}, Max Temp: {max_temp}°C, Min Temp: {min_temp}°C\n")

    else:
        canvas.create_text(canvas_width // 2, canvas_height // 2, text="Hava durumu bilgisi bulunamadı.", font=("Helvetica", 12), anchor="center")
        prompt_textentry.insert("end", "Hava durumu bilgisi bulunamadı.\n")
        
###########################################################################################
#Image Genereator
root = ctk.CTk()
root.title("AI Image Generator")

ctk.set_appearance_mode("dark")

input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)


prompt_imagelabel = ctk.CTkLabel(input_frame, text="AI Story For Images")
prompt_imagelabel.grid(row=0,column=0, padx=10, pady=10)
prompt_imageentry = ctk.CTkTextbox(input_frame, height=200,wrap=tkinter.WORD)
prompt_imageentry.grid(row=0,column=1, padx=10, pady=10)

style_imagelabel = ctk.CTkLabel(input_frame, text="Title")
style_imagelabel.grid(row=1,column=0, padx=10, pady=10)
style_imagedropdown = ctk.CTkComboBox(input_frame, values=["Realistic", "Cartoon", "3D Illustration", "Flat Art"])
style_imagedropdown.grid(row=1, column=1, padx=10, pady=10)

number_imagelabel = ctk.CTkLabel(input_frame, text="# Images")
number_imagelabel.grid(row=2,column=0)
number_imageslider = ctk.CTkSlider(input_frame, from_=1, to=10, number_of_steps=9)
number_imageslider.grid(row=2,column=1)

generate_imagebutton = ctk.CTkButton(input_frame, text="Generate", command=generateimage)
generate_imagebutton.grid(row=3, column=0, columnspan=2, sticky="news", padx=10, pady=10)

generate_sphbutton = ctk.CTkButton(input_frame, text="Read", command=text_to_speech)
generate_sphbutton.grid(row=4, column=0, columnspan=2, sticky="news", padx=10, pady=10)

canvas = tkinter.Canvas(root, width=512, height=512)
canvas.pack(side="left")

input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)

###########################################################################################
def update_button_command(choice):
    if choice == "Kendi Gazeteni Yaz":
        generate_textbutton.configure(command=chat_with_gpt)
    elif choice == "Kur Farkları":
        generate_textbutton.configure(command=lambda: call_functions(update_label_with_exchange_rate, chat_with_Doviz))
    elif choice == "Ekonomik veriler":
        generate_textbutton.configure(command=lambda: call_functions(get_interest_rate_based_on_input, chat_with_Ekonomi)) 
    elif choice == "Hava Durumu":
        generate_textbutton.configure(command=lambda: call_functions(update_label_with_forecast, chat_with_Hava))

def call_functions(func1, func2):
    func1()
    time.sleep(1)
    func2()

###########################################################################################
#Input Text
prompt_textlabel = ctk.CTkLabel(input_frame, text="Your News Story")
prompt_textlabel.grid(row=1,column=0, padx=10, pady=10)
prompt_textentry = ctk.CTkTextbox(input_frame, height=300, width=300,wrap=tkinter.WORD)
prompt_textentry.grid(row=1,column=1, padx=10, pady=10)

style_textlabel = ctk.CTkLabel(input_frame, text="Style")
style_textlabel.grid(row=2,column=0, padx=10, pady=10)
style_textdropdown = ctk.CTkComboBox(input_frame, values=["Kendi Gazeteni Yaz", "Kur Farkları", "Ekonomik veriler", "Hava Durumu",], command=update_button_command)
style_textdropdown.grid(row=2, column=1, padx=10, pady=10)

generate_textbutton = ctk.CTkButton(input_frame, text="Generate")
generate_textbutton.grid(row=3, column=0, columnspan=2, sticky="news", padx=10, pady=10)

###########################################################################################

###########################################################################################
# Audio column
transcript = ctk.IntVar()
translate = ctk.IntVar()

voice_to_text_label = ctk.CTkLabel(input_frame, height=33, corner_radius=5, fg_color=("gray95", "gray22"), text="Voice to Text", font=ctk.CTkFont(size=20, weight="bold"))
voice_to_text_label.grid(row=0, column=1, padx=(20, 20), pady=(15, 0), sticky="new")

record_button = ctk.CTkButton(input_frame, width=60, height=60, border_width=8, corner_radius=80, bg_color=("gray85", "gray17"), fg_color="Red", border_color="Red", hover_color="White", text="", command=record_button_event)
record_button.grid(row=0, column=1, padx=(10, 0), pady=(70, 0), sticky="n")

# set default values
transcript.set(1)
recording=False
###########################################################################################

root.mainloop()

