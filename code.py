import board
import busio
import displayio
import terminalio

# Импорты KMK
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.extensions.media_keys import MediaKeys

# Импорты для Экрана и Подсветки
from kmk.extensions.pegasus_oled_ssd1306 import PegasusOLEDSSD1306
from kmk.extensions.RGB import RGB, AnimationModes

# 1. Создаем клавиатуру
keyboard = KMKKeyboard()

# 2. Добавляем модули (Макросы и Слои)
macros = Macros()
keyboard.modules.append(macros)
keyboard.modules.append(Layers())
keyboard.extensions.append(MediaKeys())

# -------------------------------------------------
# 3. НАСТРОЙКА ПИНОВ (Под вашу схему)
# -------------------------------------------------

# Строки (Rows) - подключены к A0, A1, A2, A3
keyboard.row_pins = (board.A0, board.A1, board.A2, board.A3)

# Столбцы (Cols) - подключены к RX, SCK, MOSI, MISO (D7, D8, D10, D9)
keyboard.col_pins = (board.D7, board.D8, board.D10, board.D9)

# Направление диодов (Строка -> Столбец)
keyboard.diode_orientation = DiodeOrientation.ROW2COL

# -------------------------------------------------
# 4. НАСТРОЙКА ЭКРАНА (OLED)
# -------------------------------------------------
# Подключен к D4 (SDA) и D5 (SCL)
oled_ext = PegasusOLEDSSD1306(
    i2c=busio.I2C(scl=board.D5, sda=board.D4),
    # По желанию можно вывести текст на экран:
    # oled_display_data={'label': 'MY MACROPAD'} 
)
keyboard.extensions.append(oled_ext)

# -------------------------------------------------
# 5. НАСТРОЙКА ПОДСВЕТКИ (RGB)
# -------------------------------------------------
# Подключена к D6 (TX)
rgb = RGB(
    pixel_pin=board.D6,
    num_pixels=16,         # У вас 16 светодиодов
    val_limit=100,         # Ограничение яркости (чтобы не перегреть)
    hue_default=100,       # Цвет по умолчанию (зеленоватый)
    sat_default=255,
    val_default=100,
    animation_mode=AnimationModes.RAINBOW # Режим радуги
)
keyboard.extensions.append(rgb)

# -------------------------------------------------
# 6. РАСКЛАДКА И МАКРОСЫ
# -------------------------------------------------

# Пример макроса "Сохранить" (Ctrl + S)
CTRL_S = KC.MACRO(Press(KC.LCTRL), Tap(KC.S), Release(KC.LCTRL))

# Пример макроса "Копировать" (Ctrl + C)
CTRL_C = KC.MACRO(Press(KC.LCTRL), Tap(KC.C), Release(KC.LCTRL))

# Пример макроса "Вставить" (Ctrl + V)
CTRL_V = KC.MACRO(Press(KC.LCTRL), Tap(KC.V), Release(KC.LCTRL))

# Пример макроса ввода текста
HELLO = KC.MACRO("Hello World!")

# Сама таблица кнопок (4x4)
keyboard.keymap = [
    [
        # --- Ряд 1 ---
        KC.N7,    KC.N8,    KC.N9,    KC.BSPC, 
        # --- Ряд 2 ---
        KC.N4,    KC.N5,    KC.N6,    HELLO,   # Тут макрос ввода текста
        # --- Ряд 3 ---
        KC.N1,    KC.N2,    KC.N3,    KC.ENTER,
        # --- Ряд 4 ---
        CTRL_C,   CTRL_V,   CTRL_S,   KC.MUTE  # Макросы Ctrl+C/V/S
    ]
]

if __name__ == '__main__':
    keyboard.go()
