# -*- coding: utf-8 -*-
import sys
import os
import re
import json
import math
import ctypes
import stat
import shutil
import time

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFormLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QTabWidget, QScrollArea, QFrame, QGroupBox,
    QMessageBox, QInputDialog, QFileDialog, QSizePolicy, QSpacerItem,
    QToolTip, QStackedWidget, QButtonGroup
)
from PySide6.QtCore import Qt, QTimer, QEvent, QObject, Signal, QSize, QPointF
from PySide6.QtGui import (
    QIcon, QFont, QKeyEvent, QMouseEvent, QWheelEvent, QCursor, QPalette, QColor,
    QImage, QPainter, QPolygonF, QPixmap, QPen, QPainterPath
)

def ensure_arrow_icons(target_dir=None):
    if not target_dir:
        import tempfile
        target_dir = os.path.join(tempfile.gettempdir(), "hunt_settings_ui")
    os.makedirs(target_dir, exist_ok=True)
    p_normal = os.path.join(target_dir, "arrow_down.png")
    p_hover = os.path.join(target_dir, "arrow_down_hover.png")
    for path, col in [(p_normal, QColor("#8b949e")), (p_hover, QColor("#58a6ff"))]:
        if not os.path.exists(path):
            img = QImage(10, 6, QImage.Format.Format_ARGB32_Premultiplied)
            img.fill(Qt.GlobalColor.transparent)
            painter = QPainter(img)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(col)
            poly = QPolygonF([QPointF(0, 0), QPointF(10, 0), QPointF(5, 5)])
            painter.drawPolygon(poly)
            painter.end()
            img.save(path)
    return p_normal.replace('\\', '/'), p_hover.replace('\\', '/')

def create_save_icon():
    pix = QPixmap(24, 24)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(QPen(QColor("#c9d1d9"), 1.8))
    p.setBrush(Qt.BrushStyle.NoBrush)
    path = QPainterPath()
    path.moveTo(4.5, 4.5)
    path.lineTo(16.5, 4.5)
    path.lineTo(19.5, 7.5)
    path.lineTo(19.5, 19.5)
    path.lineTo(4.5, 19.5)
    path.closeSubpath()
    p.drawPath(path)
    p.drawRect(7.5, 4.5, 7, 5)
    p.drawRect(7, 13, 10, 6.5)
    p.end()
    return QIcon(pix)

def create_trash_icon():
    pix = QPixmap(24, 24)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(QPen(QColor("#f85149"), 1.8))
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawLine(4.5, 7, 19.5, 7)
    p.drawPolyline([QPointF(8.5, 7), QPointF(8.5, 4.5), QPointF(15.5, 4.5), QPointF(15.5, 7)])
    body = QPainterPath()
    body.moveTo(6.5, 8)
    body.lineTo(7.5, 19)
    body.lineTo(16.5, 19)
    body.lineTo(17.5, 8)
    p.drawPath(body)
    p.drawLine(10, 10.5, 10, 16.5)
    p.drawLine(14, 10.5, 14, 16.5)
    p.end()
    return QIcon(pix)

def create_apply_icon():
    pix = QPixmap(24, 24)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor("#3fb950"), 2.2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.drawPolyline([QPointF(5, 12), QPointF(10, 17.5), QPointF(19, 6.5)])
    p.end()
    return QIcon(pix)

def global_excepthook(exc_type, exc_value, exc_traceback):
    import traceback
    err_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    try:
        with open("crash_log.txt", "a", encoding="utf-8") as f:
            f.write(f"--- Error at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n{err_msg}\n")
    except Exception:
        pass
    try:
        QMessageBox.critical(None, "Error / Ошибка", f"Произошла непредвиденная ошибка:\n\n{err_msg}")
    except Exception:
        pass
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = global_excepthook

def can_reach_range(val_str, min_val, max_val):
    s = val_str.replace(',', '.').strip()
    if not s:
        return True
    try:
        val = float(s)
    except ValueError:
        return False

    if min_val <= val <= max_val:
        return True

    if val > max_val:
        return False

    if '.' in s:
        parts = s.split('.')
        dec_len = len(parts[1])
        max_possible = val + 10**(-dec_len)
        return max_possible >= min_val and val <= max_val

    if (val + 0.999999 >= min_val) and (val <= max_val):
        return True

    if (val * 10 <= max_val) and (val * 10 + 9.999999 >= min_val):
        return True
    if (val * 100 <= max_val) and (val * 100 + 99.999999 >= min_val):
        return True

    return False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def apply_dark_title_bar(window):
    try:
        hwnd = int(window.winId())
        value = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(value), ctypes.sizeof(value))
    except Exception:
        pass

def setup_dark_palette(app):
    if not app:
        return
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(11, 14, 20))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(201, 209, 217))
    palette.setColor(QPalette.ColorRole.Base, QColor(11, 14, 20))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(16, 21, 31))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(26, 34, 47))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(201, 209, 217))
    palette.setColor(QPalette.ColorRole.Text, QColor(201, 209, 217))
    palette.setColor(QPalette.ColorRole.Button, QColor(23, 31, 43))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(201, 209, 217))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Link, QColor(88, 166, 255))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(31, 111, 235))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

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
        "tooltip_preset_new": "Создать новый профиль (+)",
        "tooltip_preset_apply": "Применить выбранный профиль",
        "tooltip_preset_save": "Сохранить текущие настройки в выбранный профиль",
        "tooltip_preset_del": "Удалить выбранный профиль",
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
        "IronSightsMouseSensitivity": "Мушка", 
        "ShortScopeMouseSensitivity": "Меткий глаз",
        "MediumScopeMouseSensitivity": "Опытный стрелок", 
        "LongScopeMouseSensitivity": "Снайпер",
        "PeepholeMouseSensitivity": "Апертура", 
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
        "calc_base_sens_label": "Базовая чувствительность:",
        "calc_fov_label": "Угол обзора:",
        "btn_calculate": "Рассчитать и перенести в настройки",
        "calc_notice": "✓ Мгновенно рассчитывает и обновляет все прицелы справа",
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
        "btn_auto_find_tooltip": "Автоматически найти файл attributes.xml игры в Steam",
        "msg_found_hunt": "Файл игры успешно найден",
        "msg_not_found_hunt": "Не удалось автоматически обнаружить файл attributes.xml.\nПожалуйста, укажите его вручную через кнопку 'Обзор...'",
        "btn_reload_games_tooltip": "Перезагрузить список игр и множители из configs/games_sens.json",
        "msg_games_reloaded": "Список игр успешно обновлен ({count} игр)!",
        "calc_cm_frame": " Конвертер cm/360 ",
        "calc_dpi_label": "DPI мыши:",
        "calc_cm_label": "Дистанция cm/360 (см):",
        "calc_cm_tooltip": "Количество сантиметров движения мыши по коврику для полного разворота персонажа на 360° в игре.",
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
        "tooltip_preset_new": "Create new profile (+)",
        "tooltip_preset_apply": "Apply selected profile",
        "tooltip_preset_save": "Save current settings to selected profile",
        "tooltip_preset_del": "Delete selected profile",
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
        "MouseSensitivity": "Default",
        "HipMouseSensitivity": "Shoulder",
        "IronSightsMouseSensitivity": "Iron Sights",
        "ShortScopeMouseSensitivity": "Deadeye",
        "MediumScopeMouseSensitivity": "Marksman",
        "LongScopeMouseSensitivity": "Sniper",
        "PeepholeMouseSensitivity": "Aperture",
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
        "calc_base_sens_label": "Base Sensitivity:",
        "calc_fov_label": "Field of View:",
        "btn_calculate": "Calculate and transfer to settings",
        "calc_notice": "✓ Instantly calculates and updates all scopes on the right",
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
        "btn_auto_find_tooltip": "Automatically locate game's attributes.xml in Steam",
        "msg_found_hunt": "Game config file found successfully",
        "msg_not_found_hunt": "Could not automatically find attributes.xml.\nPlease select it manually using 'Browse...'",
        "btn_reload_games_tooltip": "Reload games list and multipliers from configs/games_sens.json",
        "msg_games_reloaded": "Games list reloaded successfully ({count} games)!",
        "calc_cm_frame": " cm/360 Converter ",
        "calc_dpi_label": "Mouse DPI:",
        "calc_cm_label": "cm/360 Distance (cm):",
        "calc_cm_tooltip": "Physical distance in centimeters mouse moves on mousepad to complete a full 360° turn in-game.",
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


LANG["RU"]["search_binds"] = "Поиск действия..."
LANG["RU"]["status_ready"] = "Готов к работе"
LANG["RU"]["status_saved"] = "Настройки успешно сохранены в файл игры"
LANG["RU"]["status_loaded"] = "Настройки загружены из файла"
LANG["RU"]["btn_copy_all"] = "Копировать все"
LANG["RU"]["btn_paste_all"] = "Вставить все"
LANG["RU"]["copied"] = "Скопировано в буфер обмена!"
LANG["RU"]["pasted"] = "Вставлено из буфера обмена!"
LANG["RU"]["nav_sens"] = "  Сенсор и прицелы"
LANG["RU"]["nav_binds"] = "  Назначение клавиш"
LANG["RU"]["nav_sys"] = "  Система и FOV"
LANG["RU"]["page_sens_title"] = "Сенсор и прицелы"
LANG["RU"]["page_sens_sub"] = "Калькулятор 1:1, cm/360 и прицелы"
LANG["RU"]["page_binds_title"] = "Назначение клавиш"
LANG["RU"]["page_binds_sub"] = "Настройка всех действий в игре"
LANG["RU"]["page_sys_title"] = "Системные параметры и FOV"
LANG["RU"]["page_sys_sub"] = "Угол обзора, FPS и масштаб"
LANG["RU"]["btn_apply_1to1"] = "Рассчитать 1:1 для всех прицелов"
LANG["RU"]["file_status_ok"] = "attributes.xml подключен"
LANG["RU"]["file_status_err"] = "attributes.xml не найден"
LANG["RU"]["profile_lbl"] = "Профиль:"
LANG["RU"]["btn_save_game_header"] = "Сохранить в игру"
LANG["RU"]["btn_auto_find"] = "Автопоиск"
LANG["RU"]["btn_reload_short"] = "Обновить"
LANG["RU"]["backup_card_title"] = "Файл и резервные копии"
LANG["RU"]["backup_info"] = "Перед каждым сохранением программа автоматически создаёт резервную копию вашего attributes.xml в папку configs/backups/"

LANG["EN"]["search_binds"] = "Search action..."
LANG["EN"]["status_ready"] = "Ready"
LANG["EN"]["status_saved"] = "Settings saved to game file successfully"
LANG["EN"]["status_loaded"] = "Settings loaded from file"
LANG["EN"]["btn_copy_all"] = "Copy All"
LANG["EN"]["btn_paste_all"] = "Paste All"
LANG["EN"]["copied"] = "Copied to clipboard!"
LANG["EN"]["pasted"] = "Pasted from clipboard!"
LANG["EN"]["nav_sens"] = "  Sens && Scopes"
LANG["EN"]["nav_binds"] = "  Keybinds"
LANG["EN"]["nav_sys"] = "  System && FOV"
LANG["EN"]["page_sens_title"] = "Sens & Scopes"
LANG["EN"]["page_sens_sub"] = "1:1 Matcher, cm/360 & Scopes"
LANG["EN"]["page_binds_title"] = "Keybinds"
LANG["EN"]["page_binds_sub"] = "Configure all in-game actions"
LANG["EN"]["page_sys_title"] = "System & FOV"
LANG["EN"]["page_sys_sub"] = "FOV expansion, FPS limit & HUD scaling"
LANG["EN"]["btn_apply_1to1"] = "Calculate 1:1 for All Scopes"
LANG["EN"]["file_status_ok"] = "attributes.xml connected"
LANG["EN"]["file_status_err"] = "attributes.xml not found"
LANG["EN"]["profile_lbl"] = "Profile:"
LANG["EN"]["btn_save_game_header"] = "Save Settings"
LANG["EN"]["btn_auto_find"] = "Auto Detect"
LANG["EN"]["btn_reload_short"] = "Reload"
LANG["EN"]["backup_card_title"] = "File & Backups"
LANG["EN"]["backup_info"] = "Before each save, a backup of your attributes.xml is automatically created in configs/backups/"

HUNT_YAW = 0.0429718162181364
HIDDEN_FACTORS = {
    "MouseSensitivity": 1.000000,
    "HipMouseSensitivity": 1.111111,
    "IronSightsMouseSensitivity": 1.851851,
    "ShortScopeMouseSensitivity": 2.020202,
    "MediumScopeMouseSensitivity": 5.555556,
    "LongScopeMouseSensitivity": 3.703704,
    "PeepholeMouseSensitivity": 5.555556
}

MODERN_QSS = """
QMainWindow, QWidget#centralWidget {
    background-color: #0b0e14;
    color: #c9d1d9;
    font-family: 'Segoe UI', -apple-system, sans-serif;
    font-size: 13px;
}

QFrame#sidebarFrame {
    background-color: #0c1017;
    border-right: 1px solid #1a2230;
}

QFrame#topBarFrame {
    background-color: #0c1017;
    border-bottom: 1px solid #1a2230;
}

/* Ensure NO white backgrounds in any scroll area or viewport */
QScrollArea, QScrollArea > QWidget, QScrollArea > QWidget > QWidget, QScrollArea::viewport {
    background-color: #0b0e14;
    border: none;
}

QScrollBar:vertical {
    background: #0b0e14;
    width: 8px;
    margin: 2px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #242c3b;
    min-height: 25px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #388bfd;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QPushButton.navBtn {
    background-color: transparent;
    color: #8b949e;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    font-weight: 600;
    font-size: 13px;
}
QPushButton.navBtn:hover {
    background-color: #141b26;
    color: #f0f6fc;
}
QPushButton.navBtn:checked {
    background-color: #162132;
    color: #58a6ff;
    font-weight: 700;
    border-left: 3px solid #58a6ff;
}

QGroupBox {
    background-color: #10151f;
    border: 1px solid #1c2636;
    border-radius: 10px;
    margin-top: 14px;
    padding-top: 20px;
    padding-left: 14px;
    padding-right: 14px;
    padding-bottom: 14px;
    font-weight: 700;
    font-size: 13px;
    color: #58a6ff;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 2px 8px;
    background-color: #10151f;
    color: #58a6ff;
    border-radius: 4px;
}

QFrame.cardBox {
    background-color: #10151f;
    border: 1px solid #1c2636;
    border-radius: 10px;
}

QLabel {
    color: #c9d1d9;
    font-size: 13px;
}

QLineEdit, QComboBox {
    background-color: #0b0f15;
    color: #f0f6fc;
    border: 1px solid #253142;
    border-radius: 6px;
    padding: 4px 10px;
    min-height: 24px;
    font-size: 13px;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
}
QLineEdit:hover, QComboBox:hover {
    border-color: #388bfd;
}
QLineEdit:focus, QComboBox:focus {
    border: 1px solid #58a6ff;
    background-color: #080b0f;
}
QLineEdit:read-only {
    background-color: #0e131b;
    color: #8b949e;
    border-color: #1a2330;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border: none;
    background: transparent;
}
QComboBox::down-arrow {
    image: url("__ARROW_NORMAL__");
    width: 10px;
    height: 6px;
    border: none;
    background: transparent;
}
QComboBox::down-arrow:hover {
    image: url("__ARROW_HOVER__");
}
QComboBox QAbstractItemView {
    background-color: #10151f;
    color: #c9d1d9;
    border: 1px solid #253142;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
    padding: 4px;
}
QComboBox QAbstractItemView QScrollBar:vertical {
    background-color: #0b0f15;
    width: 10px;
    margin: 2px 0px 2px 0px;
    border-radius: 4px;
}
QComboBox QAbstractItemView QScrollBar::handle:vertical {
    background-color: #253142;
    min-height: 20px;
    border-radius: 4px;
}
QComboBox QAbstractItemView QScrollBar::handle:vertical:hover {
    background-color: #58a6ff;
}
QComboBox QAbstractItemView QScrollBar::add-line:vertical,
QComboBox QAbstractItemView QScrollBar::sub-line:vertical {
    height: 0px;
}

QPushButton {
    background-color: #171f2b;
    color: #c9d1d9;
    border: 1px solid #283548;
    border-radius: 6px;
    padding: 7px 15px;
    font-size: 13px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #222d3d;
    border-color: #58a6ff;
    color: #ffffff;
}
QPushButton:pressed {
    background-color: #10151f;
}

QPushButton#primarySaveBtn {
    background-color: #238636;
    color: #ffffff;
    border: 1px solid #2ea043;
    font-weight: 700;
    font-size: 13px;
    padding: 8px 18px;
}
QPushButton#primarySaveBtn:hover {
    background-color: #2ea043;
    border-color: #3fb950;
}
QPushButton#primarySaveBtn:pressed {
    background-color: #1f6f2e;
}

QPushButton#actionBtn {
    background-color: #1f6feb;
    color: #ffffff;
    border: 1px solid #388bfd;
    font-weight: 700;
    padding: 8px 18px;
}
QPushButton#actionBtn:hover {
    background-color: #388bfd;
}
QPushButton#actionBtn:pressed {
    background-color: #1158c7;
}

QPushButton#dangerBtn {
    background-color: #171f2b;
    color: #f85149;
    border: 1px solid #283548;
}
QPushButton#dangerBtn:hover {
    background-color: #b62324;
    color: #ffffff;
    border-color: #f85149;
}
QPushButton#dangerBtn[class="topIconBtn"]:hover, QPushButton#dangerBtn.topIconBtn:hover {
    background-color: #381a1e;
    border-color: #f85149;
}
QPushButton#applyBtn[class="topIconBtn"]:hover, QPushButton#applyBtn.topIconBtn:hover {
    background-color: #15321f;
    border-color: #3fb950;
}

QPushButton[class="topIconBtn"], QPushButton.topIconBtn {
    background-color: #17202d;
    color: #c9d1d9;
    border: 1px solid #283548;
    border-radius: 6px;
    font-size: 14px;
    font-weight: bold;
    padding: 0px;
}
QPushButton[class="topIconBtn"]:hover, QPushButton.topIconBtn:hover {
    background-color: #243042;
    border-color: #58a6ff;
    color: #ffffff;
}
QPushButton[class="topIconBtn"]:pressed, QPushButton.topIconBtn:pressed {
    background-color: #10151f;
}

QPushButton[class="topBtn"], QPushButton.topBtn {
    background-color: #17202d;
    color: #c9d1d9;
    border: 1px solid #283548;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    padding: 0px 12px;
}
QPushButton[class="topBtn"]:hover, QPushButton.topBtn:hover {
    background-color: #243042;
    border-color: #58a6ff;
    color: #ffffff;
}
QPushButton[class="topBtn"]:pressed, QPushButton.topBtn:pressed {
    background-color: #10151f;
}

QToolTip {
    background-color: #1a222f;
    color: #c9d1d9;
    border: 1px solid #2d3b50;
    border-radius: 6px;
    padding: 8px;
    font-size: 12px;
}
"""

class BindButton(QPushButton):
    def __init__(self, action, slot, app):
        super().__init__()
        self.action = action
        self.slot = slot
        self.app = app
        self.dik_code = "-1"
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumWidth(110)
        self.setMinimumHeight(32)
        self.update_style(False)
        self.clicked.connect(self._on_click)

    def update_style(self, listening=False):
        if listening:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #1f6feb;
                    color: #ffffff;
                    border: 1px solid #58a6ff;
                    border-radius: 6px;
                    font-weight: 700;
                    font-size: 12px;
                    padding: 4px 10px;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #141b24;
                    color: #e6edf3;
                    border: 1px solid #283344;
                    border-bottom: 2px solid #1c2635;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 12px;
                    padding: 4px 10px;
                }
                QPushButton:hover {
                    background-color: #1d2634;
                    border-color: #58a6ff;
                    color: #ffffff;
                }
            """)

    def _on_click(self):
        if not self.app.is_listening:
            self.app.start_listening(self.action, self.slot, self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            if not self.app.is_listening:
                self.app.clear_bind(self.action, self.slot, self)
                event.accept()
                return
        super().mousePressEvent(event)


class InputCaptureFilter(QObject):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def eventFilter(self, obj, event):
        if not self.app.is_listening:
            return False

        etype = event.type()
        if etype == QEvent.Type.KeyPress:
            vk = event.nativeVirtualKey()
            dik = None
            if vk == 16 or vk in (160, 161):
                try:
                    is_r = bool(ctypes.windll.user32.GetAsyncKeyState(0xA1) & 0x8000)
                except Exception:
                    is_r = (vk == 161)
                dik = "53" if is_r else "41"
            elif vk == 17 or vk in (162, 163):
                try:
                    is_r = bool(ctypes.windll.user32.GetAsyncKeyState(0xA3) & 0x8000)
                except Exception:
                    is_r = (vk == 163)
                dik = "156" if is_r else "28"
            elif vk == 18 or vk in (164, 165):
                try:
                    is_r = bool(ctypes.windll.user32.GetAsyncKeyState(0xA5) & 0x8000)
                except Exception:
                    is_r = (vk == 165)
                dik = "183" if is_r else "55"
            else:
                str_vk = str(vk)
                dik = VK_TO_DIK.get(str_vk, str_vk)

            if dik is not None:
                self.app.finish_bind(dik)
                return True

        elif etype == QEvent.Type.MouseButtonPress:
            btn = event.button()
            dik = None
            if btn == Qt.MouseButton.LeftButton:
                dik = "256"
            elif btn == Qt.MouseButton.RightButton:
                dik = "257"
            elif btn == Qt.MouseButton.MiddleButton:
                dik = "258"
            elif btn in (Qt.MouseButton.BackButton, Qt.MouseButton.XButton1):
                dik = "259"
            elif btn in (Qt.MouseButton.ForwardButton, Qt.MouseButton.XButton2):
                dik = "260"

            if dik is not None:
                self.app.finish_bind(dik)
                return True

        elif etype == QEvent.Type.Wheel:
            delta = event.angleDelta().y()
            dik = "264" if delta > 0 else "265"
            self.app.finish_bind(dik)
            return True

        return False

class HuntConfigApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.config_dir = os.path.join(self.base_dir, "configs")
        os.makedirs(self.config_dir, exist_ok=True)
        self.app_settings_file = os.path.join(self.config_dir, "app_settings.json")
        self.games_file = os.path.join(self.config_dir, "games_sens.json")

        self.sens_keys = [
            "MouseSensitivity", "HipMouseSensitivity", "IronSightsMouseSensitivity",
            "ShortScopeMouseSensitivity", "MediumScopeMouseSensitivity",
            "LongScopeMouseSensitivity", "PeepholeMouseSensitivity"
        ]
        self.system_keys = ["MaxFPS", "OverscanScaling"]

        self.current_lang = "RU"
        self.file_path_str = ""
        self.last_preset_str = ""
        self.dpi_str = ""
        
        self.sens_entries = {}
        self.system_entries = {}
        self.current_binds = {}
        self.bind_buttons = {}
        self.bind_row_widgets = []
        self.category_widgets = []
        self.current_content = ""

        self.is_listening = False
        self.listening_action = None
        self.listening_slot = None
        self.listening_btn = None

        self.input_filter = InputCaptureFilter(self)
        self.mouse_check_timer = QTimer(self)
        self.mouse_check_timer.timeout.connect(self._check_extra_mouse_buttons)

        self._cm_updating = False
        self._fov_updating = False
        self._calc_updating = False

        self.load_app_settings()
        self.load_games_sens()

        self.init_window()
        self.create_ui()
        self.refresh_presets()

        if self.file_path_str and os.path.exists(self.file_path_str):
            self.load_values()
        else:
            self.update_file_status()

        apply_dark_title_bar(self)

    def init_window(self):
        self.setWindowTitle(self.tr("title"))
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowSystemMenuHint |
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        self.setFixedSize(1140, 890)
        for legacy_f in ["arrow_down.png", "arrow_down_hover.png"]:
            legacy_p = os.path.join(self.config_dir, legacy_f)
            if os.path.exists(legacy_p):
                try:
                    os.remove(legacy_p)
                except Exception:
                    pass
        arrow_normal, arrow_hover = ensure_arrow_icons()
        qss = MODERN_QSS.replace("__ARROW_NORMAL__", arrow_normal).replace("__ARROW_HOVER__", arrow_hover)
        self.setStyleSheet(qss)
        setup_dark_palette(QApplication.instance())
        for ip in [resource_path("icon.ico"), os.path.join(self.base_dir, "icon.ico"), "icon.ico"]:
            if os.path.exists(ip):
                app_icon = QIcon(ip)
                self.setWindowIcon(app_icon)
                app_inst = QApplication.instance()
                if app_inst:
                    app_inst.setWindowIcon(app_icon)
                break

    def tr(self, key):
        return LANG.get(self.current_lang, LANG["RU"]).get(key, key)

    def load_app_settings(self):
        if os.path.exists(self.app_settings_file):
            try:
                with open(self.app_settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.file_path_str = data.get("path", "")
                    self.current_lang = data.get("lang", "RU")
                    self.last_preset_str = data.get("last_preset", "")
                    self.dpi_str = str(data.get("dpi", ""))
            except Exception:
                pass

    def save_app_settings(self):
        try:
            with open(self.app_settings_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "path": self.path_entry.text().strip() if hasattr(self, 'path_entry') else self.file_path_str,
                    "lang": self.current_lang,
                    "last_preset": self.preset_cb.currentText() if hasattr(self, 'preset_cb') else self.last_preset_str,
                    "dpi": self.dpi_entry.text().strip() if hasattr(self, 'dpi_entry') else self.dpi_str
                }, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def load_games_sens(self):
        self.games_data = {}
        target_path = self.games_file

        if os.path.exists(target_path):
            try:
                with open(target_path, 'r', encoding='utf-8') as f:
                    self.games_data = json.load(f)
            except Exception:
                self.games_data = {}

        self.games_data.pop("cm/360", None)

        if not self.games_data:
            base_here = os.path.dirname(os.path.abspath(__file__))
            candidates = [
                resource_path(os.path.join("configs", "games_sens.json")),
                resource_path("games_sens.json"),
                os.path.join(base_here, "configs", "games_sens.json"),
                os.path.join(base_here, "games_sens.json")
            ]
            for cand in candidates:
                if os.path.exists(cand):
                    try:
                        with open(cand, 'r', encoding='utf-8') as f:
                            self.games_data = json.load(f)
                        with open(target_path, 'w', encoding='utf-8') as f:
                            json.dump(self.games_data, f, indent=4, ensure_ascii=False)
                        break
                    except Exception:
                        pass

    def reload_games_sens(self, silent=False):
        self.load_games_sens()
        games_list = list(self.games_data.keys())
        self.game_cb.blockSignals(True)
        self.game_cb.clear()
        self.game_cb.addItems(games_list)
        self.game_cb.blockSignals(False)
        if not silent:
            QMessageBox.information(self, self.tr("title_info"), self.tr("msg_games_reloaded").format(count=len(games_list)))

    def create_ui(self):
        central_widget = QWidget(self)
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.create_sidebar(root_layout)

        main_area = QWidget()
        main_area.setObjectName("mainArea")
        main_layout = QVBoxLayout(main_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.create_top_bar(main_layout)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1)

        bottom_bar = QFrame()
        bottom_bar.setObjectName("bottomBarFrame")
        bottom_bar.setFixedHeight(26)
        bottom_bar.setStyleSheet("background-color: #0c1017; border-top: 1px solid #1a2230;")
        bb_status_layout = QHBoxLayout(bottom_bar)
        bb_status_layout.setContentsMargins(18, 0, 18, 0)
        self.lbl_status = QLabel(self.tr("status_ready"))
        self.lbl_status.setStyleSheet("color: #7d8590; font-size: 11px;")
        bb_status_layout.addWidget(self.lbl_status)
        bb_status_layout.addStretch()
        self.lbl_footer_info = QLabel("Hunt: Showdown 1896 Config Studio")
        self.lbl_footer_info.setStyleSheet("color: #484f58; font-size: 11px;")
        bb_status_layout.addWidget(self.lbl_footer_info)
        main_layout.addWidget(bottom_bar)

        self.page_sens = QWidget()
        self.page_binds = QWidget()
        self.page_sys = QWidget()

        self.stacked_widget.addWidget(self.page_sens)
        self.stacked_widget.addWidget(self.page_binds)
        self.stacked_widget.addWidget(self.page_sys)

        self.setup_sens_page()
        self.setup_binds_page()
        self.setup_sys_page()

        root_layout.addWidget(main_area, 1)

    def create_sidebar(self, parent_layout):
        sidebar = QFrame()
        sidebar.setObjectName("sidebarFrame")
        sidebar.setFixedWidth(230)
        s_layout = QVBoxLayout(sidebar)
        s_layout.setContentsMargins(14, 18, 14, 18)
        s_layout.setSpacing(10)

        brand_widget = QWidget()
        b_layout = QVBoxLayout(brand_widget)
        b_layout.setContentsMargins(0, 0, 0, 0)
        b_layout.setSpacing(2)

        lbl_app_title = QLabel("HUNT: 1896")
        lbl_app_title.setStyleSheet("font-size: 16px; font-weight: 800; color: #f0f6fc; letter-spacing: 1px;")
        b_layout.addWidget(lbl_app_title)

        lbl_app_sub = QLabel("Config & Sens Studio")
        lbl_app_sub.setStyleSheet("font-size: 11px; font-weight: 500; color: #7d8590;")
        b_layout.addWidget(lbl_app_sub)
        s_layout.addWidget(brand_widget)

        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("color: #1e2634; margin: 4px 0px 8px 0px;")
        s_layout.addWidget(div)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        self.btn_nav_sens = QPushButton(self.tr("nav_sens"))
        self.btn_nav_sens.setProperty("class", "navBtn")
        self.btn_nav_sens.setCheckable(True)
        self.btn_nav_sens.setChecked(True)
        self.btn_nav_sens.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_nav_sens.clicked.connect(lambda: self.switch_page(0))
        self.nav_group.addButton(self.btn_nav_sens)
        s_layout.addWidget(self.btn_nav_sens)

        self.btn_nav_binds = QPushButton(self.tr("nav_binds"))
        self.btn_nav_binds.setProperty("class", "navBtn")
        self.btn_nav_binds.setCheckable(True)
        self.btn_nav_binds.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_nav_binds.clicked.connect(lambda: self.switch_page(1))
        self.nav_group.addButton(self.btn_nav_binds)
        s_layout.addWidget(self.btn_nav_binds)

        self.btn_nav_sys = QPushButton(self.tr("nav_sys"))
        self.btn_nav_sys.setProperty("class", "navBtn")
        self.btn_nav_sys.setCheckable(True)
        self.btn_nav_sys.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_nav_sys.clicked.connect(lambda: self.switch_page(2))
        self.nav_group.addButton(self.btn_nav_sys)
        s_layout.addWidget(self.btn_nav_sys)

        s_layout.addStretch()

        self.file_card = QFrame()
        self.file_card.setProperty("class", "cardBox")
        f_layout = QVBoxLayout(self.file_card)
        f_layout.setContentsMargins(10, 10, 10, 10)
        f_layout.setSpacing(6)

        self.lbl_file_status = QLabel(self.tr("file_status_ok"))
        self.lbl_file_status.setStyleSheet("font-size: 11px; font-weight: 600; color: #3fb950;")
        f_layout.addWidget(self.lbl_file_status)

        self.path_entry = QLineEdit(self.file_path_str)
        self.path_entry.setReadOnly(True)
        self.path_entry.setStyleSheet("font-size: 11px; padding: 4px 6px;")
        self.path_entry.setToolTip(self.file_path_str)
        f_layout.addWidget(self.path_entry)

        btn_box = QWidget()
        bb_layout = QHBoxLayout(btn_box)
        bb_layout.setContentsMargins(0, 0, 0, 0)
        bb_layout.setSpacing(6)

        self.btn_find = QPushButton(self.tr("btn_auto_find"))
        self.btn_find.setStyleSheet("font-size: 11px; padding: 4px 8px;")
        self.btn_find.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_find.setToolTip(self.tr("btn_auto_find_tooltip"))
        self.btn_find.clicked.connect(self.auto_find_path)
        bb_layout.addWidget(self.btn_find)

        self.btn_browse = QPushButton(self.tr("browse"))
        self.btn_browse.setStyleSheet("font-size: 11px; padding: 4px 8px;")
        self.btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_browse.clicked.connect(self.browse_file)
        bb_layout.addWidget(self.btn_browse)

        f_layout.addWidget(btn_box)
        s_layout.addWidget(self.file_card)

        lang_box = QWidget()
        l_layout = QHBoxLayout(lang_box)
        l_layout.setContentsMargins(0, 0, 0, 0)
        l_layout.setSpacing(6)

        lbl_lang = QLabel("Language:")
        lbl_lang.setStyleSheet("color: #7d8590; font-size: 11px;")
        l_layout.addWidget(lbl_lang)

        self.lang_cb = QComboBox()
        self.lang_cb.addItems(["RU", "EN"])
        self.lang_cb.setCurrentText(self.current_lang)
        self.lang_cb.setFixedWidth(65)
        self.lang_cb.setStyleSheet("font-size: 11px; padding: 2px 6px;")
        self.lang_cb.currentIndexChanged.connect(self.on_lang_change)
        l_layout.addWidget(self.lang_cb)
        s_layout.addWidget(lang_box)

        parent_layout.addWidget(sidebar)

    def switch_page(self, index):
        try:
            self.stacked_widget.setCurrentIndex(index)
            if index == 0:
                self.lbl_page_title.setText(self.tr("page_sens_title"))
                self.lbl_page_sub.setText(self.tr("page_sens_sub"))
                self.btn_nav_sens.setChecked(True)
            elif index == 1:
                self.lbl_page_title.setText(self.tr("page_binds_title"))
                self.lbl_page_sub.setText(self.tr("page_binds_sub"))
                self.btn_nav_binds.setChecked(True)
            elif index == 2:
                self.lbl_page_title.setText(self.tr("page_sys_title"))
                self.lbl_page_sub.setText(self.tr("page_sys_sub"))
                self.btn_nav_sys.setChecked(True)
        except Exception:
            pass

    def create_top_bar(self, parent_layout):
        top_bar = QFrame()
        top_bar.setObjectName("topBarFrame")
        top_bar.setFixedHeight(56)
        tb_layout = QHBoxLayout(top_bar)
        tb_layout.setContentsMargins(20, 8, 20, 8)
        tb_layout.setSpacing(14)

        title_box = QWidget()
        t_layout = QVBoxLayout(title_box)
        t_layout.setContentsMargins(0, 0, 0, 0)
        t_layout.setSpacing(1)

        self.lbl_page_title = QLabel(self.tr("page_sens_title"))
        self.lbl_page_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #f0f6fc;")
        t_layout.addWidget(self.lbl_page_title)

        self.lbl_page_sub = QLabel(self.tr("page_sens_sub"))
        self.lbl_page_sub.setStyleSheet("font-size: 11px; color: #7d8590;")
        t_layout.addWidget(self.lbl_page_sub)
        tb_layout.addWidget(title_box, 1)

        self.lbl_profile = QLabel(self.tr("profile_lbl"))
        self.lbl_profile.setStyleSheet("color: #8b949e; font-weight: 600; font-size: 12px;")
        tb_layout.addWidget(self.lbl_profile)

        self.preset_cb = QComboBox()
        self.preset_cb.setMinimumWidth(150)
        self.preset_cb.setMaxVisibleItems(10)
        self.preset_cb.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.preset_cb.currentIndexChanged.connect(self.on_preset_selected)
        tb_layout.addWidget(self.preset_cb)

        self.btn_preset_new = QPushButton("+")
        self.btn_preset_new.setProperty("class", "topIconBtn")
        self.btn_preset_new.setFixedSize(30, 30)
        self.btn_preset_new.setToolTip(self.tr("tooltip_preset_new"))
        self.btn_preset_new.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_preset_new.clicked.connect(self.new_preset)
        tb_layout.addWidget(self.btn_preset_new)

        self.btn_preset_apply = QPushButton()
        self.btn_preset_apply.setObjectName("applyBtn")
        self.btn_preset_apply.setProperty("class", "topIconBtn")
        self.btn_preset_apply.setIcon(create_apply_icon())
        self.btn_preset_apply.setIconSize(QSize(18, 18))
        self.btn_preset_apply.setFixedSize(30, 30)
        self.btn_preset_apply.setToolTip(self.tr("tooltip_preset_apply"))
        self.btn_preset_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_preset_apply.clicked.connect(self.action_load_preset)
        tb_layout.addWidget(self.btn_preset_apply)

        self.btn_preset_save = QPushButton()
        self.btn_preset_save.setProperty("class", "topIconBtn")
        self.btn_preset_save.setIcon(create_save_icon())
        self.btn_preset_save.setIconSize(QSize(18, 18))
        self.btn_preset_save.setFixedSize(30, 30)
        self.btn_preset_save.setToolTip(self.tr("tooltip_preset_save"))
        self.btn_preset_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_preset_save.clicked.connect(self.action_save_preset)
        tb_layout.addWidget(self.btn_preset_save)

        self.btn_preset_del = QPushButton()
        self.btn_preset_del.setObjectName("dangerBtn")
        self.btn_preset_del.setProperty("class", "topIconBtn")
        self.btn_preset_del.setIcon(create_trash_icon())
        self.btn_preset_del.setIconSize(QSize(18, 18))
        self.btn_preset_del.setFixedSize(30, 30)
        self.btn_preset_del.setToolTip(self.tr("tooltip_preset_del"))
        self.btn_preset_del.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_preset_del.clicked.connect(self.action_delete_preset)
        tb_layout.addWidget(self.btn_preset_del)

        self.lbl_preset_status = QLabel("")
        self.lbl_preset_status.setStyleSheet("color: #3fb950; font-weight: bold; font-size: 14px;")
        tb_layout.addWidget(self.lbl_preset_status)

        self.btn_save_game = QPushButton(self.tr("btn_save_game_header"))
        self.btn_save_game.setObjectName("primarySaveBtn")
        self.btn_save_game.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save_game.clicked.connect(self.save_values)
        tb_layout.addWidget(self.btn_save_game)

        parent_layout.addWidget(top_bar)

    def setup_sens_page(self):
        page_layout = QHBoxLayout(self.page_sens)
        page_layout.setContentsMargins(18, 18, 18, 18)
        page_layout.setSpacing(16)

        left_col = QWidget()
        left_layout = QVBoxLayout(left_col)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        self.group_cm = QGroupBox(self.tr("calc_cm_frame"))
        self.group_cm.setFixedHeight(155)
        cm_form = QFormLayout(self.group_cm)
        cm_form.setContentsMargins(14, 16, 14, 16)
        cm_form.setVerticalSpacing(18)
        cm_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.lbl_calc_dpi = QLabel(self.tr("calc_dpi_label"))
        self.dpi_entry = QLineEdit(self.dpi_str)
        self.dpi_entry.textChanged.connect(self._on_dpi_change)
        cm_form.addRow(self.lbl_calc_dpi, self.dpi_entry)

        self.lbl_calc_cm = QLabel(self.tr("calc_cm_label"))
        self.lbl_calc_cm.setToolTip(self.tr("calc_cm_tooltip"))
        self.cm360_entry = QLineEdit()
        self.cm360_entry.setToolTip(self.tr("calc_cm_tooltip"))
        self.cm360_entry.textChanged.connect(self._on_cm360_change)
        cm_form.addRow(self.lbl_calc_cm, self.cm360_entry)
        left_layout.addWidget(self.group_cm)

        self.group_import = QGroupBox(self.tr("calc_import_frame"))
        self.group_import.setFixedHeight(155)
        imp_form = QFormLayout(self.group_import)
        imp_form.setContentsMargins(14, 16, 14, 16)
        imp_form.setVerticalSpacing(18)
        imp_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.lbl_calc_game = QLabel(self.tr("calc_game_label"))
        game_row = QWidget()
        game_row.setFixedHeight(34)
        game_row_layout = QHBoxLayout(game_row)
        game_row_layout.setContentsMargins(0, 0, 0, 0)
        game_row_layout.setSpacing(6)

        self.game_cb = QComboBox()
        self.game_cb.setFixedHeight(34)
        self.game_cb.addItems(list(self.games_data.keys()))
        self.game_cb.currentIndexChanged.connect(self.convert_external_sens)
        game_row_layout.addWidget(self.game_cb, 1)

        self.btn_reload_games = QPushButton(self.tr("btn_reload_short"))
        self.btn_reload_games.setFixedHeight(34)
        self.btn_reload_games.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reload_games.setToolTip(self.tr("btn_reload_games_tooltip"))
        self.btn_reload_games.clicked.connect(lambda: self.reload_games_sens(False))
        game_row_layout.addWidget(self.btn_reload_games)
        imp_form.addRow(self.lbl_calc_game, game_row)

        self.lbl_calc_sens = QLabel(self.tr("calc_sens_label"))
        self.conv_sens_entry = QLineEdit()
        self.conv_sens_entry.textChanged.connect(self.convert_external_sens)
        imp_form.addRow(self.lbl_calc_sens, self.conv_sens_entry)
        left_layout.addWidget(self.group_import)

        self.group_hunt_calc = QGroupBox(self.tr("calc_params_frame"))
        self.group_hunt_calc.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        calc_form = QFormLayout(self.group_hunt_calc)
        calc_form.setContentsMargins(14, 16, 14, 18)
        calc_form.setVerticalSpacing(18)
        calc_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.lbl_calc_base = QLabel(self.tr("calc_base_sens_label"))
        self.base_sens_entry = QLineEdit()
        self.base_sens_entry.textChanged.connect(self._on_base_sens_change)
        calc_form.addRow(self.lbl_calc_base, self.base_sens_entry)

        self.lbl_calc_fov_mode = QLabel(self.tr("calc_fov_mode"))
        self.fov_mode_cb = QComboBox()
        self.fov_mode_cb.addItems([self.tr("calc_mode_hfov"), self.tr("calc_mode_vfov")])
        self.fov_mode_cb.currentIndexChanged.connect(self._on_fov_mode_changed)
        calc_form.addRow(self.lbl_calc_fov_mode, self.fov_mode_cb)

        self.lbl_calc_fov = QLabel(self.tr("calc_fov_label"))
        self.calc_fov_entry = QLineEdit()
        self.calc_fov_entry.setPlaceholderText("79.32 - 112.33")
        self.calc_fov_entry.textChanged.connect(self._on_calc_fov_change)
        self.calc_fov_entry.editingFinished.connect(self._clamp_calc_fov)
        calc_form.addRow(self.lbl_calc_fov, self.calc_fov_entry)

        self.lbl_calc_lowered = QLabel(self.tr("calc_lowered_label"))
        self.lowered_fov_cb = QComboBox()
        self.lowered_fov_cb.addItems([self.tr("opt_default"), self.tr("opt_zoom")])
        calc_form.addRow(self.lbl_calc_lowered, self.lowered_fov_cb)

        self.lbl_calc_shoulder = QLabel(self.tr("calc_shoulder_label"))
        self.shoulder_fov_cb = QComboBox()
        self.shoulder_fov_cb.addItems([self.tr("opt_default"), self.tr("opt_zoom")])
        calc_form.addRow(self.lbl_calc_shoulder, self.shoulder_fov_cb)

        self.lbl_calc_mdc = QLabel(self.tr("calc_mdc_label"))
        self.lbl_calc_mdc.setToolTip(self.tr("calc_mdc_tooltip"))
        self.mdc_entry = QLineEdit()
        self.mdc_entry.setToolTip(self.tr("calc_mdc_tooltip"))
        calc_form.addRow(self.lbl_calc_mdc, self.mdc_entry)

        self.btn_calculate = QPushButton(self.tr("btn_apply_1to1"))
        self.btn_calculate.setObjectName("actionBtn")
        self.btn_calculate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_calculate.setMinimumHeight(42)
        self.btn_calculate.clicked.connect(self.recalculate_sens)

        self.lbl_calc_notice = QLabel(self.tr("calc_notice"))
        self.lbl_calc_notice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_calc_notice.setStyleSheet("color: #58a6ff; font-style: italic; font-size: 11px;")

        calc_btn_box = QWidget()
        calc_btn_box.setMinimumHeight(72)
        calc_btn_layout = QVBoxLayout(calc_btn_box)
        calc_btn_layout.setContentsMargins(0, 16, 0, 0)
        calc_btn_layout.setSpacing(6)
        calc_btn_layout.addWidget(self.btn_calculate)
        calc_btn_layout.addWidget(self.lbl_calc_notice)
        calc_form.addRow(calc_btn_box)

        left_layout.addWidget(self.group_hunt_calc, 1)
        page_layout.addWidget(left_col, 48)

        right_col = QWidget()
        right_layout = QVBoxLayout(right_col)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        sens_box = QGroupBox(self.tr("tab_sens"))
        self.sens_box = sens_box
        sb_layout = QVBoxLayout(sens_box)
        sb_layout.setContentsMargins(16, 20, 16, 16)
        sb_layout.setSpacing(12)

        tool_row = QWidget()
        t_layout = QHBoxLayout(tool_row)
        t_layout.setContentsMargins(0, 0, 0, 0)
        t_layout.setSpacing(8)
        t_layout.addStretch()

        self.btn_copy_all = QPushButton(self.tr("btn_copy_all"))
        self.btn_copy_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy_all.clicked.connect(self.copy_sens_all)
        t_layout.addWidget(self.btn_copy_all)

        self.btn_paste_all = QPushButton(self.tr("btn_paste_all"))
        self.btn_paste_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_paste_all.clicked.connect(self.paste_sens_all)
        t_layout.addWidget(self.btn_paste_all)
        sb_layout.addWidget(tool_row)

        self.sens_labels = {}
        for key in self.sens_keys:
            row_card = QFrame()
            row_card.setStyleSheet("background-color: #0b0f15; border: 1px solid #1c2636; border-radius: 8px;")
            r_layout = QHBoxLayout(row_card)
            r_layout.setContentsMargins(12, 6, 12, 6)
            r_layout.setSpacing(10)

            name_lbl = QLabel(self.tr(key))
            name_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #c9d1d9; border: none; background: transparent;")
            r_layout.addWidget(name_lbl, 1)
            self.sens_labels[key] = name_lbl

            entry = QLineEdit()
            entry.setFixedWidth(110)
            entry.setStyleSheet("font-size: 13px; font-weight: 600; padding: 4px 8px;")
            self.sens_entries[key] = entry
            r_layout.addWidget(entry)

            sb_layout.addWidget(row_card)

        sb_layout.addStretch()
        right_layout.addWidget(sens_box)
        page_layout.addWidget(right_col, 54)

    def setup_binds_page(self):
        layout = QVBoxLayout(self.page_binds)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        top_bar = QWidget()
        t_layout = QHBoxLayout(top_bar)
        t_layout.setContentsMargins(0, 0, 0, 0)
        t_layout.setSpacing(10)

        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText(self.tr("search_binds"))
        self.search_entry.setClearButtonEnabled(True)
        self.search_entry.setMinimumHeight(36)
        self.search_entry.textChanged.connect(self.filter_binds)
        t_layout.addWidget(self.search_entry, 1)

        self.lbl_bind_hint = QLabel(self.tr("hint"))
        self.lbl_bind_hint.setStyleSheet("background-color: #10151f; border: 1px solid #1c2636; border-radius: 6px; padding: 6px 12px; color: #8b949e; font-size: 12px; font-weight: 600;")
        t_layout.addWidget(self.lbl_bind_hint)
        layout.addWidget(top_bar)

        self.lbl_bind_warn = QLabel(self.tr("warning_binds"))
        self.lbl_bind_warn.setStyleSheet("color: #d29922; font-size: 11px; font-style: italic;")
        layout.addWidget(self.lbl_bind_warn)

        self.binds_scroll = QScrollArea()
        self.binds_scroll.setWidgetResizable(True)
        self.binds_scroll.setStyleSheet("background-color: #0b0e14; border: none;")
        self.binds_scroll.viewport().setStyleSheet("background-color: #0b0e14; border: none;")

        self.binds_content = QWidget()
        self.binds_content.setStyleSheet("background-color: #0b0e14;")
        self.binds_layout = QVBoxLayout(self.binds_content)
        self.binds_layout.setContentsMargins(4, 4, 4, 4)
        self.binds_layout.setSpacing(8)

        self.binds_scroll.setWidget(self.binds_content)
        layout.addWidget(self.binds_scroll, 1)

    def setup_sys_page(self):
        page_layout = QHBoxLayout(self.page_sys)
        page_layout.setContentsMargins(18, 18, 18, 18)
        page_layout.setSpacing(16)

        self.group_sys_fov = QGroupBox(self.tr("sys_fov_frame"))
        fov_form = QFormLayout(self.group_sys_fov)
        fov_form.setContentsMargins(16, 20, 16, 16)
        fov_form.setSpacing(14)
        fov_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.lbl_sys_menu = QLabel(self.tr("sys_menu_label"))
        self.lbl_sys_menu.setMinimumWidth(220)
        self.sys_fov_ingame_entry = QLineEdit()
        self.sys_fov_ingame_entry.setPlaceholderText("79.32 - 112.33")
        self.sys_fov_ingame_entry.textChanged.connect(self._on_ingame_fov_change)
        self.sys_fov_ingame_entry.editingFinished.connect(self._clamp_ingame_fov)
        fov_form.addRow(self.lbl_sys_menu, self.sys_fov_ingame_entry)

        self.lbl_sys_config = QLabel(self.tr("sys_config_label"))
        self.sys_fov_config_entry = QLineEdit()
        self.sys_fov_config_entry.setPlaceholderText("50.0 - 80.0")
        self.sys_fov_config_entry.textChanged.connect(self._on_config_fov_change)
        self.sys_fov_config_entry.editingFinished.connect(self._clamp_config_fov)
        fov_form.addRow(self.lbl_sys_config, self.sys_fov_config_entry)

        self.system_entries["FieldOfView"] = self.sys_fov_config_entry

        self.fov_info = QLabel(self.tr("sys_fov_tooltip"))
        self.fov_info.setWordWrap(True)
        self.fov_info.setStyleSheet("""
            background-color: #0b0f15;
            color: #8b949e;
            border: 1px solid #1c2636;
            border-radius: 8px;
            padding: 14px;
            font-size: 12px;
            line-height: 1.5;
        """)
        fov_form.addRow(self.fov_info)
        page_layout.addWidget(self.group_sys_fov, 50)

        right_sys_col = QWidget()
        rs_layout = QVBoxLayout(right_sys_col)
        rs_layout.setContentsMargins(0, 0, 0, 0)
        rs_layout.setSpacing(12)

        self.group_sys_other = QGroupBox(self.tr("sys_other_frame"))
        other_form = QFormLayout(self.group_sys_other)
        other_form.setContentsMargins(16, 20, 16, 16)
        other_form.setSpacing(14)
        other_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.lbl_max_fps = QLabel(self.tr("MaxFPS") + ":")
        self.lbl_max_fps.setMinimumWidth(220)
        self.fps_entry = QLineEdit()
        other_form.addRow(self.lbl_max_fps, self.fps_entry)
        self.system_entries["MaxFPS"] = self.fps_entry

        self.lbl_scaling = QLabel(self.tr("OverscanScaling") + ":")
        self.scaling_entry = QLineEdit()
        other_form.addRow(self.lbl_scaling, self.scaling_entry)
        self.system_entries["OverscanScaling"] = self.scaling_entry

        rs_layout.addWidget(self.group_sys_other)

        self.group_backup = QGroupBox(self.tr("backup_card_title"))
        sa_layout = QVBoxLayout(self.group_backup)
        sa_layout.setContentsMargins(16, 20, 16, 16)
        sa_layout.setSpacing(10)

        self.lbl_backup_info = QLabel(self.tr("backup_info"))
        self.lbl_backup_info.setWordWrap(True)
        self.lbl_backup_info.setStyleSheet("color: #8b949e; font-size: 12px;")
        sa_layout.addWidget(self.lbl_backup_info)

        self.btn_reload_file = QPushButton(self.tr("btn_load"))
        self.btn_reload_file.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reload_file.clicked.connect(self.load_values)
        sa_layout.addWidget(self.btn_reload_file)

        rs_layout.addWidget(self.group_backup)
        rs_layout.addStretch()

        page_layout.addWidget(right_sys_col, 50)

    def copy_sens_all(self):
        data = {k: v.text().strip() for k, v in self.sens_entries.items()}
        clipboard = QApplication.clipboard()
        clipboard.setText(json.dumps(data, indent=2))
        self.lbl_preset_status.setText("✓ " + self.tr("copied"))
        QTimer.singleShot(3000, lambda: self.lbl_preset_status.setText(""))

    def paste_sens_all(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        try:
            data = json.loads(text)
            if isinstance(data, dict):
                for k, v in data.items():
                    if k in self.sens_entries:
                        self.sens_entries[k].setText(str(v))
                self.lbl_preset_status.setText("✓ " + self.tr("pasted"))
                QTimer.singleShot(3000, lambda: self.lbl_preset_status.setText(""))
        except Exception:
            pass

    def recalculate_sens(self):
        if self._calc_updating:
            return
        try:
            base_sens_str = self.base_sens_entry.text().replace(',', '.').strip()
            fov_str = self.calc_fov_entry.text().replace(',', '.').strip()
            mdc_str = self.mdc_entry.text().replace('%', '').replace(',', '.').strip()

            if not base_sens_str or not fov_str or not mdc_str:
                return

            base_sens = float(base_sens_str)
            fov_val = float(fov_str)
            mdc = float(mdc_str) / 100.0

            is_hfov = (self.fov_mode_cb.currentText() == self.tr("calc_mode_hfov"))
            min_fov, max_fov = (79.32, 112.33) if is_hfov else (50.0, 80.0)
            if fov_val > max_fov:
                fov_val = max_fov
                self._calc_updating = True
                self.calc_fov_entry.setText(f"{max_fov:.2f}".rstrip('0').rstrip('.'))
                self._calc_updating = False
            elif not can_reach_range(fov_str, min_fov, max_fov):
                fov_val = min_fov
                self._calc_updating = True
                self.calc_fov_entry.setText(f"{min_fov:.2f}".rstrip('0').rstrip('.'))
                self._calc_updating = False
            elif fov_val < min_fov:
                fov_val = min_fov
                self._calc_updating = True
                self.calc_fov_entry.setText(f"{min_fov:.2f}".rstrip('0').rstrip('.'))
                self._calc_updating = False

            if is_hfov:
                base_vfov = math.degrees(2 * math.atan(math.tan(math.radians(fov_val) / 2) / (16.0 / 9.0)))
            else:
                base_vfov = fov_val

            lowered_vfov = base_vfov if self.lowered_fov_cb.currentText() == self.tr("opt_default") else base_vfov / 1.25
            shoulder_vfov = base_vfov if self.shoulder_fov_cb.currentText() == self.tr("opt_default") else base_vfov / 1.25

            scope_vfovs = {
                "MouseSensitivity": lowered_vfov,
                "HipMouseSensitivity": shoulder_vfov,
                "IronSightsMouseSensitivity": base_vfov * 0.48,
                "ShortScopeMouseSensitivity": math.degrees(2 * math.atan(math.tan(math.radians(55) / 2) / 3.0)),
                "MediumScopeMouseSensitivity": math.degrees(2 * math.atan(math.tan(math.radians(55) / 2) / 8.0)),
                "LongScopeMouseSensitivity": math.degrees(2 * math.atan(math.tan(math.radians(55) / 2) / 12.0)),
                "PeepholeMouseSensitivity": math.degrees(2 * math.atan(math.tan(math.radians(55) / 2) / 9.0))
            }

            self._calc_updating = True
            for key in self.sens_keys:
                hidden_factor = HIDDEN_FACTORS.get(key, 1.0)
                target_vfov = scope_vfovs[key]

                if mdc == 0.0:
                    ratio = math.tan(math.radians(target_vfov) / 2) / math.tan(math.radians(base_vfov) / 2)
                else:
                    ratio = math.atan(mdc * math.tan(math.radians(target_vfov) / 2)) / math.atan(mdc * math.tan(math.radians(base_vfov) / 2))

                final_val = base_sens * hidden_factor * ratio

                if key in self.sens_entries:
                    self.sens_entries[key].setText(f"{final_val:.6f}")
            self._calc_updating = False

        except ValueError:
            self._calc_updating = False

    def _on_fov_mode_changed(self):
        is_hfov = (self.fov_mode_cb.currentText() == self.tr("calc_mode_hfov"))
        self.calc_fov_entry.setPlaceholderText("79.32 - 112.33" if is_hfov else "50.0 - 80.0")
        val_str = self.calc_fov_entry.text().replace(',', '.').strip()
        if val_str:
            try:
                val = float(val_str)
                if is_hfov:
                    if 50.0 <= val <= 80.0:
                        hfov = math.degrees(2 * math.atan(math.tan(math.radians(val) / 2) * (16.0 / 9.0)))
                        self.calc_fov_entry.setText(f"{hfov:.2f}")
                else:
                    if 79.32 <= val <= 112.33:
                        vfov = math.degrees(2 * math.atan(math.tan(math.radians(val) / 2) / (16.0 / 9.0)))
                        self.calc_fov_entry.setText(f"{vfov:.2f}")
            except ValueError:
                pass

    def _on_calc_fov_change(self, text):
        if self._calc_updating:
            return
        raw = text.replace(',', '.').strip()
        if raw:
            is_hfov = (self.fov_mode_cb.currentText() == self.tr("calc_mode_hfov"))
            min_fov, max_fov = (79.32, 112.33) if is_hfov else (50.0, 80.0)
            try:
                val = float(raw)
                if val > max_fov:
                    self._calc_updating = True
                    self.calc_fov_entry.setText(f"{max_fov:.2f}".rstrip('0').rstrip('.'))
                    self._calc_updating = False
                elif not can_reach_range(raw, min_fov, max_fov):
                    self._calc_updating = True
                    self.calc_fov_entry.setText(f"{min_fov:.2f}".rstrip('0').rstrip('.'))
                    self._calc_updating = False
            except ValueError:
                pass

    def _clamp_calc_fov(self):
        val_str = self.calc_fov_entry.text().replace(',', '.').strip()
        if not val_str:
            return
        try:
            val = float(val_str)
            is_hfov = (self.fov_mode_cb.currentText() == self.tr("calc_mode_hfov"))
            if is_hfov:
                if val < 79.32:
                    self.calc_fov_entry.setText("79.32")
                elif val > 112.33:
                    self.calc_fov_entry.setText("112.33")
            else:
                if val < 50.0:
                    self.calc_fov_entry.setText("50")
                elif val > 80.0:
                    self.calc_fov_entry.setText("80")
        except ValueError:
            pass

    def convert_external_sens(self):
        try:
            game = self.game_cb.currentText()
            sens_str = self.conv_sens_entry.text().replace(',', '.').strip()
            if not sens_str:
                return

            if not self.games_data or game not in self.games_data:
                return

            ext_sens = float(sens_str)
            mult_val = self.games_data[game]
            if isinstance(mult_val, (int, float)):
                multiplier = float(mult_val)
            elif isinstance(mult_val, dict) and "multiplier" in mult_val:
                multiplier = float(mult_val["multiplier"])
            else:
                return

            hunt_base_sens = ext_sens * multiplier
            self.base_sens_entry.setText(f"{hunt_base_sens:.6f}".rstrip('0').rstrip('.'))
        except ValueError:
            pass

    def _on_cm360_change(self):
        if self._cm_updating:
            return
        try:
            cm_str = self.cm360_entry.text().replace(',', '.').strip()
            dpi_str = self.dpi_entry.text().replace(',', '.').strip()
            if not cm_str or not dpi_str:
                return

            cm = float(cm_str)
            dpi = float(dpi_str)
            if cm <= 0 or dpi <= 0:
                return

            sens = 914.4 / (cm * HUNT_YAW * dpi)

            self._cm_updating = True
            self.base_sens_entry.setText(f"{sens:.6f}".rstrip('0').rstrip('.'))
            self._cm_updating = False
        except ValueError:
            self._cm_updating = False

    def _on_dpi_change(self):
        self.save_app_settings()
        if not self._cm_updating:
            self._on_cm360_change()

    def _on_base_sens_change(self):
        if self._cm_updating:
            return
        try:
            sens_str = self.base_sens_entry.text().replace(',', '.').strip()
            dpi_str = self.dpi_entry.text().replace(',', '.').strip()
            if not sens_str or not dpi_str:
                return

            sens = float(sens_str)
            dpi = float(dpi_str)
            if sens <= 0 or dpi <= 0:
                return

            cm = 914.4 / (sens * HUNT_YAW * dpi)

            self._cm_updating = True
            self.cm360_entry.setText(f"{cm:.2f}".rstrip('0').rstrip('.'))
            self._cm_updating = False
        except ValueError:
            self._cm_updating = False

    def _on_ingame_fov_change(self):
        if self._fov_updating:
            return
        val_str = self.sys_fov_ingame_entry.text().replace(',', '.').strip()
        if not val_str:
            self._fov_updating = True
            self.sys_fov_config_entry.setText("")
            self._fov_updating = False
            return
        try:
            val = float(val_str)
            if val > 112.33:
                val = 112.33
                self._fov_updating = True
                self.sys_fov_ingame_entry.setText("112.33")
                self._fov_updating = False
            elif not can_reach_range(val_str, 79.32, 112.33):
                val = 79.32
                self._fov_updating = True
                self.sys_fov_ingame_entry.setText("79.32")
                self._fov_updating = False

            if 79.32 <= val <= 112.33:
                vfov = math.degrees(2 * math.atan(math.tan(math.radians(val) / 2) / (16.0 / 9.0)))
                self._fov_updating = True
                self.sys_fov_config_entry.setText(f"{vfov:.6f}".rstrip('0').rstrip('.'))
                self._fov_updating = False
        except ValueError:
            self._fov_updating = False

    def _clamp_ingame_fov(self):
        if self._fov_updating:
            return
        val_str = self.sys_fov_ingame_entry.text().replace(',', '.').strip()
        if not val_str:
            return
        try:
            fov_in = float(val_str)
            clamped = False
            if fov_in < 79.32:
                fov_in = 79.32
                clamped = True
            elif fov_in > 112.33:
                fov_in = 112.33
                clamped = True

            self._fov_updating = True
            if clamped:
                self.sys_fov_ingame_entry.setText(f"{fov_in:.2f}")
            vfov = math.degrees(2 * math.atan(math.tan(math.radians(fov_in) / 2) / (16.0 / 9.0)))
            self.sys_fov_config_entry.setText(f"{vfov:.6f}".rstrip('0').rstrip('.'))
            self._fov_updating = False
        except ValueError:
            pass

    def _on_config_fov_change(self):
        if self._fov_updating:
            return
        val_str = self.sys_fov_config_entry.text().replace(',', '.').strip()
        if not val_str:
            self._fov_updating = True
            self.sys_fov_ingame_entry.setText("")
            self._fov_updating = False
            return
        try:
            val = float(val_str)
            if val > 80.0:
                val = 80.0
                self._fov_updating = True
                self.sys_fov_config_entry.setText("80")
                self._fov_updating = False
            elif not can_reach_range(val_str, 50.0, 80.0):
                val = 50.0
                self._fov_updating = True
                self.sys_fov_config_entry.setText("50")
                self._fov_updating = False

            if 50.0 <= val <= 80.0:
                hfov = math.degrees(2 * math.atan(math.tan(math.radians(val) / 2) * (16.0 / 9.0)))
                self._fov_updating = True
                self.sys_fov_ingame_entry.setText(f"{hfov:.2f}".rstrip('0').rstrip('.'))
                self._fov_updating = False
        except ValueError:
            self._fov_updating = False

    def _clamp_config_fov(self):
        if self._fov_updating:
            return
        val_str = self.sys_fov_config_entry.text().replace(',', '.').strip()
        if not val_str:
            return
        try:
            vfov = float(val_str)
            clamped = False
            if vfov < 50.0:
                vfov = 50.0
                clamped = True
            elif vfov > 80.0:
                vfov = 80.0
                clamped = True

            self._fov_updating = True
            if clamped:
                self.sys_fov_config_entry.setText(f"{vfov:.6f}".rstrip('0').rstrip('.'))
            hfov = math.degrees(2 * math.atan(math.tan(math.radians(vfov) / 2) * (16.0 / 9.0)))
            self.sys_fov_ingame_entry.setText(f"{hfov:.2f}".rstrip('0').rstrip('.'))
            self._fov_updating = False
        except ValueError:
            pass

    def refresh_presets(self):
        presets = []
        excluded_files = ["games_sens.json", "app_settings.json"]
        if os.path.exists(self.config_dir):
            for filename in os.listdir(self.config_dir):
                if filename in excluded_files:
                    continue
                if filename.endswith(".json"):
                    presets.append(filename[:-5])

        self.preset_cb.blockSignals(True)
        self.preset_cb.clear()
        self.preset_cb.addItems(presets)
        if self.last_preset_str in presets:
            self.preset_cb.setCurrentText(self.last_preset_str)
        elif presets:
            self.preset_cb.setCurrentIndex(0)
            self.last_preset_str = presets[0]
        else:
            self.last_preset_str = ""
        self.preset_cb.blockSignals(False)

    def on_preset_selected(self):
        self.last_preset_str = self.preset_cb.currentText()
        self.save_app_settings()

    def new_preset(self):
        name, ok = QInputDialog.getText(self, self.tr("btn_preset_new"), self.tr("prompt_new_preset"))
        if ok and name:
            clean_name = re.sub(r'[\\/*?:"<>|]', "", name).strip()
            if clean_name:
                self.preset_cb.addItem(clean_name)
                self.preset_cb.setCurrentText(clean_name)
                self.action_save_preset()
                self.refresh_presets()
            else:
                QMessageBox.warning(self, self.tr("title_error"), self.tr("msg_preset_err"))

    def action_delete_preset(self):
        preset_name = self.preset_cb.currentText()
        if not preset_name:
            return
        ans = QMessageBox.question(
            self,
            self.tr("btn_preset_del"),
            self.tr("msg_preset_del_confirm").format(name=preset_name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if ans == QMessageBox.StandardButton.Yes:
            path = os.path.join(self.config_dir, f"{preset_name}.json")
            try:
                if os.path.exists(path):
                    os.remove(path)
                self.last_preset_str = ""
                self.refresh_presets()
                self.save_app_settings()
            except Exception as e:
                QMessageBox.critical(self, self.tr("title_error"), str(e))

    def action_save_preset(self):
        preset_name = self.preset_cb.currentText()
        if not preset_name:
            QMessageBox.warning(self, self.tr("title_warning"), self.tr("msg_preset_err"))
            return

        data = {
            "sens": {k: v.text().strip() for k, v in self.sens_entries.items()},
            "sys": {k: v.text().strip() for k, v in self.system_entries.items()},
            "binds": self.current_binds
        }

        path = os.path.join(self.config_dir, f"{preset_name}.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            self.save_app_settings()
            self.refresh_presets()

            self.lbl_preset_status.setText("✓")
            QTimer.singleShot(3000, lambda: self.lbl_preset_status.setText(""))
        except Exception as e:
            QMessageBox.critical(self, self.tr("title_error"), str(e))

    def action_load_preset(self):
        preset_name = self.preset_cb.currentText()
        if not preset_name:
            return
        path = os.path.join(self.config_dir, f"{preset_name}.json")
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for k, val in data.get("sens", {}).items():
                if k in self.sens_entries:
                    try:
                        self.sens_entries[k].setText(str(val))
                    except Exception:
                        pass

            for k, val in data.get("sys", {}).items():
                if k in self.system_entries:
                    try:
                        self.system_entries[k].setText(str(val))
                    except Exception:
                        pass

            for raw_action, slots in data.get("binds", {}).items():
                if raw_action in self.current_binds and raw_action in self.bind_buttons:
                    try:
                        v1 = slots.get("1", "-1")
                        v2 = slots.get("2", "-1")
                        self.current_binds[raw_action]["1"] = v1
                        self.current_binds[raw_action]["2"] = v2
                        self.bind_buttons[raw_action]["btn1"].setText(self.get_key_name(v1))
                        self.bind_buttons[raw_action]["btn2"].setText(self.get_key_name(v2))
                    except Exception:
                        pass

            self.lbl_preset_status.setText("✔")
            QTimer.singleShot(3000, lambda: self.lbl_preset_status.setText(""))
        except Exception as e:
            QMessageBox.critical(self, self.tr("title_error"), str(e))

    def start_listening(self, action, slot, btn):
        if self.is_listening:
            return
        self.is_listening = True
        self.listening_action = action
        self.listening_slot = slot
        self.listening_btn = btn

        btn.setText(self.tr("listening"))
        btn.update_style(True)
        QTimer.singleShot(150, self._activate_input_capture)

    def _activate_input_capture(self):
        if not self.is_listening:
            return
        QApplication.instance().installEventFilter(self.input_filter)
        self.mouse_check_timer.start(30)

    def _check_extra_mouse_buttons(self):
        if not self.is_listening:
            return
        try:
            if ctypes.windll.user32.GetAsyncKeyState(0x05) & 0x8000:
                self.finish_bind("259")
            elif ctypes.windll.user32.GetAsyncKeyState(0x06) & 0x8000:
                self.finish_bind("260")
        except Exception:
            pass

    def stop_listening(self):
        self.mouse_check_timer.stop()
        QApplication.instance().removeEventFilter(self.input_filter)
        if self.listening_btn:
            self.listening_btn.update_style(False)
            current_dik = self.current_binds.get(self.listening_action, {}).get(self.listening_slot, "-1")
            self.listening_btn.setText(self.get_key_name(current_dik))
        self.is_listening = False
        self.listening_action = None
        self.listening_slot = None
        self.listening_btn = None

    def finish_bind(self, dik_code):
        if not self.is_listening:
            return
        action = self.listening_action
        slot = self.listening_slot
        btn = self.listening_btn

        if action in self.current_binds:
            self.current_binds[action][slot] = dik_code

        if btn:
            btn.dik_code = dik_code
            btn.setText(self.get_key_name(dik_code))

        self.stop_listening()

    def clear_bind(self, action, slot, btn):
        if self.is_listening:
            return
        if action in self.current_binds:
            self.current_binds[action][slot] = "-1"
        btn.dik_code = "-1"
        btn.setText(self.tr("empty"))

    def get_key_name(self, dik_code):
        if not dik_code or dik_code.startswith("-"):
            return self.tr("empty")
        lang_dict = KEYS.get(self.current_lang, KEYS["RU"])
        if dik_code in lang_dict:
            return lang_dict[dik_code]
        if dik_code in BASE_KEYS:
            return BASE_KEYS[dik_code]
        return f"[{dik_code}]"

    def filter_binds(self, query):
        q = query.strip().lower()
        for row_widget, cat_widget, raw_action, gui_name in self.bind_row_widgets:
            if not q:
                row_widget.setVisible(True)
            else:
                btn1_text = self.bind_buttons.get(raw_action, {}).get("btn1").text().lower() if raw_action in self.bind_buttons else ""
                btn2_text = self.bind_buttons.get(raw_action, {}).get("btn2").text().lower() if raw_action in self.bind_buttons else ""
                match = (
                    (q in raw_action.lower()) or
                    (q in self.tr(gui_name).lower()) or
                    (q in btn1_text) or
                    (q in btn2_text)
                )
                row_widget.setVisible(match)

        for cat_widget, cat_rows in self.category_widgets:
            any_visible = any(not r.isHidden() for r in cat_rows)
            cat_widget.setVisible(any_visible)

    def detect_hunt_attributes(self):
        paths_to_check = []
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
            if steam_path:
                paths_to_check.append(os.path.normpath(steam_path))
        except Exception:
            pass

        for sp in list(paths_to_check):
            vdf_path = os.path.join(sp, "steamapps", "libraryfolders.vdf")
            if os.path.exists(vdf_path):
                try:
                    with open(vdf_path, "r", encoding="utf-8") as f:
                        for line in f:
                            m = re.search(r'"path"\s*"([^"]+)"', line)
                            if m:
                                paths_to_check.append(os.path.normpath(m.group(1).replace("\\\\", "\\")))
                except Exception:
                    pass

        for drive in ["C", "D", "E", "F", "G"]:
            paths_to_check.append(f"{drive}:\\Program Files (x86)\\Steam")
            paths_to_check.append(f"{drive}:\\SteamLibrary")
            paths_to_check.append(f"{drive}:\\Steam")

        hunt_subpaths = [
            os.path.join("steamapps", "common", "Hunt Showdown 1896", "user", "profiles", "default", "attributes.xml"),
            os.path.join("steamapps", "common", "Hunt Showdown", "user", "profiles", "default", "attributes.xml"),
        ]

        for base in paths_to_check:
            for sub in hunt_subpaths:
                full = os.path.join(base, sub)
                if os.path.exists(full):
                    return os.path.normpath(full)
        return None

    def update_file_status(self):
        path = self.path_entry.text().strip() if hasattr(self, 'path_entry') else ""
        if path and os.path.exists(path):
            self.lbl_file_status.setText(self.tr("file_status_ok"))
            self.lbl_file_status.setStyleSheet("font-size: 11px; font-weight: 600; color: #3fb950;")
            self.path_entry.setToolTip(path)
        else:
            self.lbl_file_status.setText(self.tr("file_status_err"))
            self.lbl_file_status.setStyleSheet("font-size: 11px; font-weight: 600; color: #f85149;")
            self.path_entry.setToolTip(self.tr("file_status_err"))

    def auto_find_path(self):
        found = self.detect_hunt_attributes()
        if found:
            self.path_entry.setText(found)
            self.update_file_status()
            self.save_app_settings()
            self.load_values()
            QMessageBox.information(self, self.tr("title_info"), f"{self.tr('msg_found_hunt')}:\n{found}")
        else:
            self.update_file_status()
            QMessageBox.warning(self, self.tr("title_warning"), self.tr("msg_not_found_hunt"))

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "XML File", "", "XML Files (*.xml);;All Files (*.*)")
        if path:
            self.path_entry.setText(path)
            self.update_file_status()
            self.save_app_settings()
            self.load_values()

    def add_bind_row(self, raw_action, gui_name, val1, val2):
        self.current_binds[raw_action] = {"1": val1, "2": val2}

        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(12, 3, 12, 3)
        row_layout.setSpacing(10)

        disp_name = self.tr(gui_name)
        lbl = QLabel(disp_name + ":")
        lbl.setStyleSheet("color: #c9d1d9; font-size: 13px;")
        row_layout.addWidget(lbl, 1)

        btn1 = BindButton(raw_action, "1", self)
        btn1.dik_code = val1
        btn1.setText(self.get_key_name(val1))
        row_layout.addWidget(btn1)

        btn2 = BindButton(raw_action, "2", self)
        btn2.dik_code = val2
        btn2.setText(self.get_key_name(val2))
        row_layout.addWidget(btn2)

        self.bind_buttons[raw_action] = {"btn1": btn1, "btn2": btn2}
        self.binds_layout.addWidget(row_widget)
        return row_widget

    def load_values(self):
        self.update_file_status()
        path = self.path_entry.text().strip()
        if not path or not os.path.exists(path):
            if hasattr(self, 'lbl_status'):
                self.lbl_status.setText(self.tr("file_status_err"))
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.current_content = f.read()

            for key, entry in {**self.sens_entries, **self.system_entries}.items():
                match = re.search(fr'<Attr name="{key}" value="([^"]*)"\s*/>', self.current_content)
                if match:
                    entry.setText(match.group(1))

            # Clear previous binds widgets
            while self.binds_layout.count():
                item = self.binds_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            self.current_binds.clear()
            self.bind_buttons.clear()
            self.bind_row_widgets.clear()
            self.category_widgets.clear()

            # Table header
            header_widget = QWidget()
            h_layout = QHBoxLayout(header_widget)
            h_layout.setContentsMargins(12, 8, 12, 8)
            lbl_act = QLabel(self.tr("action"))
            lbl_act.setStyleSheet("font-weight: 700; color: #58a6ff; font-size: 13px;")
            lbl_b1 = QLabel(self.tr("btn1"))
            lbl_b1.setFixedWidth(130)
            lbl_b1.setStyleSheet("font-weight: 700; color: #58a6ff; font-size: 13px; text-align: center;")
            lbl_b2 = QLabel(self.tr("btn2"))
            lbl_b2.setFixedWidth(130)
            lbl_b2.setStyleSheet("font-weight: 700; color: #58a6ff; font-size: 13px; text-align: center;")
            h_layout.addWidget(lbl_act, 1)
            h_layout.addWidget(lbl_b1)
            h_layout.addWidget(lbl_b2)
            self.binds_layout.addWidget(header_widget)

            matches = re.finditer(r'<Attr name="PC_([a-zA-Z0-9_]+)_1" value="([^"]*)"\s*/>', self.current_content)
            found_actions = {}
            for m in matches:
                raw_action = m.group(1)
                lower_action = raw_action.lower()
                if any(bad in lower_action for bad in BLACKLIST):
                    continue
                val1 = m.group(2)
                v2_m = re.search(fr'<Attr name="PC_{raw_action}_2" value="([^"]*)"\s*/>', self.current_content)
                val2 = v2_m.group(1) if v2_m else ""
                found_actions[lower_action] = {"raw": raw_action, "v1": val1, "v2": val2}

            processed = set()
            for cat_key, items in GUI_LAYOUT:
                cat_widget = None
                cat_rows = []
                for gui_name, synonyms in items:
                    best_synonym = None
                    for syn in synonyms:
                        if syn in found_actions:
                            if not best_synonym:
                                best_synonym = syn
                            elif found_actions[syn]["v1"] != "-1" and found_actions[best_synonym]["v1"] == "-1":
                                best_synonym = syn

                    if best_synonym:
                        if cat_widget is None:
                            cat_widget = QLabel(self.tr(cat_key))
                            cat_widget.setStyleSheet("color: #8b949e; font-weight: 700; font-size: 13px; padding-top: 14px; padding-bottom: 4px;")
                            self.binds_layout.addWidget(cat_widget)
                            self.category_widgets.append((cat_widget, cat_rows))

                        data = found_actions[best_synonym]
                        row_w = self.add_bind_row(data["raw"], gui_name, data["v1"], data["v2"])
                        cat_rows.append(row_w)
                        self.bind_row_widgets.append((row_w, cat_widget, data["raw"], gui_name))

                        for syn in synonyms:
                            processed.add(syn)

            self.binds_layout.addStretch()
            self.lbl_status.setText(self.tr("status_loaded"))

        except Exception as e:
            QMessageBox.critical(self, self.tr("title_error"), str(e))

    def save_values(self):
        if not self.current_content:
            return

        for raw_action, slots in self.current_binds.items():
            if slots["1"].startswith("-") and slots["2"].startswith("-"):
                action_name = self.tr(raw_action.lower())
                msg = self.tr("msg_error_bind").format(action=action_name)
                QMessageBox.critical(self, self.tr("title_error"), msg)
                return

        new_content = self.current_content
        changes = False

        def replace_or_add(content, key, val):
            pattern = fr'(<Attr name="{key}" value=")([^"]*)("\s*/>)'
            if re.search(pattern, content):
                return re.sub(pattern, fr'\g<1>{val}\g<3>', content), True
            else:
                new_line = "\n    <Attr name=\"" + str(key) + "\" value=\"" + str(val) + "\"/>"
                if re.search(r'<Attributes[^>]*>', content):
                    content = re.sub(r'(<Attributes[^>]*>)', r'\g<1>' + new_line, content, count=1)
                    return content, True
                return content, False

        for key, entry in {**self.sens_entries, **self.system_entries}.items():
            new_content, ch = replace_or_add(new_content, key, entry.text().strip())
            if ch:
                changes = True

        for raw_action, slots in self.current_binds.items():
            new_content, ch1 = replace_or_add(new_content, f"PC_{raw_action}_1", slots["1"])
            new_content, ch2 = replace_or_add(new_content, f"PC_{raw_action}_2", slots["2"])
            if ch1 or ch2:
                changes = True

        if changes:
            target_file = self.path_entry.text().strip()
            try:
                is_readonly = False
                if os.path.exists(target_file):
                    try:
                        file_stat = os.stat(target_file)
                        if not (file_stat.st_mode & stat.S_IWRITE):
                            is_readonly = True
                            os.chmod(target_file, stat.S_IWRITE)
                    except Exception:
                        pass

                try:
                    backup_dir = os.path.join(self.config_dir, "backups")
                    os.makedirs(backup_dir, exist_ok=True)
                    backup_name = f"attributes_backup_{time.strftime('%Y%m%d_%H%M%S')}.xml"
                    shutil.copy2(target_file, os.path.join(backup_dir, backup_name))
                except Exception:
                    pass

                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                self.current_content = new_content

                if is_readonly:
                    try:
                        os.chmod(target_file, stat.S_IREAD)
                    except Exception:
                        pass

                self.lbl_status.setText(self.tr("status_saved"))
                QMessageBox.information(self, self.tr("title_info"), self.tr("msg_success"))

            except Exception as e:
                QMessageBox.critical(self, self.tr("title_error"), str(e))
        else:
            QMessageBox.information(self, self.tr("title_info"), self.tr("msg_no_changes"))

    def on_lang_change(self):
        self.current_lang = self.lang_cb.currentText()
        self.save_app_settings()
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("title"))

        # Sidebar navigation & file card
        self.btn_nav_sens.setText(self.tr("nav_sens"))
        self.btn_nav_binds.setText(self.tr("nav_binds"))
        self.btn_nav_sys.setText(self.tr("nav_sys"))
        self.btn_find.setText(self.tr("btn_auto_find"))
        self.btn_find.setToolTip(self.tr("btn_auto_find_tooltip"))
        self.btn_browse.setText(self.tr("browse"))
        self.update_file_status()

        # Top Bar
        curr_idx = self.stacked_widget.currentIndex()
        if curr_idx == 0:
            self.lbl_page_title.setText(self.tr("page_sens_title"))
            self.lbl_page_sub.setText(self.tr("page_sens_sub"))
        elif curr_idx == 1:
            self.lbl_page_title.setText(self.tr("page_binds_title"))
            self.lbl_page_sub.setText(self.tr("page_binds_sub"))
        elif curr_idx == 2:
            self.lbl_page_title.setText(self.tr("page_sys_title"))
            self.lbl_page_sub.setText(self.tr("page_sys_sub"))

        self.lbl_profile.setText(self.tr("profile_lbl"))
        self.btn_preset_new.setToolTip(self.tr("tooltip_preset_new"))
        self.btn_preset_apply.setToolTip(self.tr("tooltip_preset_apply"))
        self.btn_preset_save.setToolTip(self.tr("tooltip_preset_save"))
        self.btn_preset_del.setToolTip(self.tr("tooltip_preset_del"))
        self.btn_save_game.setText(self.tr("btn_save_game_header"))

        # Page 0 - Sens
        self.group_cm.setTitle(self.tr("calc_cm_frame"))
        self.lbl_calc_dpi.setText(self.tr("calc_dpi_label"))
        self.lbl_calc_cm.setText(self.tr("calc_cm_label"))

        self.group_import.setTitle(self.tr("calc_import_frame"))
        self.lbl_calc_game.setText(self.tr("calc_game_label"))
        self.lbl_calc_sens.setText(self.tr("calc_sens_label"))
        self.btn_reload_games.setText(self.tr("btn_reload_short"))
        self.btn_reload_games.setToolTip(self.tr("btn_reload_games_tooltip"))

        self.group_hunt_calc.setTitle(self.tr("calc_params_frame"))
        self.lbl_calc_base.setText(self.tr("calc_base_sens_label"))
        self.lbl_calc_fov_mode.setText(self.tr("calc_fov_mode"))

        curr_fov_idx = self.fov_mode_cb.currentIndex()
        self.fov_mode_cb.blockSignals(True)
        self.fov_mode_cb.clear()
        self.fov_mode_cb.addItems([self.tr("calc_mode_hfov"), self.tr("calc_mode_vfov")])
        self.fov_mode_cb.setCurrentIndex(curr_fov_idx if curr_fov_idx >= 0 else 0)
        self.fov_mode_cb.blockSignals(False)

        self.lbl_calc_fov.setText(self.tr("calc_fov_label"))
        self.lbl_calc_lowered.setText(self.tr("calc_lowered_label"))

        curr_l_idx = self.lowered_fov_cb.currentIndex()
        self.lowered_fov_cb.blockSignals(True)
        self.lowered_fov_cb.clear()
        self.lowered_fov_cb.addItems([self.tr("opt_default"), self.tr("opt_zoom")])
        self.lowered_fov_cb.setCurrentIndex(curr_l_idx if curr_l_idx >= 0 else 0)
        self.lowered_fov_cb.blockSignals(False)

        self.lbl_calc_shoulder.setText(self.tr("calc_shoulder_label"))

        curr_s_idx = self.shoulder_fov_cb.currentIndex()
        self.shoulder_fov_cb.blockSignals(True)
        self.shoulder_fov_cb.clear()
        self.shoulder_fov_cb.addItems([self.tr("opt_default"), self.tr("opt_zoom")])
        self.shoulder_fov_cb.setCurrentIndex(curr_s_idx if curr_s_idx >= 0 else 0)
        self.shoulder_fov_cb.blockSignals(False)

        self.lbl_calc_mdc.setText(self.tr("calc_mdc_label"))
        self.btn_calculate.setText(self.tr("btn_apply_1to1"))
        self.lbl_calc_notice.setText(self.tr("calc_notice"))

        self.sens_box.setTitle(self.tr("tab_sens"))
        self.btn_copy_all.setText(self.tr("btn_copy_all"))
        self.btn_paste_all.setText(self.tr("btn_paste_all"))
        for k, lbl in self.sens_labels.items():
            lbl.setText(self.tr(k))

        # Page 1 - Binds
        self.search_entry.setPlaceholderText(self.tr("search_binds"))
        self.lbl_bind_hint.setText(self.tr("hint"))
        self.lbl_bind_warn.setText(self.tr("warning_binds"))

        # Page 2 - Sys
        self.group_sys_fov.setTitle(self.tr("sys_fov_frame"))
        self.lbl_sys_menu.setText(self.tr("sys_menu_label"))
        self.lbl_sys_config.setText(self.tr("sys_config_label"))
        self.fov_info.setText(self.tr("sys_fov_tooltip"))

        self.group_sys_other.setTitle(self.tr("sys_other_frame"))
        self.lbl_max_fps.setText(self.tr("MaxFPS") + ":")
        self.lbl_scaling.setText(self.tr("OverscanScaling") + ":")

        self.group_backup.setTitle(self.tr("backup_card_title"))
        self.lbl_backup_info.setText(self.tr("backup_info"))
        self.btn_reload_file.setText(self.tr("btn_load"))

        # Status
        self.lbl_status.setText(self.tr("status_ready"))

        # Re-render binds with new language if loaded
        if self.current_content:
            self.load_values()


def main():
    try:
        myappid = 'hunt.showdown.configmanager.1896'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass
    app = QApplication(sys.argv)
    window = HuntConfigApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
