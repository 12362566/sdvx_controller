import board
import digitalio
import keypad
import usb_hid
import time
import supervisor

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

from rotaryio import IncrementalEncoder

print("boot success")
# --- 原始引脚定义 ---
# l_a = board.GP14
# l_b = board.GP15
# r_c = board.GP16
# r_d = board.GP17
# b_l = board.GP18
# b_r = board.GP19
print("init_model")
# 将所有引脚组织成一个元组。
# 这些引脚的顺序对应于后续事件中的 key_number (0到5)
KEY_PINS = (
    board.GP14,  # Index 0: l_a
    board.GP15,  # Index 1: l_b
    board.GP16,  # Index 2: r_c
    board.GP17,  # Index 3: r_d
    board.GP18,  # Index 4: b_l
    board.GP19  # Index 5: b_r
)
L_RE = (board.GP20, board.GP21)
R_RE = (board.GP22, board.GP23)
l_encode = IncrementalEncoder(*L_RE, )
r_encode = IncrementalEncoder(*R_RE, )

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
    "l_RE": (Keycode.ONE, Keycode.TWO),
    "r_RE": (Keycode.NINE, Keycode.ZERO)
}
mouse  = Mouse(usb_hid.devices)

class key_status():
    lr_keys = None
    pos = 0
    ro_pos = 0
    lock_key_mode = False
    key_lock = False
    status = "none"

    def __init__(self,l_or_r, lr_keys, ro_pos,lock_key_mode, sensitivity=0):
        self.lc = l_or_r
        self.lr_keys = lr_keys
        self.pos = ro_pos
        self.ro_pos = ro_pos
        self.lock_key_mode = lock_key_mode
        self.sensitivity = sensitivity

    def check(self, pos):

            if abs(pos - self.ro_pos) > self.sensitivity:
                print(abs(pos - self.ro_pos))
                if pos > self.ro_pos:
                    self.rcp()
                else:
                    self.lcp()
            else:
                self.claencp()
            self.ro_pos = pos


    def lcp(self):
        if self.lock_key_mode == "key_press":
            if not self.key_lock:
                cbd.press(self.lr_keys[0])
                self.status = "l"
            else:
                self.claencp()
        elif self.lock_key_mode == "key_send" :
            cbd.send(self.lr_keys[0])
        elif self.lock_key_mode == "mouse":
            if self.lc=="l":
                mouse.move(x=10,y=0)
            else:
                mouse.move(x=0,y=10)

    def rcp(self):
        if self.lock_key_mode == "key_press":
            if not self.key_lock:
                cbd.press(self.lr_keys[0])
                self.status = "l"
            else:
                self.claencp()
        elif self.lock_key_mode == "key_send":
            cbd.send(self.lr_keys[0])
        elif self.lock_key_mode == "mouse":
            if self.lc == "l":
                mouse.move(x=-10, y=0)
            else:
                mouse.move(x=0, y=-10)
        ...
    def claencp(self):
        if self.status == "l":
            cbd.release(self.lr_keys[0])
        elif self.status == "r":
            cbd.release(self.lr_keys[1])
        self.key_lock = False
        self.status = "none"
l_pos = l_encode.position
r_pos = r_encode.position
cbd = Keyboard(usb_hid.devices)
l_ststus = key_status("l",keys_link['l_RE'],l_pos,"mouse")
r_status = key_status("r",keys_link['r_RE'],r_pos,"mouse")
while True:
    event = keys.events.get()
    l_cpos = l_encode.position
    r_cpos = r_encode.position
    if event:
        if event.pressed:
            # print("Pressed:", keys_link[event.key_number])
            cbd.press(keys_link[event.key_number])
        elif event.released:
            # print("Released:", keys_link[event.key_number])
            cbd.release(keys_link[event.key_number])
    l_ststus.check(l_cpos)
    r_status.check(r_cpos)


