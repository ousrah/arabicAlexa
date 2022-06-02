# ----------------------------------------------------------------
# Arabic Alexa
# By Rahmouni oussama
#----------------------------------------------------------------
# # Youtube : https://www.youtube.com/c/rahmouniOussama
# # Credly :# https://www.credly.com/users/oussama-rahmouni/badges
# # Linked in :# https://www.linkedin.com/in/oussama-rahmouni-bb034624/
# # Instagram :# https://www.instagram.com/ousrah74/
# # Facebook :# https://web.facebook.com/FormationsRahmouni
# # Tiktok : # https://www.tiktok.com/@programinglanguage?lang=en
# # GitHub:# https://github.com/ousrah
# # stackoverflow:# https://stackoverflow.com/users/7415390/rahmouni-oussama
# ----------------------------------------------------------------


from gtts import gTTS
import os
import playsound
import datetime
import speech_recognition as sr
import random
import requests
from bs4 import BeautifulSoup
import pywhatkit
import wikipedia
import pyjokes
from googletrans import Translator, constants



LANG="ar"
wikipedia.set_lang(LANG)  
translator = Translator()

preReponses = [' .حسنا.',' .تحت أمرِكْ.',' .أمركَ مُطاعْ.',' .أوكي',' .أنا مشغولةٌ الآنْ. لكنْ سأجيبكْ.',' .لا أريدُ الإجابةَ على سؤالكْ. لاتقلقْ. فقطْ أمزحُ معكْ.']
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
}

def speak(text):
    tts=gTTS(text=text,lang=LANG)
    tts.save("hello.mp3")
    playsound.playsound("hello.mp3",True)
    os.remove("hello.mp3")

listener = sr.Recognizer()

def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def get_date():
    return datetime.datetime.now().strftime("%A %d/%m/%Y")

def listen():
    try:
        with sr.Microphone() as source:
            print("انا في الاستماع")
            voice=listener.listen(source)
            command=listener.recognize_google(voice, language=LANG)
            if 'اليكسا' in command:
                print(command)
                return command
            else:
                return ""
    except:
        speak("لم أستطع فهم طلبكم")
        


def run():
    v=True
    while v:
        command= listen()
        if not command is None:
            i=random.randint(0,5)
            intro = preReponses[i]
            if 'انهاء' in command:
                v=False
            elif 'ساعه' in command:
                speak(intro + ".الساعة الان هي ." +get_time())
            elif 'تاريخ' in command:
                speak(intro + ".التاريخ الان هو ." +get_date())
            elif 'كيف حالك' in command:
                speak(".بخير الحمد لله .")
            elif 'عنوانك' in command:
                speak(".أنا أسكن في تطوان .") 
            elif 'اخبار' in command:
                URL = "https://www.hespress.com"
                page = requests.get(URL, headers=headers)   
                soup = BeautifulSoup(page.content, 'html.parser')
                l = [a.text for a in soup.select('div li a h3')]
                for a in l:
                    print(a)
                    speak(a)
            elif 'لدي سؤال' in command:
                question = command.replace('لدي سؤال', '')
                question = question.replace('اليكسا', '')
                URL = "https://www.google.co.ma/search?hl="+LANG+"&q=" + question
                page = requests.get(URL, headers=headers)
                soup = BeautifulSoup(page.content, 'html.parser')
                result=""
                try:
                    result=soup.find(class_='HwtpBd gsrt PZPZlf kTOYnf').get_text()
                    speak(result)
                except:
                    pass
            elif 'اغنيه' in command or 'موسيقى' in command or 'سوره' in command or 'صوره' in command:
                command = command.replace('اليكسا', '')   
                speak(intro + " ها هي " + command)         
                pywhatkit.playonyt(command)
            elif   'كلميني عن' in command:   
                command = command.replace('كلميني عن', '')     
                command = command.replace('اليكسا', '')    
                info = wikipedia.summary(command,1)
                speak(info)      
            elif   'نكته' in command:   
                jok = pyjokes.get_joke(language="en",category="neutral")
                print(jok)
                arjok = translator.translate(jok,dest=LANG)
                speak(f'{arjok.text}')
 
   
    speak("مع السلامة")
        
run()