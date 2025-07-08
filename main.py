import requests
from bs4 import BeautifulSoup
import time
from flask import Flask
import threading
import datetime

TOKEN="8113085469:AAHerJW1TKQNsq2sRZ7AGdx_6xIJb_Sodo4"
CHAT_ID="1608045019"

urls=[
    "https://www.sahibinden.com/satilik-daire/trabzon-merkez",
    "https://www.sahibinden.com/satilik-daire/trabzon-akcaabat",
    "https://www.sahibinden.com/satilik-daire/trabzon-besikduzu",
    "https://www.sahibinden.com/satilik-daire/ankara-altindag",
    "https://www.sahibinden.com/satilik-daire/ankara-kecioren",
    "https://www.sahibinden.com/satilik-daire/ankara-mamak",
    "https://www.sahibinden.com/satilik-daire/ankara-etimesgut"
]

duyurulan_ilanlar=set()

def telegram_gonder(mesaj):
    url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload={"chat_id":CHAT_ID,"text":mesaj}
    try:
        requests.post(url,data=payload)
    except Exception as e:
        print("Telegram gönderim hatası:",e)

def ilanlari_kontrol_et():
    print("İlan kontrolü başladı:",datetime.datetime.now())
    for url in urls:
        print("Taranıyor:",url)
        try:
            response=requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
            soup=BeautifulSoup(response.text,"lxml")
            ilanlar=soup.find_all("a",class_="classifiedTitle")
            for ilan in ilanlar:
                link="https://www.sahibinden.com"+ilan.get("href")
                if link not in duyurulan_ilanlar:
                    duyurulan_ilanlar.add(link)
                    telegram_gonder(f"Yeni ilan: {link}")
        except Exception as e:
            print("Hata oluştu:",e)

def zamanlayici():
    while True:
        simdi=datetime.datetime.now()
        hedef=simdi.replace(hour=10,minute=0,second=0,microsecond=0)
        if simdi>=hedef:
            hedef+=datetime.timedelta(days=1)
        bekleme=(hedef-simdi).total_seconds()
        print("Bir sonraki kontrol:",hedef)
        time.sleep(bekleme)
        ilanlari_kontrol_et()

app=Flask(__name__)

@app.route("/")
def home():
    return "Sahibinden takip botu aktif - "+str(datetime.datetime.now())

def zamanlayici_baslat():
    time.sleep(5)
    zamanlayici()

threading.Thread(target=zamanlayici_baslat).start()

if __name__=="__main__":
    telegram_gonder("🔄 Bot yeniden başlatıldı ve çalışıyor.")
    app.run(host="0.0.0.0",port=8080)