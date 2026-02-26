import tkinter as tk
import time

def update_time():
    #format waktu (jam:menit:detik)
    string_time = time.strftime('%H:%M:%S %p')
    label.config(text=string_time) 

    #memperbarui waktu setiap 1000 milidetik (1 detik)
    label.after(1000, update_time)

# membuat jendela utama
root = tk.Tk()
root.title('Jam Digital')

#mengatur tampilan label (font, warna, dll)
label = tk.Label(
    root,
    font=('calibri', 40, 'bold'),
    background='black',
    foreground='grey'
)

#menempatkan label di tengah jendela
label.pack(anchor='center')

#menjalankan fungsi perbarui_waktu
update_time()

#menjalankan aplikasi
root.mainloop()
