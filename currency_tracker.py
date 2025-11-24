import requests
import tkinter as tk
import threading
import time

# Kurları almak için fonksiyonlar
def get_price(symbol):
    try:
        r = requests.get(f"https://open.er-api.com/v6/latest/{symbol}")
        j = r.json()
        return j["rates"]["TRY"]
    except:
        return None

def get_btc():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        btc_usd = float(r.json()["price"])
        usd_try = get_price("USD")
        return btc_usd * usd_try
    except:
        return None

# Arayüz güncelleme fonksiyonu
def update_data():
    while True:
        usd = get_price("USD")
        eur = get_price("EUR")
        btc = get_btc()

        usd_label.config(text=f"USD: {usd:.2f} TL" if usd else "USD alınamadı")
        eur_label.config(text=f"EUR: {eur:.2f} TL" if eur else "EUR alınamadı")
        btc_label.config(text=f"BTC: {btc:,.2f} TL" if btc else "BTC alınamadı")

        time_label.config(text=f"Güncelleme: {time.strftime('%H:%M:%S')}")
        time.sleep(1)

# Tkinter arayüzü
root = tk.Tk()
root.title("Kur Takip")
root.configure(bg="#1e1e1e")  # koyu arka plan
root.geometry("300x180")

# Label renkleri ve fontları
label_font = ("Helvetica", 14, "bold")
text_color = "#ffffff"

usd_label = tk.Label(root, text="USD: ...", font=label_font, fg=text_color, bg="#1e1e1e")
usd_label.pack(pady=6)

eur_label = tk.Label(root, text="EUR: ...", font=label_font, fg=text_color, bg="#1e1e1e")
eur_label.pack(pady=6)

btc_label = tk.Label(root, text="BTC: ...", font=label_font, fg=text_color, bg="#1e1e1e")
btc_label.pack(pady=6)

time_label = tk.Label(root, text="Güncelleme: ...", font=("Helvetica", 10), fg="#bbbbbb", bg="#1e1e1e")
time_label.pack(pady=6)

# Arka planda veri güncelleme thread'i
t = threading.Thread(target=update_data)
t.daemon = True
t.start()

root.mainloop()
