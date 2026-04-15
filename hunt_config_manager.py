import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import re
import os
import sys
import json
import ctypes

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

LANG = {
    "RU": {
        "title": "Конфигуратор Hunt: Showdown",
        "file_frame": " Файл конфигурации (attributes.xml) ",
        "browse": "Обзор...",
        "tab_sens": " Настройка чувствительности ",
        "tab_sys": " Система ",
        "tab_binds": " Управление ",
        "hint": "ЛКМ - назначить кнопку | ПКМ - очистить бинд",
        "warning_binds": "Внимание: Игра может не поддерживать вторую кнопку для некоторых действий.",
        "btn_load": "Обновить из файла",
        "btn_save": "Сохранить настройки в игру",
        "action": "Действие",
        "btn1": "Кнопка 1",
        "btn2": "Кнопка 2",
        "listening": "Нажмите...",
        "empty": "-",
        "msg_success": "Настройки успешно сохранены в файл игры!",
        "msg_no_changes": "Нет изменений для сохранения.",
        "msg_error_bind": "Действие '{action}' не назначено!\nИгра требует хотя бы один бинд.",
        "frame_presets": " Профили настроек ",
        "btn_preset_save": "Сохранить",
        "btn_preset_new": "Создать...",
        "btn_preset_del": "Удалить",
        "prompt_new_preset": "Введите имя нового профиля:",
        "msg_preset_err": "Пожалуйста, введите корректное имя.",
        "msg_preset_del_confirm": "Вы действительно хотите удалить профиль '{name}'?",
        "cat_weapons": "Оружие",
        "cat_tools": "Приспособления",
        "cat_cons": "Расходники",
        "cat_mov": "Передвижение",
        "cat_combat": "Бой и Взаимодействие",
        "cat_vision": "Зрение и Навигация",
        "cat_misc": "Чат и Экипировка",
        "cat_other": "Прочие бинды",
        "slot1": "Слот 1",
        "slot2": "Слот 2",
        "slot3": "Слот 3",
        "slot4": "Слот 4",
        "slot5": "Слот 5",
        "slot6": "Слот 6",
        "slot7": "Слот 7",
        "slot8": "Слот 8",
        "slot9": "Слот 9",
        "slot10": "Слот 10",
        "bandage": "Взаимодействие/Перевязка/Тушение",
        "weaponlight": "Взаимодействие с предметом/оружием",
        "pushtotalk": "Голосовой чат (Команда)",
        "pushtotalk_proximity": "Голосовой чат (Общий)",
        "prevslot": "Предыдущий предмет",
        "nextslot": "Следующий предмет",
        "movement_forward": "Вперед",
        "movement_up": "Вперед",
        "movement_down": "Назад",
        "movement_left": "Влево",
        "movement_right": "Вправо",
        "inspect": "Осмотреть оружие",
        "aim": "Прицел (Удержание)",
        "aimtoggle": "Прицел (Нажатие)",
        "attack": "Стрельба / Атака",
        "darkvision": "Темное зрение",
        "darksight_interact": "Взаимодействие в темном зрении",
        "darksight_boost": "Активировать усиленное темное зрение",
        "meleeattack": "Ближний бой",
        "jump": "Прыжок", 
        "vault": "Паркур (Старый)",
        "navigate": "Перелаз",
        "sprint": "Спринт",
        "crouch": "Присесть",
        "reload": "Перезарядка",
        "interact": "Взаимодействие",
        "map": "Карта",
        "menu": "Меню",
        "pingmarker": "Метка / Пинг",
        "spectatenext": "Наблюдение: След. игрок",
        "spectateprevious": "Наблюдение: Пред. игрок",
        "togglemuteall": "Заглушить всех",
        "togglechat": "Текстовый чат (Команда)",
        "togglechatall": "Текстовый чат (Общий)",
        "weaponnext": "Быстрая смена оружия",
        "MouseSensitivity": "По умолчанию", 
        "HipMouseSensitivity": "От плеча",
        "IronSightsMouseSensitivity": "Режим точного прицеливания", 
        "ShortScopeMouseSensitivity": "Прицел Меткий глаз",
        "MediumScopeMouseSensitivity": "Прицел Опытный стрелок", 
        "LongScopeMouseSensitivity": "Прицел Снайпер",
        "PeepholeMouseSensitivity": "Прицел Линза", 
        "MaxFPS": "Лимит кадров", 
        "OverscanScaling": "Размер интерфейса",
        "btn_yes": "Да",
        "btn_no": "Нет",
        "btn_cancel": "Отмена",
        "title_error": "Ошибка",
        "title_warning": "Внимание",
        "title_info": "Информация"
    },
    "EN": {
        "title": "Hunt: Showdown Config Manager",
        "file_frame": " Configuration File (attributes.xml) ",
        "browse": "Browse...",
        "tab_sens": " Sensitivity ",
        "tab_sys": " System ",
        "tab_binds": " Keybinds ",
        "hint": "LMB - assign key | RMB - clear bind",
        "warning_binds": "Note: The game may not support secondary keybinds for all actions.",
        "btn_load": "Reload from File",
        "btn_save": "Save Settings to Game",
        "action": "Action",
        "btn1": "Key 1",
        "btn2": "Key 2",
        "listening": "Press Key...",
        "empty": "-",
        "msg_success": "Settings saved to game file successfully!",
        "msg_no_changes": "No changes made.",
        "msg_error_bind": "Action '{action}' is unassigned!\nThe game requires at least one key.",
        "frame_presets": " Configuration Profiles ",
        "btn_preset_save": "Save",
        "btn_preset_new": "New...",
        "btn_preset_del": "Delete",
        "prompt_new_preset": "Enter name for new profile:",
        "msg_preset_err": "Please enter a valid name.",
        "msg_preset_del_confirm": "Are you sure you want to delete the profile '{name}'?",
        "cat_weapons": "Weapons", 
        "cat_tools": "Tools", 
        "cat_cons": "Consumables",
        "cat_mov": "Movement",
        "cat_combat": "Combat & Interaction",
        "cat_vision": "Vision & Navigation",
        "cat_misc": "Chat & Equipment",
        "cat_other": "Other Binds",
        "slot1": "Slot 1",
        "slot2": "Slot 2",
        "slot3": "Slot 3",
        "slot4": "Slot 4",
        "slot5": "Slot 5",
        "slot6": "Slot 6",
        "slot7": "Slot 7",
        "slot8": "Slot 8",
        "slot9": "Slot 9",
        "slot10": "Slot 10",
        "bandage": "First Aid Kit / Bleeding",
        "weaponlight": "Interact with Item/Weapon",
        "pushtotalk": "Voice Chat (Party)",
        "pushtotalk_proximity": "Voice Chat (Proximity)",
        "prevslot": "Previous Item",
        "nextslot": "Next Item",
        "movement_forward": "Move Forward",
        "movement_up": "Move Forward",
        "movement_down": "Move Backward",
        "movement_left": "Move Left",
        "movement_right": "Move Right",
        "inspect": "Inspect Item",
        "aim": "Aim Down Sights (Hold)",
        "aimtoggle": "Toggle ADS",
        "attack": "Fire / Attack",
        "darkvision": "Dark Sight",
        "darksight_interact": "Dark Sight Interact",
        "darksight_boost": "Activate Dark Sight Boost",
        "meleeattack": "Melee",
        "jump": "Jump",
        "vault": "Vault (Legacy)",
        "navigate": "Navigate",
        "sprint": "Sprint",
        "crouch": "Crouch",
        "reload": "Reload",
        "interact": "Interact",
        "map": "Map",
        "menu": "Menu",
        "pingmarker": "Ping Marker",
        "spectatenext": "Spectate: Next Player",
        "spectateprevious": "Spectate: Previous Player",
        "togglemuteall": "Toggle Mute All",
        "togglechat": "Text Chat (Party)",
        "togglechatall": "Text Chat (All)",
        "weaponnext": "Next Weapon",
        "MouseSensitivity": "Global Sensitivity",
        "HipMouseSensitivity": "Hip Fire",
        "IronSightsMouseSensitivity": "Iron Sights",
        "ShortScopeMouseSensitivity": "Short Scope",
        "MediumScopeMouseSensitivity": "Medium Scope",
        "LongScopeMouseSensitivity": "Long Scope",
        "PeepholeMouseSensitivity": "Aperture Scope",
        "MaxFPS": "Max FPS",
        "OverscanScaling": "HUD Scaling",
        "btn_yes": "Yes",
        "btn_no": "No",
        "btn_cancel": "Cancel",
        "title_error": "Error",
        "title_warning": "Warning",
        "title_info": "Information"
    }
}

KEYS = {
    "RU": {
        "0": "Esc", "13": "Backspace", "14": "Tab", "27": "Enter", "28": "Л.Ctrl",
        "41": "Л.Shift", "55": "Alt", "56": "Пробел", "57": "CapsLock",
        "199": "Стрелка Вверх", "200": "Стрелка Вверх", "97": "Стрелка Вверх", 
        "207": "Стрелка Вниз", "208": "Стрелка Вниз", "102": "Стрелка Вниз", 
        "202": "Стрелка Влево", "203": "Стрелка Влево", 
        "204": "Стрелка Вправо", "205": "Стрелка Вправо", 
        "210": "Delete",
        "256": "ЛКМ", "257": "ПКМ", "258": "СКМ (Колесо)", "259": "Боковая 1 (M4)", "260": "Боковая 2 (M5)",
        "264": "Колесо Вверх", "265": "Колесо Вниз"
    },
    "EN": {
        "0": "Esc", "13": "Backspace", "14": "Tab", "27": "Enter", "28": "LCtrl",
        "41": "LShift", "55": "Alt", "56": "Space", "57": "CapsLock",
        "199": "Up Arrow", "200": "Up Arrow", "97": "Up Arrow",
        "207": "Down Arrow", "208": "Down Arrow", "102": "Down Arrow",
        "202": "Left Arrow", "203": "Left Arrow",
        "204": "Right Arrow", "205": "Right Arrow",
        "210": "Delete",
        "256": "LMB", "257": "RMB", "258": "MMB", "259": "Mouse 4", "260": "Mouse 5",
        "264": "Wheel Up", "265": "Wheel Down"
    }
}

BASE_KEYS = {
    "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "0",
    "11": "-", "12": "=", "15": "Q", "16": "W", "17": "E", "18": "R", "19": "T", "20": "Y", "21": "U", "22": "I", "23": "O", "24": "P",
    "25": "[", "26": "]", "29": "A", "30": "S", "31": "D", "32": "F", "33": "G", "34": "H", "35": "J", "36": "K", "37": "L", "38": ";",
    "39": "'", "40": "`", "42": "\\", "43": "Z", "44": "X", "45": "C", "46": "V", "47": "B", "48": "N", "49": "M",
    "50": ",", "51": ".", "52": "/", "58": "F1", "59": "F2", "60": "F3", "61": "F4", "62": "F5", "63": "F6", 
    "64": "F7", "65": "F8", "66": "F9", "67": "F10", "86": "F11", "87": "F12",
    "96": "Num 0", "98": "Num 2", "99": "Num 3", "100": "Num 4", "101": "Num 5",
    "103": "Num 7", "104": "Num 8", "105": "Num 9", "106": "Num *",
    "107": "Num +", "109": "Num -", "110": "Num .", "111": "Num /",
    "156": "RCtrl", "183": "RAlt", "198": "Home", "200": "Page Up", "206": "End", "208": "Page Down", "209": "Insert"
}

VK_TO_DIK = {
    "27": "0", "49": "1", "50": "2", "51": "3", "52": "4", "53": "5", "54": "6", "55": "7", "56": "8", "57": "9", "48": "10",
    "189": "11", "187": "12", "8": "13", "9": "14",
    "81": "15", "87": "16", "69": "17", "82": "18", "84": "19", "89": "20", "85": "21", "73": "22", "79": "23", "80": "24",
    "219": "25", "221": "26", "13": "27", "17": "28",
    "65": "29", "83": "30", "68": "31", "70": "32", "71": "33", "72": "34", "74": "35", "75": "36", "76": "37",
    "186": "38", "222": "39", "192": "40", "16": "41",
    "220": "42", "90": "43", "88": "44", "67": "45", "86": "46", "66": "47", "78": "48", "77": "49",
    "188": "50", "190": "51", "191": "52", "106": "54",
    "18": "55", "32": "56", "20": "57",
    "112": "58", "113": "59", "114": "60", "115": "61", "116": "62", "117": "63",
    "118": "64", "119": "65", "120": "66", "121": "67", "144": "68", "145": "69",
    "103": "70", "104": "71", "105": "72", "109": "73",
    "100": "74", "101": "75", "102": "76", "107": "77",
    "97": "78", "98": "79", "99": "80", "96": "81", "110": "82", "111": "111",
    "122": "86", "123": "87",
    "36": "198", "38": "199", "33": "200", "37": "202", "39": "204",
    "35": "206", "40": "207", "34": "208", "45": "209", "46": "210"
}

TK_TO_DIK = {
    "control_l": "28", "control_r": "156", 
    "shift_l": "41", "shift_r": "53", 
    "alt_l": "55", "alt_r": "183"
}

GUI_LAYOUT = [
    ("cat_weapons", [
        ("weaponnext", ["weaponnext"]),
        ("slot1", ["weapon1", "equip1"]),
        ("slot2", ["weapon2", "equip2"])
    ]),
    ("cat_tools", [
        ("slot3", ["item1", "weapon3", "tool1", "equip3"]),
        ("slot4", ["item2", "weapon4", "tool2", "equip4"]),
        ("slot5", ["item3", "weapon5", "tool3", "equip5"]),
        ("slot6", ["item4", "weapon6", "tool4", "equip6"])
    ]),
    ("cat_cons", [
        ("slot7", ["item5", "weapon7", "consumable1", "equip7"]),
        ("slot8", ["item6", "weapon8", "consumable2", "equip8"]),
        ("slot9", ["item7", "weapon9", "consumable3", "equip9"]),
        ("slot10", ["item8", "weapon10", "weapon0", "consumable4", "item10", "item0", "equip10", "equip0"])
    ]),
    ("cat_mov", [
        ("movement_forward", ["movement_forward", "movement_up"]),
        ("movement_down", ["movement_down"]),
        ("movement_left", ["movement_left"]),
        ("movement_right", ["movement_right"]),
        ("jump", ["jump"]),
        ("crouch", ["crouch"]),
        ("sprint", ["sprint"]),
        ("vault", ["vault"]),
        ("navigate", ["navigate"])
    ]),
    ("cat_combat", [
        ("attack", ["attack"]),
        ("aim", ["aim"]),
        ("aimtoggle", ["aimtoggle"]),
        ("reload", ["reload"]),
        ("interact", ["interact"]),
        ("meleeattack", ["meleeattack"]),
        ("inspect", ["inspect"]),
        ("bandage", ["bandage"])
    ]),
    ("cat_vision", [
        ("darkvision", ["darkvision"]),
        ("darksight_boost", ["darksight_boost"]),
        ("darksight_interact", ["darksight_interact"]),
        ("map", ["map"]),
        ("pingmarker", ["pingmarker", "ping", "ping_marker", "marker"])
    ]),
    ("cat_misc", [
        ("pushtotalk", ["pushtotalk", "pushtotalkteam", "voicechat"]),
        ("pushtotalk_proximity", ["pushtotalk_proximity", "pushtotalkcontinuous", "pushtotalkproximity"]),
        ("togglechat", ["togglechat"]),
        ("togglechatall", ["togglechatall", "togglechat_all"]),
        ("togglemuteall", ["togglemuteall", "toggle_mute_all"]),
        ("weaponlight", ["weaponlight"]),
        ("prevslot", ["prevslot"]),
        ("nextslot", ["nextslot"]),
        ("menu", ["menu"]),
        ("spectatenext", ["spectatenext"]),
        ("spectateprevious", ["spectateprevious"])
    ])
]

BLACKLIST = ["ascent", "descent", "togglemode", "axis", "dummy"]

class SensEditorApp:
    def __init__(self, root):
        self.root = root
        
        self.root.withdraw()
        try: self.root.iconbitmap(resource_path("icon.ico"))
        except Exception: pass
        
        self.root.geometry("740x840")
        self.root.resizable(False, False)
        
        self.bg_main = "#0d1117"    
        self.bg_sec = "#161b22"     
        self.bg_entry = "#010409"   
        self.fg_main = "#c9d1d9"    
        self.bg_btn = "#21262d"     
        self.fg_btn = "#c9d1d9"     
        self.bg_btn_act = "#30363d" 
        self.bg_listen = "#1f6feb"  
        self.accent_text = "#58a6ff" 
        self.warning_text = "#d29922"
        self.success_text = "#3fb950"
        self.error_text = "#f85149"
        
        self.font_main = ("Segoe UI", 10)
        self.font_header = ("Segoe UI", 11, "bold")
        self.root.configure(bg=self.bg_main)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.root.option_add('*Listbox.background', self.bg_entry)
        self.root.option_add('*Listbox.foreground', self.fg_main)
        self.root.option_add('*Listbox.selectBackground', self.bg_listen)
        self.root.option_add('*Listbox.selectForeground', '#ffffff')
        self.root.option_add('*TCombobox*Listbox.background', self.bg_entry)
        self.root.option_add('*TCombobox*Listbox.foreground', self.fg_main)
        self.root.option_add('*TCombobox*Listbox.selectBackground', self.bg_listen)
        self.root.option_add('*TCombobox*Listbox.selectForeground', '#ffffff')
        
        self.style.configure(".", font=self.font_main, background=self.bg_main, foreground=self.fg_main)
        self.style.configure("TEntry", fieldbackground=self.bg_entry, foreground=self.fg_main, bordercolor=self.bg_btn, insertcolor=self.fg_main)
        self.style.configure("TNotebook", background=self.bg_main, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.bg_sec, foreground=self.fg_main, borderwidth=0, padding=(18, 10))
        self.style.map("TNotebook.Tab", background=[("selected", self.bg_entry)], foreground=[("selected", self.accent_text)])
        self.style.configure("TLabelframe", background=self.bg_main, foreground=self.fg_main, bordercolor=self.bg_sec)
        self.style.configure("TLabelframe.Label", background=self.bg_main, foreground=self.accent_text, font=self.font_header)
        self.style.configure("TButton", background=self.bg_btn, foreground=self.fg_btn, borderwidth=0, padding=(10, 6))
        self.style.map("TButton", background=[("active", self.bg_btn_act)])
        self.style.configure("TCombobox", fieldbackground=self.bg_entry, background=self.bg_btn, foreground=self.fg_main, arrowcolor=self.fg_main)
        self.style.map("TCombobox", fieldbackground=[("readonly", self.bg_entry)], selectbackground=[("readonly", "focus", self.bg_entry), ("readonly", self.bg_entry)], selectforeground=[("readonly", "focus", self.fg_main), ("readonly", self.fg_main)])
        
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.config_dir = os.path.join(base_dir, "configs")
        os.makedirs(self.config_dir, exist_ok=True)
        self.app_settings_file = os.path.join(self.config_dir, "app_settings.json")

        self.sens_keys = ["MouseSensitivity", "HipMouseSensitivity", "IronSightsMouseSensitivity", "ShortScopeMouseSensitivity", "MediumScopeMouseSensitivity", "LongScopeMouseSensitivity", "PeepholeMouseSensitivity"]
        self.system_keys = ["MaxFPS", "OverscanScaling"]
        
        self.file_path = tk.StringVar()
        self.current_lang = tk.StringVar(value="RU")
        self.preset_var = tk.StringVar()
        
        self.sens_entries = {}
        self.system_entries = {}
        self.current_binds = {}
        self.bind_buttons = {}
        self.current_content = ""
        self.is_listening = False
        
        self.load_app_settings()
        self.create_widgets()
        self.refresh_presets()
        
        if self.file_path.get() and os.path.exists(self.file_path.get()):
            self.load_values()

        self._apply_dark_title_bar()
        self.root.deiconify()

    def _apply_dark_title_bar(self, window=None):
        if window is None: window = self.root
        try:
            window.update()
            hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
            value = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(value), ctypes.sizeof(value))
            ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0027)
        except Exception: pass

    def _center_window(self, window, w, h):
        self.root.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - (h // 2)
        window.geometry(f"{w}x{h}+{x}+{y}")

    def custom_msg_box(self, title_key, message, is_error=False):
        dialog = tk.Toplevel(self.root)
        dialog.withdraw()
        dialog.title(self.tr(title_key))
        self._center_window(dialog, 400, 160)
        dialog.configure(bg=self.bg_main)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        try: dialog.iconbitmap(resource_path("icon.ico"))
        except Exception: pass
        self._apply_dark_title_bar(dialog)

        color = self.error_text if is_error else self.fg_main
        tk.Label(dialog, text=message, bg=self.bg_main, fg=color, font=self.font_main, wraplength=360, justify="center").pack(pady=(25, 15), expand=True)

        btn_frame = tk.Frame(dialog, bg=self.bg_main)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="OK", command=dialog.destroy).pack()

        dialog.deiconify()
        self.root.wait_window(dialog)

    def custom_ask_yes_no(self, title, message):
        dialog = tk.Toplevel(self.root)
        dialog.withdraw()
        dialog.title(title)
        self._center_window(dialog, 400, 160)
        dialog.configure(bg=self.bg_main)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        try: dialog.iconbitmap(resource_path("icon.ico"))
        except Exception: pass
        self._apply_dark_title_bar(dialog)

        tk.Label(dialog, text=message, bg=self.bg_main, fg=self.fg_main, font=self.font_main, wraplength=360, justify="center").pack(pady=(25, 15), expand=True)

        result = [False]
        def on_yes():
            result[0] = True
            dialog.destroy()
        def on_no():
            dialog.destroy()

        dialog.protocol("WM_DELETE_WINDOW", on_no)

        btn_frame = tk.Frame(dialog, bg=self.bg_main)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text=self.tr("btn_yes"), command=on_yes).pack(side="left", padx=10)
        ttk.Button(btn_frame, text=self.tr("btn_no"), command=on_no).pack(side="left", padx=10)

        dialog.deiconify()
        self.root.wait_window(dialog)
        return result[0]

    def custom_ask_string(self, title, prompt):
        dialog = tk.Toplevel(self.root)
        dialog.withdraw()
        dialog.title(title)
        self._center_window(dialog, 380, 160)
        dialog.configure(bg=self.bg_main)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        try: dialog.iconbitmap(resource_path("icon.ico"))
        except Exception: pass
        self._apply_dark_title_bar(dialog)

        tk.Label(dialog, text=prompt, bg=self.bg_main, fg=self.fg_main, font=self.font_main).pack(pady=(20, 10))
        
        entry = ttk.Entry(dialog, width=35)
        entry.pack(pady=5)
        entry.focus_set()

        result = [None]
        def on_ok(event=None):
            val = entry.get().strip()
            if val:
                result[0] = val
                dialog.destroy()
            else:
                dialog.destroy()

        def on_cancel(event=None):
            dialog.destroy()
            
        dialog.protocol("WM_DELETE_WINDOW", on_cancel)

        btn_frame = tk.Frame(dialog, bg=self.bg_main)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="OK", command=on_ok).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=self.tr("btn_cancel"), command=on_cancel).pack(side="left", padx=5)

        dialog.bind("<Return>", on_ok)
        dialog.bind("<Escape>", on_cancel)
        
        dialog.deiconify()
        self.root.wait_window(dialog)
        return result[0]

    def load_app_settings(self):
        if os.path.exists(self.app_settings_file):
            try:
                with open(self.app_settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.file_path.set(data.get("path", ""))
                    self.current_lang.set(data.get("lang", "RU"))
                    self.preset_var.set(data.get("last_preset", ""))
            except: pass

    def save_app_settings(self):
        try:
            with open(self.app_settings_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "path": self.file_path.get(), 
                    "lang": self.current_lang.get(),
                    "last_preset": self.preset_var.get()
                }, f)
        except: pass

    def refresh_presets(self):
        presets = []
        for f in os.listdir(self.config_dir):
            if f.endswith(".json") and f != "app_settings.json":
                presets.append(f[:-5])
        
        self.preset_cb['values'] = presets
        if self.preset_var.get() not in presets and presets:
            self.preset_var.set(presets[0] if presets else "")

    def on_preset_selected(self, event=None):
        self.save_app_settings()
        self.action_load_preset()

    def new_preset(self):
        name = self.custom_ask_string(self.tr("btn_preset_new"), self.tr("prompt_new_preset"))
        if name:
            name = re.sub(r'[\\/*?:"<>|]', "", name).strip()
            if name:
                self.preset_var.set(name)
                self.action_save_preset()
                self.refresh_presets()
            else:
                self.custom_msg_box("title_error", self.tr("msg_preset_err"), True)

    def action_delete_preset(self):
        preset_name = self.preset_var.get()
        if not preset_name: return
        
        if self.custom_ask_yes_no(self.tr("btn_preset_del"), self.tr("msg_preset_del_confirm").format(name=preset_name)):
            path = os.path.join(self.config_dir, f"{preset_name}.json")
            try:
                if os.path.exists(path):
                    os.remove(path)
                self.preset_var.set("")
                self.save_app_settings()
                self.refresh_presets()
            except Exception as e:
                self.custom_msg_box("title_error", str(e), True)

    def action_save_preset(self):
        preset_name = self.preset_var.get()
        if not preset_name:
            self.custom_msg_box("title_warning", self.tr("msg_preset_err"), True)
            return
            
        data = {
            "sens": {k: v.get() for k, v in self.sens_entries.items()},
            "sys": {k: v.get() for k, v in self.system_entries.items()},
            "binds": self.current_binds
        }
        
        path = os.path.join(self.config_dir, f"{preset_name}.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            self.save_app_settings()
            self.refresh_presets()
            
            self.save_status_label.config(text="✓")
            self.root.after(3000, lambda: self.save_status_label.config(text=""))
        except Exception as e:
            self.custom_msg_box("title_error", str(e), True)

    def action_load_preset(self):
        preset_name = self.preset_var.get()
        if not preset_name: return
        
        path = os.path.join(self.config_dir, f"{preset_name}.json")
        if not os.path.exists(path): return
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for k, val in data.get("sens", {}).items():
                if k in self.sens_entries:
                    self.sens_entries[k].delete(0, tk.END)
                    self.sens_entries[k].insert(0, val)
                    
            for k, val in data.get("sys", {}).items():
                if k in self.system_entries:
                    self.system_entries[k].delete(0, tk.END)
                    self.system_entries[k].insert(0, val)
                    
            for raw_action, slots in data.get("binds", {}).items():
                if raw_action in self.current_binds and raw_action in self.bind_buttons:
                    v1 = slots.get("1", "-1")
                    v2 = slots.get("2", "-1")
                    self.current_binds[raw_action]["1"] = v1
                    self.current_binds[raw_action]["2"] = v2
                    self.bind_buttons[raw_action]["btn1"].config(text=self.get_key_name(v1))
                    self.bind_buttons[raw_action]["btn2"].config(text=self.get_key_name(v2))
            
        except Exception as e:
            self.custom_msg_box("title_error", str(e), True)

    def on_lang_change(self, event=None):
        self.save_app_settings()
        for widget in self.root.winfo_children(): widget.destroy()
        self.create_widgets()
        self.refresh_presets()
        if self.file_path.get() and os.path.exists(self.file_path.get()):
            self.load_values()

    def tr(self, key):
        return LANG[self.current_lang.get()].get(key, key)

    def create_widgets(self):
        self.root.title(self.tr("title"))
        
        header_frame = tk.Frame(self.root, bg=self.bg_main)
        header_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        frame_top = ttk.LabelFrame(header_frame, text=self.tr("file_frame"), padding=(15, 10))
        frame_top.pack(side="left", fill="x", expand=True)
        ttk.Entry(frame_top, textvariable=self.file_path, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 15))
        ttk.Button(frame_top, text=self.tr("browse"), command=self.browse_file).pack(side="right")

        lang_cb = ttk.Combobox(header_frame, textvariable=self.current_lang, values=["RU", "EN"], state="readonly", width=5)
        lang_cb.pack(side="right", padx=(15, 0), pady=(10, 0))
        lang_cb.bind("<<ComboboxSelected>>", self.on_lang_change)
        
        preset_frame = ttk.LabelFrame(self.root, text=self.tr("frame_presets"), padding=(15, 10))
        preset_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.preset_cb = ttk.Combobox(preset_frame, textvariable=self.preset_var, state="readonly", width=25)
        self.preset_cb.pack(side="left", padx=(0, 15))
        self.preset_cb.bind("<<ComboboxSelected>>", self.on_preset_selected)
        
        ttk.Button(preset_frame, text=self.tr("btn_preset_new"), command=self.new_preset).pack(side="left", padx=(0, 10))
        ttk.Button(preset_frame, text=self.tr("btn_preset_del"), command=self.action_delete_preset).pack(side="left", padx=(0, 10))
        ttk.Button(preset_frame, text=self.tr("btn_preset_save"), command=self.action_save_preset).pack(side="left")
        
        self.save_status_label = tk.Label(preset_frame, text="", bg=self.bg_main, fg=self.success_text, font=("Segoe UI", 12, "bold"))
        self.save_status_label.pack(side="left", padx=(10, 0))

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=15, pady=5)

        tab_sens = ttk.Frame(notebook, padding=20)
        notebook.add(tab_sens, text=self.tr("tab_sens"))
        for i, key in enumerate(self.sens_keys):
            ttk.Label(tab_sens, text=self.tr(key) + ":").grid(row=i, column=0, sticky="w", pady=12)
            entry = ttk.Entry(tab_sens, width=22)
            entry.grid(row=i, column=1, sticky="e", pady=12, padx=15)
            self.sens_entries[key] = entry
            tab_sens.columnconfigure(1, weight=1)

        tab_sys = ttk.Frame(notebook, padding=20)
        notebook.add(tab_sys, text=self.tr("tab_sys"))
        for i, key in enumerate(self.system_keys):
            ttk.Label(tab_sys, text=self.tr(key) + ":").grid(row=i, column=0, sticky="w", pady=12)
            entry = ttk.Entry(tab_sys, width=22)
            entry.grid(row=i, column=1, sticky="e", pady=12, padx=15)
            self.system_entries[key] = entry
            tab_sys.columnconfigure(1, weight=1)

        tab_binds_container = ttk.Frame(notebook)
        notebook.add(tab_binds_container, text=self.tr("tab_binds"))
        
        self.binds_canvas = tk.Canvas(tab_binds_container, bg=self.bg_main, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab_binds_container, orient="vertical", command=self.binds_canvas.yview)
        self.tab_binds = tk.Frame(self.binds_canvas, bg=self.bg_main, padx=15, pady=15)
        self.tab_binds.bind("<Configure>", lambda e: self.binds_canvas.configure(scrollregion=self.binds_canvas.bbox("all")))
        
        self.canvas_window = self.binds_canvas.create_window((0, 0), window=self.tab_binds, anchor="nw")
        self.binds_canvas.bind("<Configure>", lambda e: self.binds_canvas.itemconfig(self.canvas_window, width=e.width))
        self.binds_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.binds_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            if not getattr(self, "is_listening", False):
                self.binds_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.binds_canvas.bind("<Enter>", lambda e: self.binds_canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.binds_canvas.bind("<Leave>", lambda e: self.binds_canvas.unbind_all("<MouseWheel>"))
        
        tk.Label(self.tab_binds, text=self.tr("hint"), font=("Segoe UI", 9), bg=self.bg_main, fg="#8b949e").grid(row=0, column=0, columnspan=3, pady=(0, 5), sticky="w")
        tk.Label(self.tab_binds, text=self.tr("warning_binds"), font=("Segoe UI", 9, "italic"), bg=self.bg_main, fg=self.warning_text).grid(row=1, column=0, columnspan=3, pady=(0, 15), sticky="w")

        frame_bottom = ttk.Frame(self.root, padding=(15, 15))
        frame_bottom.pack(fill="x")
        ttk.Button(frame_bottom, text=self.tr("btn_load"), command=self.load_values).pack(side="left")
        ttk.Button(frame_bottom, text=self.tr("btn_save"), command=self.save_values).pack(side="right")

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=(("XML", "*.xml"), ("All", "*.*")))
        if path:
            self.file_path.set(path)
            self.save_app_settings()
            self.load_values()

    def get_key_name(self, dik_code):
        if not dik_code or dik_code.startswith("-"): return self.tr("empty")
        lang = self.current_lang.get()
        if dik_code in KEYS[lang]: return KEYS[lang][dik_code]
        if dik_code in BASE_KEYS: return BASE_KEYS[dik_code]
        return f"[{dik_code}]"

    def add_bind_row(self, raw_action, gui_name, val1, val2, row_idx):
        self.current_binds[raw_action] = {"1": val1, "2": val2}
        disp_name = self.tr(gui_name)
        
        tk.Label(self.tab_binds, text=f"{disp_name}:", font=self.font_main, bg=self.bg_main, fg=self.fg_main).grid(row=row_idx, column=0, sticky="w", pady=6)
        
        btn1 = tk.Button(self.tab_binds, text=self.get_key_name(val1), width=22, font=("Segoe UI", 9, "bold"), 
                         bg=self.bg_entry, fg=self.fg_btn, activebackground=self.bg_btn_act, activeforeground="#ffffff", 
                         highlightthickness=1, highlightbackground=self.bg_sec, highlightcolor=self.bg_sec,
                         relief="flat", cursor="hand2", pady=4)
        btn1.grid(row=row_idx, column=1, padx=8, pady=6)
        btn1.config(command=lambda a=raw_action, s="1", b=btn1: self.start_listening(a, s, b))
        btn1.bind("<Button-3>", lambda e, a=raw_action, s="1", b=btn1: self.clear_bind(a, s, b))
        
        btn2 = tk.Button(self.tab_binds, text=self.get_key_name(val2), width=22, font=("Segoe UI", 9, "bold"), 
                         bg=self.bg_entry, fg=self.fg_btn, activebackground=self.bg_btn_act, activeforeground="#ffffff", 
                         highlightthickness=1, highlightbackground=self.bg_sec, highlightcolor=self.bg_sec,
                         relief="flat", cursor="hand2", pady=4)
        btn2.grid(row=row_idx, column=2, padx=8, pady=6)
        btn2.config(command=lambda a=raw_action, s="2", b=btn2: self.start_listening(a, s, b))
        btn2.bind("<Button-3>", lambda e, a=raw_action, s="2", b=btn2: self.clear_bind(a, s, b))
        
        self.bind_buttons[raw_action] = {"btn1": btn1, "btn2": btn2}

    def load_values(self):
        path = self.file_path.get()
        if not path or not os.path.exists(path): return

        try:
            with open(path, 'r', encoding='utf-8') as file:
                self.current_content = file.read()
                
            for key, entry in {**self.sens_entries, **self.system_entries}.items():
                match = re.search(fr'<Attr name="{key}" value="([^"]*)"\s*/>', self.current_content)
                entry.delete(0, tk.END)
                if match: entry.insert(0, match.group(1))

            for widget in self.tab_binds.winfo_children():
                if widget.grid_info().get("row") not in (0, 1): widget.destroy()
            self.current_binds.clear()
            self.bind_buttons.clear()

            row_idx = 2
            
            tk.Label(self.tab_binds, text=self.tr("action"), font=self.font_header, bg=self.bg_main, fg=self.accent_text).grid(row=row_idx, column=0, sticky="w", pady=(10, 15))
            tk.Label(self.tab_binds, text=self.tr("btn1"), font=self.font_header, bg=self.bg_main, fg=self.accent_text).grid(row=row_idx, column=1, padx=8, pady=(10, 15))
            tk.Label(self.tab_binds, text=self.tr("btn2"), font=self.font_header, bg=self.bg_main, fg=self.accent_text).grid(row=row_idx, column=2, padx=8, pady=(10, 15))
            row_idx += 1

            matches = re.finditer(r'<Attr name="PC_([a-zA-Z0-9_]+)_1" value="([^"]*)"\s*/>', self.current_content)
            found_actions = {}
            for match in matches:
                raw_action = match.group(1)
                lower_action = raw_action.lower()
                
                if any(bad in lower_action for bad in BLACKLIST):
                    continue
                    
                val1 = match.group(2)
                v2_match = re.search(fr'<Attr name="PC_{raw_action}_2" value="([^"]*)"\s*/>', self.current_content)
                val2 = v2_match.group(1) if v2_match else ""
                found_actions[lower_action] = {"raw": raw_action, "v1": val1, "v2": val2}

            processed = set()
            
            for cat_key, items in GUI_LAYOUT:
                cat_has_items = False
                
                for gui_name, synonyms in items:
                    best_synonym = None
                    for syn in synonyms:
                        if syn in found_actions:
                            if not best_synonym:
                                best_synonym = syn
                            elif found_actions[syn]["v1"] != "-1" and found_actions[best_synonym]["v1"] == "-1":
                                best_synonym = syn
                                
                    if best_synonym:
                        if not cat_has_items:
                            tk.Label(self.tab_binds, text=self.tr(cat_key), font=self.font_header, bg=self.bg_main, fg="#8b949e").grid(row=row_idx, column=0, columnspan=3, sticky="w", pady=(20, 10))
                            row_idx += 1
                            cat_has_items = True
                            
                        data = found_actions[best_synonym]
                        self.add_bind_row(data["raw"], gui_name, data["v1"], data["v2"], row_idx)
                        row_idx += 1
                        
                        for syn in synonyms:
                            processed.add(syn)      
        except Exception as e:
            self.custom_msg_box("title_error", str(e), True)

    def start_listening(self, action, slot, btn):
        if self.is_listening: return
        self.is_listening = True
        self.l_action, self.l_slot, self.l_btn = action, slot, btn
        
        btn.config(text=self.tr("listening"), bg=self.bg_listen, fg="#ffffff") 
        self.root.after(100, self.bind_events)

    def bind_events(self):
        self.ev_key = self.root.bind("<Key>", self.on_key)
        self.ev_mouse = self.root.bind("<Button>", self.on_mouse)
        self.ev_wheel = self.root.bind("<MouseWheel>", self.on_wheel)
        self.root.focus_set()
        self.check_extra_mouse_buttons()

    def check_extra_mouse_buttons(self):
        if not self.is_listening: return
        try:
            if ctypes.windll.user32.GetAsyncKeyState(0x05) & 0x8000: return self.finish_bind("259")
            if ctypes.windll.user32.GetAsyncKeyState(0x06) & 0x8000: return self.finish_bind("260")
        except: pass
        self.root.after(50, self.check_extra_mouse_buttons)

    def stop_listening(self):
        self.root.unbind("<Key>", self.ev_key)
        self.root.unbind("<Button>", self.ev_mouse)
        self.root.unbind("<MouseWheel>", self.ev_wheel)
        self.l_btn.config(bg=self.bg_entry, fg=self.fg_btn)
        self.is_listening = False

    def finish_bind(self, dik_code):
        self.current_binds[self.l_action][self.l_slot] = dik_code
        self.l_btn.config(text=self.get_key_name(dik_code))
        self.stop_listening()

    def on_key(self, event):
        keycode = str(event.keycode)
        sym = event.keysym.lower()
        
        if sym in ["shift_l", "shift_r", "control_l", "control_r", "alt_l", "alt_r"]:
            dik = TK_TO_DIK.get(sym)
        elif keycode in VK_TO_DIK:
            dik = VK_TO_DIK[keycode]
        else:
            dik = str(event.keycode)
            
        self.finish_bind(dik)
        return "break"

    def on_mouse(self, event):
        num_map = {1: "256", 2: "258", 3: "257"}
        if event.num in num_map: self.finish_bind(num_map[event.num])
        return "break"

    def on_wheel(self, event):
        self.finish_bind("264" if event.delta > 0 else "265")
        return "break"

    def clear_bind(self, action, slot, btn):
        if self.is_listening: return
        self.current_binds[action][slot] = "-1"
        btn.config(text=self.tr("empty"))

    def save_values(self):
        if not self.current_content: return
        new_content = self.current_content
        changes = False

        def replace_or_add(content, key, val):
            pattern = fr'(<Attr name="{key}" value=")([^"]*)("\s*/>)'
            if re.search(pattern, content):
                return re.sub(pattern, fr'\g<1>{val}\g<3>', content), True
            else:
                new_line = f'\n <Attr name="{key}" value="{val}"/>'
                if re.search(r'<Attributes[^>]*>', content):
                    content = re.sub(r'(<Attributes[^>]*>)', fr'\1{new_line}', content, count=1)
                    return content, True
                return content, False

        for key, entry in {**self.sens_entries, **self.system_entries}.items():
            new_content, changed = replace_or_add(new_content, key, entry.get())
            if changed: changes = True

        for raw_action, slots in self.current_binds.items():
            if slots["1"].startswith("-") and slots["2"].startswith("-"):
                msg = self.tr("msg_error_bind").format(action=self.tr(raw_action.lower()))
                self.custom_msg_box("title_error", msg, True)
                return

            new_content, ch1 = replace_or_add(new_content, f"PC_{raw_action}_1", slots["1"])
            new_content, ch2 = replace_or_add(new_content, f"PC_{raw_action}_2", slots["2"])
            if ch1 or ch2: changes = True

        if changes:
            try:
                with open(self.file_path.get(), 'w', encoding='utf-8') as f: f.write(new_content)
                self.current_content = new_content
                self.custom_msg_box("title_info", self.tr("msg_success"))
            except Exception as e: 
                self.custom_msg_box("title_error", str(e), True)
        else: 
            self.custom_msg_box("title_info", self.tr("msg_no_changes"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SensEditorApp(root)
    root.mainloop()