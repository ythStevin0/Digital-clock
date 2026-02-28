import tkinter as tk
import time
import customtkinter as ctk

# 1. Variabel dan Fungsi Logika
is_24 = True

def toggle_format():
    """Mengganti format antara 24 jam dan 12 jam (AM/PM)"""
    global is_24
    is_24 = not is_24
    update_time()

def update_time():
    """Fungsi rekursif untuk memperbarui teks jam, sapaan, dan tanggal setiap detik"""
    # 1. Update Jam
    if is_24:
        string_time = time.strftime('%H:%M:%S')
    else:
        string_time = time.strftime('%I:%M:%S %p')
    
    label_time.config(text=string_time) 

    # 2. Update Sapaan (Greeting)
    hour = int(time.strftime('%H'))
    if 5 <= hour < 11:
        greeting = "Selamat Pagi 🌅"
    elif 11 <= hour < 15:
        greeting = "Selamat Siang ☀️"
    elif 15 <= hour < 18:
        greeting = "Selamat Sore 🌤️"
    else:
        greeting = "Selamat Malam 🌙"
    
    label_greeting.config(text=greeting)

    # 3. Update Tanggal
    string_date = time.strftime('%A, %d %B %Y')
    label_date.config(text=string_date)

    # Memperbarui label_time setiap 1 detik
    label_time.after(1000, update_time)

# 2. Pengaturan Jendela Utama
root = tk.Tk()
root.title('Jam Digital')
root.config(bg='#061E29')

# 2.0 Mengatur agar jendela muncul di tengah layar
root.update_idletasks()
width = 600
height = 300
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

# 2.1 Bind tombol Escape untuk menutup aplikasi
root.bind('<Escape>', lambda e: root.destroy())

# 3. Membuat Frame (Wadah) untuk Jam dan Tombol agar Sejajar
# Menggunakan Frame agar widget di dalamnya bisa berjejer horizontal (side='left')
frame_jam = tk.Frame(root, bg='#061E29')
frame_jam.pack(pady=(30, 0)) # Memberi jarak dari atas jendela

# 4. Membuat Widget di dalam Frame (Susunan Kiri ke Kanan)
label_time = tk.Label(
    frame_jam,
    font=('verdana', 55, 'bold'),
    background='#061E29',
    foreground='#5F9598'
)
label_time.pack(side='left', padx=10) # Berada di kiri dalam frame

btn_toggle = ctk.CTkButton(
    frame_jam,
    text="12/24h", # Teks dipersingkat agar tidak terlalu lebar
    command=toggle_format,
    width=60,
    height=30,
    font=('verdana', 10, 'bold'),
    fg_color='#5F9598',
    text_color='#061E29',
    hover_color='#1D546D',
    corner_radius=20
)
btn_toggle.pack(side='left', padx=10) # Berada di sebelah kanan jam

# 5. Membuat Widget Sapaan (Di bawah Jam)
label_greeting = tk.Label(
    root,
    font=('verdana', 15, 'italic'),
    background='#061E29',
    foreground='#5F9598'
)
label_greeting.pack(pady=(5, 0))

# 6. Membuat Widget Tanggal (Di bawah Sapaan)
label_date = tk.Label(
    root,
    font=('verdana', 25, 'bold'),
    background='#061E29',
    foreground='#F3F4F4'
)
label_date.pack(pady=(10, 30)) # Berada di bawah label_greeting

# 6. Menjalankan Aplikasi
update_time()
root.mainloop()
