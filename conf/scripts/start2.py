import customtkinter as ctk
import time
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def execute_command(option):
    if option == "Secret.me":
        subprocess.Popen(["python", "./conf/scripts/Linsta.pyw"]) 
        root.destroy() 

def animate_window(root, target_width, target_height):
    width, height = 100, 50
    while width < target_width or height < target_height:
        width = min(width + 10, target_width)
        height = min(height + 5, target_height)
        root.geometry(f"{width}x{height}")
        root.update()
        time.sleep(0.01)

def create_gui():
    global root
    root = ctk.CTk()
    target_width, target_height = 600, 400
    root.geometry("100x50")
    root.title("Menu")

    root.resizable(False, False)  
    root.bind('<F11>', lambda e: 'break')  # Desativa F11
    animate_window(root, target_width, target_height)
    
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
    title = ctk.CTkLabel(frame, text="Menu", font=("Arial", 24))
    title.pack(pady=(20, 10))

    button1 = ctk.CTkButton(frame, text="Secret.me", command=lambda: execute_command("Secret.me"), hover_color="#550000", text_color="white", corner_radius=10)
    button1.pack(pady=10)

    footer = ctk.CTkLabel(frame, text="© 2024 Lalaio1", font=("Arial", 10))
    footer.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
