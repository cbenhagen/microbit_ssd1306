from ssd1306 import *

def draw_stamp(x, y, stamp, color, draw=1):
    global screen
    page, shiftPage = divmod(y, 8)
    ind = (x << 1) + (page << 7) + 1
    if ind>0:
        for col in range(0, 5):
            index = ind + (col << 1)
            b = (screen[index] | (stamp[col] << shiftPage)
                 ) if color else (screen[index
                                         ] & ~ (stamp[col] << shiftPage))
            pack_into(">BB", screen, index, b, b)
    ind += 128
    if ind < 513:
        for col in range(0, 5):
            index = ind + col * 2
            b = (screen[index] | (stamp[col] >> (8 - shiftPage))
                 ) if color else screen[index
                                        ] & ~ (stamp[col] >> (8 - shiftPage))
            pack_into(">BB", screen, index, b, b)
    if draw:
        offset = 2 if x != 0 else 0
        set_pos(x - (offset >> 1), page)
        i2c.write(ADDR, b'\x40' + screen[ind - 128 - offset:ind - 116])
        if page < 3:
            set_pos(x - (offset >> 1), page + 1)
            i2c.write(ADDR, b'\x40' + screen[ind - offset:ind + 14])
