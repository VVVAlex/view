#!/usr/bin/env python

import tkinter as tk
from collections import namedtuple

from common import get_color


class Lupa(tk.Toplevel):
    """Лупа для увеличения"""

    def __init__(self, parent=None):  # 'beige' 'gray22' color=' beige',
        super().__init__(parent)
        # tk.Toplevel.__init__(self, parent)
        # self.wm_overrideredirect(True)
        self.overrideredirect(True)
        # self.overrideredirect(False)                   # можно update()
        self.wm_attributes("-alpha", 0.7)
        # self.wm_attributes("-topmost", "true")
        # self.lift()
        self.parent = parent
        canv = tk.Canvas(self, relief=tk.SUNKEN)  # bg=color,
        canv.config(width=200, height=200)
        canv.config(highlightthickness=0)
        canv.pack()
        # canv.bind('<Double-1>', self.onDoubleClick)
        self.can = canv
        self.can.create_line(0, 0, 200, 0, width=2, fill="gray22", tags="po")  # рамка
        self.can.create_line(0, 0, 0, 200, width=2, fill="gray22", tags="po")
        self.can.create_line(200, 0, 200, 200, width=2, fill="gray22", tags="po")
        self.can.create_line(0, 200, 200, 200, width=2, fill="gray22", tags="po")
        self.can.create_line(0, 100, 200, 100, width=1, fill="gray52", tags="po")  # x
        self.can.create_line(100, 0, 100, 200, width=1, fill="gray52", tags="po")  # y
        # self.lenth = True
        self.transient(parent)
        self.focus_force()
        self.resizable(False, False)
        self.bind("<Escape>", self.destroy_)

    def destroy_(self, arg=None) -> None:
        # self.destroy()
        self.withdraw()

    # def move_lupa(self, x, y):
    #     self.can.move('po', x, y)
    #     self.can.move('point', x, y)

    # def onDoubleClick(self, event):
    #     self.geometry("+40+80")

    def clr(self) -> None:
        self.can.delete("point")

    def draw(self, k: int, h: int, y0: int, data: namedtuple = None) -> None:
        """Отрисовка холста"""
        """[Row(format_='DBK', glub=1477, ampl='0', lenth=0.48,
            timdata=time.struct_time(tm_year=2019, tm_mon=6, tm_mday=17, tm_hour=12, tm_min=5, tm_sec=19,
            tm_wday=0, tm_yday=168, tm_isdst=-1),
            shir='', dolg='', vs='', kurs='', vz='1500', zg='0.0', ku='15', depth='M', rej='R', frek='50',
            cnt=2, m='2', m_man='', color_mm='', m_avto='', all_data=[(1477, 20, 0.48), (1500, 62, 2.88)]), ...]"""
        self.can.delete("point")
        dx = 6  # размер пикселя
        i = 0
        for ix in data:
            # print(ix.all_data)
            for gl, am, ln in ix.all_data:
                y = (gl / k * h / 200 - y0) * dx / 2
                l1 = (ln / k * h / 20) * dx / 2
                l_ = l1 // 2 if l1 > dx else dx
                color = get_color(am)
                x0 = 200 - dx * i
                x1 = 200 - dx * (i + 1)
                self.can.create_rectangle(
                    x0, y, x1 + 1, y + l_, fill=color, outline="", tags="point"
                )
            i += 1


if __name__ == "__main__":
    L = Lupa()
    # L.draw()
    L.mainloop()
