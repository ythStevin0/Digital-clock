import os
import time
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

# 1. Variabel dan Konfigurasi
is_24 = True
NOTES_FILE = "notes.txt"

# State autosave catatan
autosave_job = None
save_status_job = None

# State stopwatch
stopwatch_running = False
stopwatch_elapsed_seconds = 0
stopwatch_job = None
stopwatch_lap_count = 0

# State alarm
alarm_enabled = False
alarm_time = ""
alarm_last_triggered = ""


def toggle_format():
    """Mengganti format antara 24 jam dan 12 jam (AM/PM)."""
    global is_24
    is_24 = not is_24
    update_time()


def update_time():
    """Memperbarui teks jam, sapaan, dan tanggal setiap detik."""
    if is_24:
        string_time = time.strftime("%H:%M:%S")
    else:
        string_time = time.strftime("%I:%M:%S %p")

    label_time.config(text=string_time)

    hour = int(time.strftime("%H"))
    if 5 <= hour < 11:
        greeting = "Selamat Pagi"
    elif 11 <= hour < 15:
        greeting = "Selamat Siang"
    elif 15 <= hour < 18:
        greeting = "Selamat Sore"
    else:
        greeting = "Selamat Malam"

    label_greeting.config(text=greeting)

    string_date = time.strftime("%A, %d %B %Y")
    label_date.config(text=string_date)

    check_alarm()
    label_time.after(1000, update_time)


def check_alarm():
    """Memeriksa alarm setiap detik dan menampilkan popup saat cocok."""
    global alarm_last_triggered
    if not alarm_enabled or not alarm_time:
        return

    now_hm = time.strftime("%H:%M")
    current_minute_key = time.strftime("%Y-%m-%d %H:%M")
    if now_hm == alarm_time and alarm_last_triggered != current_minute_key:
        alarm_last_triggered = current_minute_key
        messagebox.showinfo("Alarm", f"Waktunya: {alarm_time}")


# ---------- Fitur Catatan Otomatis ----------
def save_note_to_file():
    """Menyimpan isi catatan ke file notes.txt."""
    content = text_note.get("1.0", "end-1c")
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    show_save_status("Tersimpan")


def load_note_from_file():
    """Memuat isi catatan dari file jika ada."""
    if not os.path.exists(NOTES_FILE):
        text_note.insert("1.0", "...")
        return

    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    text_note.insert("1.0", content if content else "...")


def schedule_autosave(_event=None):
    """Menjadwalkan simpan catatan otomatis (debounce)."""
    global autosave_job
    if autosave_job is not None:
        root.after_cancel(autosave_job)
    show_save_status("Menyimpan...")
    autosave_job = root.after(600, save_note_to_file)


def show_save_status(message):
    """Menampilkan status simpan singkat di bawah catatan."""
    global save_status_job
    label_save_status.config(text=message)
    if save_status_job is not None:
        root.after_cancel(save_status_job)
    if message == "Tersimpan":
        save_status_job = root.after(1500, lambda: label_save_status.config(text=""))


def clear_note():
    text_note.delete("1.0", "end")
    save_note_to_file()


# ---------- Fitur Stopwatch ----------
def format_stopwatch(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def update_stopwatch_label():
    label_stopwatch.config(text=format_stopwatch(stopwatch_elapsed_seconds))


def run_stopwatch_tick():
    global stopwatch_elapsed_seconds, stopwatch_job
    stopwatch_elapsed_seconds += 1
    update_stopwatch_label()
    stopwatch_job = root.after(1000, run_stopwatch_tick)


def start_stopwatch():
    global stopwatch_running, stopwatch_job
    if stopwatch_running:
        return
    stopwatch_running = True
    stopwatch_job = root.after(1000, run_stopwatch_tick)


def pause_stopwatch():
    global stopwatch_running, stopwatch_job
    stopwatch_running = False
    if stopwatch_job is not None:
        root.after_cancel(stopwatch_job)
        stopwatch_job = None


def reset_stopwatch():
    global stopwatch_elapsed_seconds
    pause_stopwatch()
    stopwatch_elapsed_seconds = 0
    update_stopwatch_label()
    clear_laps()


def add_lap():
    global stopwatch_lap_count
    if stopwatch_elapsed_seconds == 0:
        return
    stopwatch_lap_count += 1
    lap_text = f"Lap {stopwatch_lap_count}: {format_stopwatch(stopwatch_elapsed_seconds)}"
    listbox_laps.insert("end", lap_text)


def clear_laps():
    global stopwatch_lap_count
    stopwatch_lap_count = 0
    listbox_laps.delete(0, "end")


def on_close():
    """Simpan catatan saat aplikasi ditutup."""
    save_note_to_file()
    root.destroy()


def set_alarm():
    """Menyetel alarm dalam format HH:MM (24 jam)."""
    global alarm_enabled, alarm_time
    hh = entry_alarm_hour.get().strip()
    mm = entry_alarm_minute.get().strip()

    if not (hh.isdigit() and mm.isdigit()):
        label_alarm_status.config(text="Format harus angka")
        return

    hour = int(hh)
    minute = int(mm)
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        label_alarm_status.config(text="Jam 00-23, menit 00-59")
        return

    alarm_time = f"{hour:02d}:{minute:02d}"
    alarm_enabled = True
    label_alarm_status.config(text=f"Alarm aktif: {alarm_time}")


def cancel_alarm():
    global alarm_enabled, alarm_time
    alarm_enabled = False
    alarm_time = ""
    label_alarm_status.config(text="Alarm mati")


# 2. Pengaturan Jendela Utama
root = tk.Tk()
root.title("Jam Digital")
root.config(bg="#061E29")

# 2.0 Mengatur agar jendela muncul di tengah layar
root.update_idletasks()
width = 600
height = 640
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")

# 2.1 Bind close behavior
root.bind("<Escape>", lambda _e: on_close())
root.bind("<Control-s>", lambda _e: save_note_to_file())
root.protocol("WM_DELETE_WINDOW", on_close)

# 3. Frame untuk jam + tombol format
frame_jam = tk.Frame(root, bg="#061E29")
frame_jam.pack(pady=(30, 0))

label_time = tk.Label(
    frame_jam,
    font=("verdana", 55, "bold"),
    background="#061E29",
    foreground="#5F9598",
)
label_time.pack(side="left", padx=10)

btn_toggle = ctk.CTkButton(
    frame_jam,
    text="12/24h",
    command=toggle_format,
    width=60,
    height=30,
    font=("verdana", 10, "bold"),
    fg_color="#5F9598",
    text_color="#061E29",
    hover_color="#1D546D",
    corner_radius=20,
)
btn_toggle.pack(side="left", padx=10)

# 4. Sapaan dan tanggal
label_greeting = tk.Label(
    root,
    font=("verdana", 15, "italic"),
    background="#061E29",
    foreground="#5F9598",
)
label_greeting.pack(pady=(5, 0))

label_date = tk.Label(
    root,
    font=("verdana", 25, "bold"),
    background="#061E29",
    foreground="#F3F4F4",
)
label_date.pack(pady=(10, 20))

# 5. Bagian stopwatch
label_stopwatch_head = tk.Label(
    root,
    text="Stopwatch",
    font=("verdana", 12, "bold"),
    background="#061E29",
    foreground="#F3F4F4",
)
label_stopwatch_head.pack(pady=(0, 5))

label_stopwatch = tk.Label(
    root,
    text="00:00:00",
    font=("verdana", 28, "bold"),
    background="#061E29",
    foreground="#F3F4F4",
)
label_stopwatch.pack()

frame_stopwatch_btn = tk.Frame(root, bg="#061E29")
frame_stopwatch_btn.pack(pady=(8, 18))

btn_start = ctk.CTkButton(
    frame_stopwatch_btn,
    text="Start",
    command=start_stopwatch,
    width=80,
    height=30,
)
btn_start.pack(side="left", padx=5)

btn_pause = ctk.CTkButton(
    frame_stopwatch_btn,
    text="Pause",
    command=pause_stopwatch,
    width=80,
    height=30,
)
btn_pause.pack(side="left", padx=5)

btn_reset = ctk.CTkButton(
    frame_stopwatch_btn,
    text="Reset",
    command=reset_stopwatch,
    width=80,
    height=30,
)
btn_reset.pack(side="left", padx=5)

btn_lap = ctk.CTkButton(
    frame_stopwatch_btn,
    text="Lap",
    command=add_lap,
    width=80,
    height=30,
)
btn_lap.pack(side="left", padx=5)

listbox_laps = tk.Listbox(
    root,
    height=4,
    width=30,
    font=("verdana", 9),
    background="#0A2B39",
    foreground="#F3F4F4",
    border=0,
    highlightthickness=0,
)
listbox_laps.pack(pady=(0, 16))

# 6. Bagian alarm
frame_alarm = tk.Frame(root, bg="#061E29")
frame_alarm.pack(pady=(0, 16))

label_alarm_head = tk.Label(
    frame_alarm,
    text="Alarm (24h):",
    font=("verdana", 10, "bold"),
    background="#061E29",
    foreground="#F3F4F4",
)
label_alarm_head.pack(side="left", padx=(0, 8))

entry_alarm_hour = tk.Entry(
    frame_alarm,
    width=3,
    font=("verdana", 10),
    justify="center",
)
entry_alarm_hour.pack(side="left")

label_colon = tk.Label(
    frame_alarm,
    text=":",
    font=("verdana", 10, "bold"),
    background="#061E29",
    foreground="#F3F4F4",
)
label_colon.pack(side="left", padx=4)

entry_alarm_minute = tk.Entry(
    frame_alarm,
    width=3,
    font=("verdana", 10),
    justify="center",
)
entry_alarm_minute.pack(side="left")

btn_set_alarm = ctk.CTkButton(
    frame_alarm,
    text="Set",
    command=set_alarm,
    width=60,
    height=30,
)
btn_set_alarm.pack(side="left", padx=6)

btn_cancel_alarm = ctk.CTkButton(
    frame_alarm,
    text="Cancel",
    command=cancel_alarm,
    width=70,
    height=30,
)
btn_cancel_alarm.pack(side="left")

label_alarm_status = tk.Label(
    root,
    text="Alarm mati",
    font=("verdana", 9, "italic"),
    background="#061E29",
    foreground="#5F9598",
)
label_alarm_status.pack(pady=(0, 10))

# 7. Bagian catatan
label_note_head = tk.Label(
    root,
    text="Catatan Hari Ini:",
    font=("verdana", 10, "bold"),
    background="#061E29",
    foreground="#F3F4F4",
)
label_note_head.pack(pady=(8, 0))

text_note = tk.Text(
    root,
    height=5,
    width=45,
    font=("verdana", 10),
    background="#061E29",
    foreground="white",
    insertbackground="white",
    padx=15,
    pady=15,
    border=0,
)
text_note.pack(pady=(10, 30), padx=20)

frame_note_btn = tk.Frame(root, bg="#061E29")
frame_note_btn.pack(pady=(0, 6))

btn_save_note = ctk.CTkButton(
    frame_note_btn,
    text="Save",
    command=save_note_to_file,
    width=80,
    height=30,
)
btn_save_note.pack(side="left", padx=5)

btn_clear_note = ctk.CTkButton(
    frame_note_btn,
    text="Clear",
    command=clear_note,
    width=80,
    height=30,
)
btn_clear_note.pack(side="left", padx=5)

label_save_status = tk.Label(
    root,
    text="",
    font=("verdana", 9, "italic"),
    background="#061E29",
    foreground="#5F9598",
)
label_save_status.pack(pady=(0, 18))

# Muat catatan awal dan aktifkan autosave
load_note_from_file()
text_note.bind("<KeyRelease>", schedule_autosave)

# 8. Menjalankan aplikasi
update_time()
update_stopwatch_label()
root.mainloop()
