import board
import digitalio
import keypad
import usb_hid
import time

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from rotaryio import IncrementalEncoder
# --- 原始引脚定义 ---
# l_a = board.GP14
# l_b = board.GP15
# r_c = board.GP16
# r_d = board.GP17
# b_l = board.GP18
# b_r = board.GP19

# 将所有引脚组织成一个元组。
# 这些引脚的顺序对应于后续事件中的 key_number (0到5)
KEY_PINS = (
    board.GP14,  # Index 0: l_a
    board.GP15,  # Index 1: l_b
    board.GP16,  # Index 2: r_c
    board.GP17,  # Index 3: r_d
    board.GP18,  # Index 4: b_l
    board.GP19   # Index 5: b_r
)
L_RE = (board.GP20, board.GP21)
R_RE = (board.GP22, board.GP23)
l_encode =IncrementalEncoder(*L_RE,)
r_encode =IncrementalEncoder(*R_RE,)

# 使用 keypad.Keys 初始化按键组
keys = keypad.Keys(
    KEY_PINS,
    # 核心配置 1: 设置内部下拉电阻
    # 未按下时，引脚通过电阻保持低电平（0V）
    pull=True,
    # 核心配置 2: 按下时为高电平
    # 告诉 keypad 模块，我们期望的按下信号是高电平 (True)
    value_when_pressed=True
)
keys_link = {
    0: Keycode.A,
    1: Keycode.S,
    2: Keycode.K,
    3: Keycode.L,
    4: Keycode.C,
    5: Keycode.M,
    "l_RE":(Keycode.ONE,Keycode.TWO),
    "r_RE":(Keycode.NINE,Keycode.ZERO)
}
l_pos = l_encode.position
r_pos = r_encode.position
cbd = Keyboard(usb_hid.devices)
while True :
    event = keys.events.get()
    l_cpos = l_encode.position
    r_cpos = r_encode.position
    if event:
        if event.pressed:
            print("Pressed:", keys_link[event.key_number])
            cbd.press(keys_link[event.key_number])
        elif event.released:
            print("Released:", keys_link[event.key_number])
            cbd.release(keys_link[event.key_number])
    if l_cpos != l_pos:
        if l_cpos > l_pos:
            cbd.send(keys_link["l_RE"][1])
        else:
            cbd.send(keys_link["l_RE"][0])
        l_pos = l_cpos
        print("l_pos:", l_pos)
    if r_cpos != r_pos:
        if r_cpos > r_pos:
            cbd.send(keys_link["r_RE"][1])
        else:
            cbd.send(keys_link["r_RE"][0])
        r_pos = r_cpos
        print("r_pos:", r_pos)


