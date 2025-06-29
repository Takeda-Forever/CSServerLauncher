import customtkinter as ctk
import subprocess
import os
import psutil
import socket
from tkinter import filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("640x460")
app.title("🎮 CS2 Local Server Launcher")
app.resizable(False, False)

path = ""
interface_ip_map = {}

# ---------- Функции ----------

def browse_file():
    global path
    folder_path = filedialog.askdirectory()
    if folder_path:
        path_entry_var.set(folder_path)
        path = folder_path
        exe_path = f"{path}/cs2.exe"
        if os.path.exists(exe_path):
            status_label.configure(text="✅ cs2.exe найдено", text_color="green")
        else:
            status_label.configure(text="❌ cs2.exe не найдено", text_color="red")

def on_interface_select(choice):
    ip = interface_ip_map.get(choice, "")
    ip_var.set(ip)

def update_gslt_status(*args):
    key = gslt_entry_var.get().strip()
    if len(key) == 32:
        gslt_status_label.configure(text="✅ Сервер будет запущен с GSLT-ключом", text_color="green")
    elif len(key) == 0:
        gslt_status_label.configure(text="⚠️ Сервер будет запущен в insecure режиме (без GSLT)", text_color="orange")
    else:
        gslt_status_label.configure(text="❌ Неверный GSLT-ключ (должно быть 32 символа)", text_color="red")


def launch_server():
    if not path:
        status_label.configure(text="❌ Путь к cs2.exe не задан", text_color="red")
        return

    ip = ip_var.get()
    gslt = gslt_entry.get()
    selected_map = map_menu.get()

    exe_path = f"{path}/cs2.exe"
    args = [
        exe_path,
        "-dedicated",
        "-maxplayers", "10",
        "-usercon",
        "-console",
        "-dev",
        "+game_type", "0",
        "+game_mode", "1",
        "+map", selected_map
    ]

    if gslt.strip() == "":
        args += ["-insecure", "+sv_lan", "1"]
    else:
        args += ["-secure", "+sv_lan", "0", "+sv_setsteamaccount", gslt]

    try:
        subprocess.Popen(args, shell=True)
        status_label.configure(text="🟢 Сервер запущен", text_color="green")
    except Exception as e:
        status_label.configure(text=f"❌ Ошибка: {e}", text_color="red")

# ---------- Интерфейс ----------

ctk.CTkLabel(app, text="🎮 CS2 Server Launcher", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(10, 5))

# Путь к exe
ctk.CTkLabel(app, text="Путь к папке cs2.exe:").pack(anchor="w", padx=40)
path_frame = ctk.CTkFrame(app)
path_frame.pack(padx=40, fill="x")
path_entry_var = ctk.StringVar()
ctk.CTkEntry(path_frame, textvariable=path_entry_var, width=440).pack(side="left", padx=(0, 10), pady=5, fill="x", expand=True)
ctk.CTkButton(path_frame, text="📁 Browse", command=browse_file).pack(side="left", padx=(0, 10))

# Сетевой интерфейс
ctk.CTkLabel(app, text="Сетевой интерфейс:").pack(anchor="w", padx=40, pady=(10, 0))
net_frame = ctk.CTkFrame(app)
net_frame.pack(padx=40, fill="x")

interface_names = []
for name, addrs in psutil.net_if_addrs().items():
    for addr in addrs:
        if addr.family == socket.AF_INET:
            interface_names.append(name)
            interface_ip_map[name] = addr.address
            break

ip_var = ctk.StringVar()
ctk.CTkEntry(net_frame, textvariable=ip_var, width=240).pack(side="left", padx=(0, 10), pady=5)
interface_menu = ctk.CTkOptionMenu(net_frame, values=interface_names, command=on_interface_select, width=240)
interface_menu.pack(side="left")

if interface_names:
    interface_menu.set(interface_names[0])
    ip_var.set(interface_ip_map[interface_names[0]])

# GSLT
ctk.CTkLabel(app, text="GSLT ключ (можно пусто):").pack(anchor="w", padx=40, pady=(10, 0))
gslt_entry_var = ctk.StringVar()
gslt_entry = ctk.CTkEntry(app, textvariable=gslt_entry_var, placeholder_text="GSLT ключ", width=560)
gslt_entry.pack(padx=40, pady=5)

gslt_status_label = ctk.CTkLabel(app, text="")
gslt_status_label.pack(padx=40, anchor="w")

# Привязка после создания label и переменной
gslt_entry_var.trace_add("write", update_gslt_status)
update_gslt_status()  # чтобы текст появился сразу



# Карты
ctk.CTkLabel(app, text="Выберите карту:").pack(anchor="w", padx=40, pady=(10, 0))
map_menu = ctk.CTkOptionMenu(app, values=["de_mirage", "de_dust2", "de_inferno", "de_nuke", "de_overpass", "cs_office"])
map_menu.pack(padx=40, pady=5)
map_menu.set("de_mirage")

# Запуск
ctk.CTkButton(app, text="🚀 Запустить сервер", command=launch_server, width=200).pack(pady=10)

status_label = ctk.CTkLabel(app, text="")
status_label.pack()

app.mainloop()
