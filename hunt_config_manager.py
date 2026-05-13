import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import re
import os
import sys
import json
import ctypes
import math

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

    def show_tip(self):
        if self.tip_window or not self.text: return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left",
                         background="#1c2128", foreground="#c9d1d9",
                         relief="solid", borderwidth=1,
                         font=("Segoe UI", 9), padx=10, pady=5, wraplength=400)
        label.pack()

    def hide_tip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

def create_tooltip(widget, text):
    tooltip = ToolTip(widget, text)
    widget.bind("<Enter>", lambda e: tooltip.show_tip())
    widget.bind("<Leave>", lambda e: tooltip.hide_tip())

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
        "btn_preset_apply": "Применить",
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
        "title_info": "Информация",
        "calc_tab": " Калькулятор 1:1 ",
        "calc_import_frame": " Импорт из других игр ",
        "calc_game_label": "Игра:",
        "calc_sens_label": "Чувствительность:",
        "calc_params_frame": " Параметры Hunt: Showdown ",
        "calc_base_sens_label": "Базовая чувствительность (Default):",
        "calc_fov_label": "Угол обзора:",
        "btn_calculate": "Рассчитать и перенести в настройки",
        "calc_notice": "* Значения будут рассчитаны и перенесены во вкладку 'Настройка чувствительности'",
        "sys_fov_frame": " Угол обзора ",
        "sys_menu_label": "В Игровом меню (79.32 - 112.33):",
        "sys_config_label": "В файле attributes.xml (50 - 80):",
        "sys_other_frame": " Прочие параметры ",
        "calc_fov_mode": "Тип ввода угла обзора:",
        "calc_mode_hfov": "Из игры ",
        "calc_mode_vfov": "Из файла attributes.xml",
        "opt_default": "По умолчанию",
        "opt_zoom": "Приближение",
        "calc_lowered_label": "Поле зрения в опущенном состоянии:",
        "calc_shoulder_label": "Поле зрения прицеливания от плеча:",
        "calc_mdc_tooltip": "Чувствительность при разных FOV никогда не может быть абсолютно одинаковой: MDC позволяет выбрать конкретную точку на экране, где движение мыши будет совпадать. Обычно выбирают от 0% (центр) до 100% (край экрана), но технически можно ставить значения выше или даже отрицательные.",
        "calc_mdc_label": "Коэф. дистанции монитора (MDC %):",
        "sys_fov_tooltip": "Игра скрыто преобразует заданный вами горизонтальный угол обзора (FOV) в вертикальный FOV, адаптированный под соотношение сторон 16:9. Например, горизонтальный FOV 85° соответствует вертикальному FOV ~55°.\n\nВсе внутренние расчеты Hunt: Showdown опираются именно на этот вертикальный FOV.\n\nВы можете вручную задать вертикальный FOV, изменив параметр FieldOfView в файле attributes.xml (доступны значения от 50 до 80). В этой программе отображаются ваши актуальные значения, и вы можете изменять их прямо здесь.\n\nЕсли вы меняете FOV через файл, редактируйте именно это значение, а не горизонтальный FOV.\n\nРучная настройка позволяет расширить границы горизонтального FOV до 79°–112° (вместо стандартных 85°–110° в меню игры).\n\nИгровые настройки могут вводить в заблуждение: горизонтальный FOV, который вы выбираете в меню, не всегда совпадает с реальным углом обзора в игре.\n\nОбратите внимание: игра всегда округляет значение в файле attributes.xml при запуске, если для файла не установлен атрибут «Только чтение».",
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
        "btn_preset_apply": "Apply",
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
        "title_info": "Information",
        "calc_tab": " 1:1 Calculator ",
        "calc_import_frame": " Import from other games ",
        "calc_game_label": "Game:",
        "calc_sens_label": "Sensitivity:",
        "calc_params_frame": " Hunt: Showdown Parameters ",
        "calc_base_sens_label": "Base Sensitivity (Default):",
        "calc_fov_label": "Field of View:",
        "btn_calculate": "Calculate and transfer to settings",
        "calc_notice": "* Values will be calculated and transferred to the 'Sensitivity' tab",
        "sys_fov_frame": " Field Of View ",
        "sys_menu_label": "In-game menu (79.32 - 112.33):",
        "sys_config_label": "File attributes.xml (50 - 80):",
        "sys_other_frame": " Other parameters ",
        "calc_fov_mode": "FOV Input Type:",
        "calc_mode_hfov": "From game menu",
        "calc_mode_vfov": "From file attributes.xml",
        "opt_default": "Default",
        "opt_zoom": "Zoom",
        "calc_lowered_label": "Lowered State FOV:",
        "calc_shoulder_label": "Shoulder Aim FOV:",
        "calc_mdc_tooltip": "Sensitivities across different FOVs can never truly be equal: the Monitor Distance Coefficient allows to choose the specific point on the screen where mouse movement will match across FOVs. Generally you'll want to pick a value between 0% (center of the screen) and 100% (edge of the screen) but you can technically pick higher values or even negative values.",
        "calc_mdc_label": "Monitor Distance Coeff (MDC %):",
        "sys_fov_tooltip": "The game implicitly converts your configured horizontal FOV into a vertical FOV adapted for a 16:9 aspect ratio. For example, a horizontal FOV of 85° corresponds to a vertical FOV of ~55°.\n\nHunt: Showdown bases all its internal calculations on this vertical FOV.\n\nYou can manually set the vertical FOV by changing the FieldOfView parameter in the attributes.xml file (values from 50 to 80 are allowed). This program displays your actual values, and you can modify them directly here.\n\nIf you modify the FOV through the file, edit this value, not the horizontal FOV.\n\nManual configuration extends the horizontal FOV limits to 79°–112° (instead of the standard 85°–110° in the game menu).\n\nIn-game settings can be misleading: the horizontal FOV you select in the menu does not always match the actual field of view rendered in-game.\n\nPlease note: the game will always round the value in the attributes.xml file upon launch unless the file is set to \"Read-only\".",
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
        
        self.HIDDEN_FACTORS = {
            "MouseSensitivity": 1.000000,
            "HipMouseSensitivity": 1.111111,
            "IronSightsMouseSensitivity": 1.851851,
            "ShortScopeMouseSensitivity": 2.020202,
            "MediumScopeMouseSensitivity": 5.555556,
            "LongScopeMouseSensitivity": 3.703704,
            "PeepholeMouseSensitivity": 5.555556
        }

        self.load_app_settings()

        self.calc_base_sens = tk.StringVar()
        self.calc_fov = tk.StringVar()
        self.calc_mdc = tk.StringVar()
        
        self.calc_fov_mode = tk.StringVar(value=self.tr("calc_mode_hfov"))
        self.calc_fov_mode.trace_add("write", self.recalculate_sens)
        
        self.games_file = os.path.join(self.config_dir, "games_sens.json")

        self.sys_fov_ingame = tk.StringVar()
        self.sys_fov_config = tk.StringVar()
        self._fov_updating = False 
        
        self.sys_fov_ingame.trace_add("write", self._on_ingame_fov_change)
        self.sys_fov_config.trace_add("write", self._on_config_fov_change)
        
        self.games_data = {
            "CS2 / Apex Legends": 0.5119635,
            "Valorant": 1.6289741215,
            "Overwatch 2 / Call of Duty": 0.153589498,
            "Rainbow Six Siege (Default)": 0.104719
        }
        
        if os.path.exists(self.games_file):
            try:
                with open(self.games_file, 'r', encoding='utf-8') as f:
                    self.games_data = json.load(f)
            except: pass
        else:
            try:
                with open(self.games_file, 'w', encoding='utf-8') as f:
                    json.dump(self.games_data, f, indent=4, ensure_ascii=False)
            except: pass

        self.conv_game = tk.StringVar(value=list(self.games_data.keys())[0])
        self.conv_sens = tk.StringVar()

        self.conv_game.trace_add("write", self.convert_external_sens)
        self.conv_sens.trace_add("write", self.convert_external_sens)

        self.calc_lowered_fov = tk.StringVar(value=self.tr("opt_default"))
        self.calc_shoulder_fov = tk.StringVar(value=self.tr("opt_default"))

        self.calc_base_sens.trace_add("write", self.recalculate_sens)
        self.calc_fov.trace_add("write", self.recalculate_sens)
        self.calc_mdc.trace_add("write", self.recalculate_sens)
        self.calc_lowered_fov.trace_add("write", self.recalculate_sens)
        self.calc_shoulder_fov.trace_add("write", self.recalculate_sens)
        
        self.create_widgets()
        self.refresh_presets()
        
        if self.file_path.get() and os.path.exists(self.file_path.get()):
            self.load_values()

        self._apply_dark_title_bar()
        self.root.deiconify()

    def recalculate_sens(self, *args):
        try:
            base_sens_str = self.calc_base_sens.get().replace(',', '.').strip()
            fov_str = self.calc_fov.get().replace(',', '.').strip()
            mdc_str = self.calc_mdc.get().replace('%', '').replace(',', '.').strip()
            
            if not base_sens_str or not fov_str or not mdc_str: return
                
            base_sens = float(base_sens_str)
            fov_val = float(fov_str)
            mdc = float(mdc_str) / 100.0  
            
            if self.calc_fov_mode.get() == self.tr("calc_mode_hfov"):
                base_vfov = math.degrees(2 * math.atan(math.tan(math.radians(fov_val) / 2) / (16.0 / 9.0)))
            else:
                base_vfov = fov_val
            
            lowered_vfov = base_vfov if self.calc_lowered_fov.get() == self.tr("opt_default") else base_vfov / 1.25
            shoulder_vfov = base_vfov if self.calc_shoulder_fov.get() == self.tr("opt_default") else base_vfov / 1.25
            
            scope_vfovs = {
                "MouseSensitivity": lowered_vfov,
                "HipMouseSensitivity": shoulder_vfov,
                "IronSightsMouseSensitivity": base_vfov * 0.48,
                "ShortScopeMouseSensitivity": math.degrees(2 * math.atan(math.tan(math.radians(55) / 2) / 3.0)),
                "MediumScopeMouseSensitivity": math.degrees(2 * math.atan(math.tan(math.radians(55) / 2) / 8.0)),
                "LongScopeMouseSensitivity": math.degrees(2 * math.atan(math.tan(math.radians(55) / 2) / 12.0)),
                "PeepholeMouseSensitivity": math.degrees(2 * math.atan(math.tan(math.radians(55) / 2) / 9.0))
            }
            
            for key in self.sens_keys:
                hidden_factor = self.HIDDEN_FACTORS.get(key, 1.0)
                target_vfov = scope_vfovs[key]
                
                if mdc == 0.0:
                    ratio = math.tan(math.radians(target_vfov) / 2) / math.tan(math.radians(base_vfov) / 2)
                else:
                    ratio = math.atan(mdc * math.tan(math.radians(target_vfov) / 2)) / math.atan(mdc * math.tan(math.radians(base_vfov) / 2))
                    
                final_val = base_sens * hidden_factor * ratio
                
                if key in self.sens_entries:
                    self.sens_entries[key].delete(0, tk.END)
                    self.sens_entries[key].insert(0, f"{final_val:.6f}")
                    
        except ValueError:
            pass
            
    def convert_external_sens(self, *args):
        try:
            game = self.conv_game.get()
            sens_str = self.conv_sens.get().replace(',', '.').strip()
            
            if not sens_str or game not in self.games_data:
                return
                
            ext_sens = float(sens_str)
            multiplier = self.games_data[game]
            
            hunt_base_sens = ext_sens * multiplier
            
            self.calc_base_sens.set(f"{hunt_base_sens:.6f}".rstrip('0').rstrip('.'))
            
        except ValueError:
            pass
            
    def _on_ingame_fov_change(self, *args):
        if self._fov_updating: return 
        try:
            val_str = self.sys_fov_ingame.get().replace(',', '.').strip()
            if not val_str: return
            fov_in = float(val_str)
            
            if fov_in > 112.33:
                fov_in = 112.33
                self._fov_updating = True
                self.sys_fov_ingame.set("112.33")
                self._fov_updating = False
            
            vfov = math.degrees(2 * math.atan(math.tan(math.radians(fov_in) / 2) / (16.0 / 9.0)))
            
            self._fov_updating = True
            self.sys_fov_config.set(f"{vfov:.6f}".rstrip('0').rstrip('.'))
            self._fov_updating = False
        except ValueError:
            pass

    def _on_config_fov_change(self, *args):
        if self._fov_updating: return
        try:
            val_str = self.sys_fov_config.get().replace(',', '.').strip()
            if not val_str: return
            vfov = float(val_str)
            
            if vfov > 80.0:
                vfov = 80.0
                self._fov_updating = True
                self.sys_fov_config.set("80")
                self._fov_updating = False
            
            hfov = math.degrees(2 * math.atan(math.tan(math.radians(vfov) / 2) * (16.0 / 9.0)))
            
            self._fov_updating = True
            hfov_clean = f"{hfov:.2f}".rstrip('0').rstrip('.')
            self.sys_fov_ingame.set(hfov_clean)
            self._fov_updating = False
        except ValueError:
            pass

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
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            
        presets = []
        excluded_files = ["games_sens.json", "app_settings.json"]
        
        for filename in os.listdir(self.config_dir):
            if filename in excluded_files:
                continue
                
            if filename.endswith(".json"):
                presets.append(filename[:-5])
        
        self.preset_cb["values"] = presets
            
    def on_preset_selected(self, event=None):
        self.save_app_settings()

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
            
            self.save_status_label.config(text="✔")
            self.root.after(3000, lambda: self.save_status_label.config(text=""))
            
        except Exception as e:
            self.custom_msg_box("title_error", str(e), True)

    def on_lang_change(self, event=None):
        mode_val = self.calc_fov_mode.get()
        lowered_val = self.calc_lowered_fov.get()
        shoulder_val = self.calc_shoulder_fov.get()

        is_hfov = mode_val in [LANG["RU"]["calc_mode_hfov"], LANG["EN"]["calc_mode_hfov"]]
        is_lowered_def = lowered_val in [LANG["RU"]["opt_default"], LANG["EN"]["opt_default"]]
        is_shoulder_def = shoulder_val in [LANG["RU"]["opt_default"], LANG["EN"]["opt_default"]]

        self.save_app_settings()
        new_l = self.current_lang.get()

        self.calc_fov_mode.set(LANG[new_l]["calc_mode_hfov"] if is_hfov else LANG[new_l]["calc_mode_vfov"])
        self.calc_lowered_fov.set(LANG[new_l]["opt_default"] if is_lowered_def else LANG[new_l]["opt_zoom"])
        self.calc_shoulder_fov.set(LANG[new_l]["opt_default"] if is_shoulder_def else LANG[new_l]["opt_zoom"])

        for widget in self.root.winfo_children(): 
            widget.destroy()
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
        self.preset_cb.pack(side="left", padx=(0, 10))
        self.preset_cb.bind("<<ComboboxSelected>>", self.on_preset_selected)
        
        ttk.Button(preset_frame, text=self.tr("btn_preset_save"), command=self.action_save_preset).pack(side="left", padx=(0, 10))
        ttk.Button(preset_frame, text=self.tr("btn_preset_apply"), command=self.action_load_preset).pack(side="left", padx=(0, 10))
        ttk.Button(preset_frame, text=self.tr("btn_preset_new"), command=self.new_preset).pack(side="left", padx=(0, 10))
        ttk.Button(preset_frame, text=self.tr("btn_preset_del"), command=self.action_delete_preset).pack(side="left", padx=(0, 10))
        
        self.save_status_label = tk.Label(preset_frame, text="", bg=self.bg_main, fg=self.success_text, font=("Segoe UI", 12, "bold"))
        self.save_status_label.pack(side="left", padx=(15, 0))

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
        tab_sys.columnconfigure(0, weight=1) 
        
        frame_fov = ttk.LabelFrame(tab_sys, padding=(15, 10))
        
        lbl_fov_title = ttk.Label(tab_sys, text=self.tr("sys_fov_frame"), cursor="question_arrow", style="TLabelframe.Label")
        
        frame_fov.configure(labelwidget=lbl_fov_title)
        frame_fov.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        corner_fov = tk.Canvas(lbl_fov_title, width=6, height=6, bg=self.bg_main, highlightthickness=0)
        corner_fov.place(relx=1.0, rely=0.0, x=-2, y=2, anchor="ne")
        corner_fov.create_polygon(0, 0, 6, 0, 6, 6, fill="#ffffff")
        
        create_tooltip(lbl_fov_title, self.tr("sys_fov_tooltip"))

        frame_fov.columnconfigure(0, minsize=260)
        frame_fov.columnconfigure(1, weight=1)
        
        ttk.Label(frame_fov, text=self.tr("sys_menu_label")).grid(row=0, column=0, sticky="w", pady=5)
        entry_ingame = ttk.Entry(frame_fov, textvariable=self.sys_fov_ingame)
        entry_ingame.grid(row=0, column=1, sticky="ew", pady=5)
        
        ttk.Label(frame_fov, text=self.tr("sys_config_label")).grid(row=1, column=0, sticky="w", pady=5)
        entry_config = ttk.Entry(frame_fov, textvariable=self.sys_fov_config)
        entry_config.grid(row=1, column=1, sticky="ew", pady=5)
        
        self.system_entries["FieldOfView"] = entry_config       
        
        frame_sys_other = ttk.LabelFrame(tab_sys, text=self.tr("sys_other_frame"), padding=(15, 10))
        frame_sys_other.grid(row=1, column=0, sticky="ew")
        
        frame_sys_other.columnconfigure(0, minsize=260)
        frame_sys_other.columnconfigure(1, weight=1)
        
        for i, key in enumerate(["MaxFPS", "OverscanScaling"]):
            ttk.Label(frame_sys_other, text=self.tr(key) + ":").grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(frame_sys_other)
            entry.grid(row=i, column=1, sticky="ew", pady=5)
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
        
        tab_calc = ttk.Frame(notebook, padding=20)
        notebook.add(tab_calc, text=self.tr("calc_tab"))
        tab_calc.columnconfigure(0, weight=1)
        
        frame_conv = ttk.LabelFrame(tab_calc, text=self.tr("calc_import_frame"), padding=(15, 10))
        frame_conv.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        frame_conv.columnconfigure(0, minsize=260)
        frame_conv.columnconfigure(1, weight=1)
        frame_conv.columnconfigure(2, minsize=220)
        
        ttk.Label(frame_conv, text=self.tr("calc_game_label")).grid(row=0, column=0, sticky="w", pady=5)
        ttk.Combobox(frame_conv, textvariable=self.conv_game, values=list(self.games_data.keys()), state="readonly").grid(row=0, column=2, sticky="ew", pady=5)
        
        ttk.Label(frame_conv, text=self.tr("calc_sens_label")).grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(frame_conv, textvariable=self.conv_sens).grid(row=1, column=2, sticky="ew", pady=5)

        frame_calc = ttk.LabelFrame(tab_calc, text=self.tr("calc_params_frame"), padding=(15, 10))
        frame_calc.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        frame_calc.columnconfigure(0, minsize=260)
        frame_calc.columnconfigure(1, weight=1)
        frame_calc.columnconfigure(2, minsize=220)
        
        ttk.Label(frame_calc, text=self.tr("calc_base_sens_label")).grid(row=0, column=0, sticky="w", pady=8)
        ttk.Entry(frame_calc, textvariable=self.calc_base_sens).grid(row=0, column=2, sticky="ew", pady=8)
        
        ttk.Label(frame_calc, text=self.tr("calc_fov_mode")).grid(row=1, column=0, sticky="w", pady=8)
        fov_mode_cb = ttk.Combobox(frame_calc, textvariable=self.calc_fov_mode, 
                                   values=[self.tr("calc_mode_hfov"), self.tr("calc_mode_vfov")], 
                                   state="readonly")
        fov_mode_cb.grid(row=1, column=2, sticky="ew", pady=8)
        
        ttk.Label(frame_calc, text=self.tr("calc_fov_label")).grid(row=2, column=0, sticky="w", pady=8)
        ttk.Entry(frame_calc, textvariable=self.calc_fov).grid(row=2, column=2, sticky="ew", pady=8)
        
        ttk.Label(frame_calc, text=self.tr("calc_lowered_label")).grid(row=3, column=0, sticky="w", pady=8)
        ttk.Combobox(frame_calc, textvariable=self.calc_lowered_fov, 
                     values=[self.tr("opt_default"), self.tr("opt_zoom")], 
                     state="readonly").grid(row=3, column=2, sticky="ew", pady=8)
        
        ttk.Label(frame_calc, text=self.tr("calc_shoulder_label")).grid(row=4, column=0, sticky="w", pady=8)
        ttk.Combobox(frame_calc, textvariable=self.calc_shoulder_fov, 
                     values=[self.tr("opt_default"), self.tr("opt_zoom")], 
                     state="readonly").grid(row=4, column=2, sticky="ew", pady=8)
        
        mdc_label = ttk.Label(frame_calc, text=self.tr("calc_mdc_label"), cursor="question_arrow")
        mdc_label.grid(row=5, column=0, sticky="w", pady=8)
        
        corner = tk.Canvas(mdc_label, width=6, height=6, bg=self.bg_main, highlightthickness=0)
        corner.place(relx=1.0, rely=0.0, x=-2, y=2, anchor="ne")
        
        corner.create_polygon(0, 0, 6, 0, 6, 6, fill=self.accent_text)
        
        mdc_entry = ttk.Entry(frame_calc, textvariable=self.calc_mdc)
        mdc_entry.grid(row=5, column=2, sticky="ew", pady=8)

        create_tooltip(mdc_label, self.tr("calc_mdc_tooltip"))
        create_tooltip(mdc_entry, self.tr("calc_mdc_tooltip"))
        
        btn_apply = tk.Button(tab_calc, text=self.tr("btn_calculate"), font=("Segoe UI", 10, "bold"), 
                              bg=self.bg_listen, fg="#ffffff", activebackground=self.accent_text, activeforeground="#ffffff",
                              relief="flat", cursor="hand2", pady=8)
        btn_apply.grid(row=2, column=0, sticky="ew", pady=(10, 5))
        btn_apply.config(command=self.recalculate_sens)
        
        ttk.Label(tab_calc, text=self.tr("calc_notice"), 
                  foreground=self.accent_text, font=("Segoe UI", 9, "italic")).grid(row=3, column=0, pady=(5, 0), sticky="w")
        
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