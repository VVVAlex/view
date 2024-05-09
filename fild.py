#!/usr/bin/env python

import math
import pathlib
import time
import tkinter as tk
import customtkinter as ctk
from ctk_popupmenu import CTkPopupMenu
from common import font, font_size, get_color, dict_color, load_image
from lupa import Lupa

color1 = fil = 'grey15'          # "blue"
color3 = color4 = "brown"
color_p = "#f59400"
color_t = "black"
color_d = "darkgreen"
color_dno_w = "grey85"
color_dno_b = "#505050"

offset_x = 15
offset_y = 12
offset_d = 43


class Fild(ctk.CTkFrame):
    """Класс холста просмотра + информ.лабель"""

    def __init__(self, parent, size_x, size_y):
        super().__init__(parent, corner_radius=0, border_width=2, border_color="grey75")
        self.parent = parent
        # self.mult = (1, 2, 5, 10, 20, 40, 50, 100, 200, 300, 400, 500)
        self.mult = (1, 2, 5, 10, 20, 40, 100, 200, 300, 400)
        self.step = (0, 5, 10, 15, 20, 25, 30, 35)
        self.W = size_x
        self.H = size_y  # 988, 400
        self.color__ = "gray85"
        self.bg = "#282828"
        self.dno_color = "#282828"
        self.thema = 1                               # Dark
        self.grid__ = 1
        self.m_top = 35  # 35 for notebook 7
        self.m_right = 65  # 55
        self.m_bottom = 35
        self.m_left = 20  # margin
        # self.font = ('tahoma', '10', 'bold')        # Helvetica bold italic
        self.font = ctk.CTkFont(family=f"{font}", size=font_size)
        self.n = 0
        # self.n__ = 11  # 9 for 6000
        self.n__ = 8
        self.scale = 0  # scale 0,1,2,3,4,5,6,7 +4000, 6000
        self.screen = 1  # текущий экран
        self.marker_on = 0
        self.fullscreen = 0
        self.id = None
        self.start = None

        self.k = self.mult[self.scale]
        self.flag_on_point = False  # показать все цели
        self.flag_on_lentht = False  # не показать длительность цели
        self.dno_ = False  # не подсвечивать рельеф при старте
        self.hide_ = True  # показать метки при старте
        self.imgbufer = []  # буфер для хранения изображений меток

        # VAR_C = namedtuple('VAR_C', 'schirvalue dolgvalue timevar tglub ampvar vsvar kursvar')
        # self.var = VAR_C(*(tk.StringVar() for _ in range(7)))

        # (self.schirvalue, self.dolgvalue, self.timevar,
        #  self.tglub, self.ampvar, self.vsvar, self.kursvar) = (tk.StringVar() for _ in range(7))
        # self.len_2 = self.parent.len_2
        self.len_2 = 0
        self.day = ''
        self.data = None
        self.n_screen = 0
        self.data_full = None
        # self.frame_canv = ctk.CTkFrame(self.parent.frame_left)
        w = self.W + self.m_right + self.m_left
        self.canvw = tk.Canvas(
            self,
            width=w,
            height=self.H + self.m_top + self.m_bottom,
            bg="#bbb",
            relief="ridge",
            bd=0,
        )  # beige
        self.canvw.config(highlightthickness=0, takefocus=1)
        self.pop_up(self.canvw)
        self.L = Lupa(self.parent)

    def pop_up(self, frame) -> None:
        pp = CTkPopupMenu(frame, width=160)
        im_1 = load_image("fon_w.png", im_2=None, size=(20, 20))
        im_2 = load_image("fon_b.png", im_2=None, size=(20, 20))
        im_e = load_image("exit.png", im_2=None, size=(20, 20))
        pp.configure(
            values=({'text': 'Светлый фон', 'command': self.fon_white, "image": im_1},
                    {'text': 'Темный фон', 'image': im_2, 'command': self.fon_black},
                    None,
                    {'text': 'Выход', 'command': self.parent.on_closing, 'image': im_e}))

    def fon_white(self) -> None:
        """Установить светлый фон"""
        self.bg = "beige"
        self.dno_color = color_dno_w
        self.thema = 0
        self.ch_fon()

    def fon_black(self) -> None:
        """Установить темный фон"""
        self.bg = "#282828"
        self.dno_color = color_dno_b
        self.thema = 1
        self.ch_fon()

    def ch_fon(self) -> None:
        """Смена фона холста"""
        self.canvw.bind("<Configure>", self.resize)
        # self.canvw.config(background=bg)
        color_dno = self.bg if not self.dno_ else self.dno_color
        self.canvw.itemconfigure("fild", fill=self.bg)
        self.canvw.itemconfigure("dno", fill=color_dno)
        self.dno_color = color_dno

    def run_(self, data: list = None) -> None:
        """Показ данных"""
        self.data_full = data  # all data
        self.canvw.pack(fill="both", expand=True)
        # self.frame_canv.pack(fill="both", expand=True)
        # self.frame_canv.grid(row=0, column=0, sticky="nsew")
        # self.L = Lupa(self.parent)
        self.L.withdraw()
        if self.data_full:
            self.n_screen = self.get_maxscreen()  # число экранов
            self.data = self.data_full[:self.W]
            self._calk_scale()
            self.parent.st_bar.set_curent_scr(self.screen)
            self.create_fild(self.canvw)
            self.text_axis(self.canvw)
            self.set_grid()
            # self.label_()
        self.bind_()

    def create_fild(self, canv: tk.Canvas) -> None:
        """Рисуем поле с осями"""
        w, h, m_top, m_right, m_bottom, m_left = (
            self.W,
            self.H,
            self.m_top,
            self.m_right,
            self.m_bottom,
            self.m_left,
        )
        line = canv.create_line
        canv.config(width=w + m_right + m_left, height=h + m_top + m_bottom)
        canv.create_rectangle(
            m_left, m_top, m_left + w, m_top + h, fill=self.bg, tags="fild"
        )
        line(
            m_left - 1,
            m_top,
            m_left - 1,  # axis
            m_top + h,
            width=2,
            fill=color4,
            tags="fild",
        )  # 4 left
        line(
            m_left + w + 2,
            m_top,
            m_left + w + 2,
            m_top + h,
            width=2,
            fill=color1,
            tags="fild",
        )  # 2 right
        line(
            m_left - 1,
            m_top,
            m_left + w + 1,  # 1 top
            m_top,
            width=2,
            fill=color1,
            tags="fild",
        )
        line(
            m_left - 2,
            m_top + h,  # 3 bottom
            m_left + w + 2,
            m_top + h,
            width=2,
            fill=color3,
            tags="fild",
        )
        for N in range(8):
            t = 10 if N % 2 == 0 else 7  # len tick short ant long
            line(
                m_left + w + 2,
                m_top + N * h // 8,
                m_left + w + 2 + t,
                m_top + N * h // 8,  # tick_Y
                width=2,
                fill=color1,
                tags="fild",
            )
            line(
                m_left + N * w // 8 - 2,
                m_top + h,
                m_left + N * w // 8 - 2,
                m_top + h + t,  # tick_X
                width=2,
                fill=color3,
                tags="fild",
            )

    def set_grid(self) -> None:
        """Показать сетку"""
        self.grid__ = 1  # grid on
        for N in range(8):
            self.canvw.create_line(
                self.m_left,
                self.m_top + N * self.H // 8,
                self.m_left + self.W,
                self.m_top + N * self.H // 8,  # grid_X
                width=1,
                dash=(3, 5),
                fill="gray55",
                tags="grid",
            )
            self.canvw.create_line(
                self.m_left + N * self.W // 8 - 2,
                self.m_top + self.H,
                self.m_left + N * self.W // 8 - 2,
                self.m_top,  # grid_Y
                width=1,
                dash=(3, 5),
                fill="gray55",
                tags="grid",
            )

    def clr_grid(self) -> None:
        """Убрать сетку"""
        self.grid__ = 0  # grid off
        self.canvw.delete("grid")

    def text_axis(self, canv: tk.Canvas) -> None:
        """Наносим на оси время и дату по Y всё по X только в начале"""
        w, h, m_top, m_left = self.W, self.H, self.m_top, self.m_left
        text = canv.create_text
        for i in range(5):
            txt_y = self.step[i] * self.k
            text(
                m_left + w + offset_x,
                m_top + i * h // 4,
                text=f"{txt_y:2d}",  # text_Y
                anchor="w",
                font=self.font,
                fill=color1,
                tags="text",
            )
        txt_x = time.strftime("%H:%M", self.data[0].timdata)
        self.day = txt_xd = time.strftime("%d.%m", self.data[0].timdata)
        if txt_x and txt_xd:
            text(
                m_left + w - 16,
                m_top + h + offset_y,
                text=f"{txt_x}/{txt_xd}",  # text_X_time0
                anchor="n",
                font=self.font,
                fill="black",
                tags="text",
            )  # brown
            # text(m_left + w + 25, m_top + h + ofset_y, text=f'/{txt_xd}',             # text_X_data0
            #      anchor='n', font=self.font, fill='darkgreen', tags='text')

    # data = [(format, glub, amp, lehth, timdata, shir, dolg, vs, kurs,...
    #         m_man, color_mm, m_avto, all_data)...] all_data = [(gl,amp,len),(gl1,amp1,len1)...]
    def set_data(self, canv: tk.Canvas) -> None:
        """Выводим данные и надписи на осях и метки"""
        w, h, m_top, m_left = self.W, self.H, self.m_top, self.m_left
        line = canv.create_line
        len2 = self.len_2
        # print(w, len(self.data), self.data)
        for j in range(w):
            if j < len(self.data):
                y = self.data[j].glub / self.k * h / 200
                if y < h and y != 0:
                    line(
                        m_left + w - j,
                        m_top + y,
                        m_left + w - j,
                        h + m_top - 2,
                        fill=self.dno_color,
                        tags="dno",
                    )  # дно рисуем раньше точек (иначе затрём нижние цели)
                if not self.flag_on_point:
                    all_data = self.data[j].all_data
                    for gl, amp, ln in all_data:
                        y1 = gl / self.k * h / 200
                        l1 = (ln / self.k * h / 20) if self.flag_on_lentht else 2
                        # color = get_color(amp)
                        color = dict_color.get(amp, 'grey55')
                        if y1 < h:
                            l_ = l1 // 2 if len2 else l1
                            y_len = l_ if l_ > 2 else 2
                            if y1 + y_len > h:
                                y_len = h - y1
                            line(
                                m_left + w - j,
                                m_top + y1,  # point_all
                                m_left + w - j,
                                m_top + y1 + y_len,
                                fill=color,
                                width="1",
                                tags="point_all",
                            )
                else:
                    if y < h and y != 0:
                        line(
                            m_left + w - j,
                            m_top + y,  # point one
                            m_left + w - j,
                            m_top + y + 2,
                            fill=color_p,
                            width="1",
                            tags="point",
                        )

                if j == w // 4 - 1:
                    self.create_tex(j, 3, 4)
                if j == w // 2 - 1:
                    self.create_tex(j, 1, 2)
                if j == w * 3 // 4 - 1:
                    self.create_tex(j, 1, 4)
                if j == w - 1:
                    self.create_tex(j, 0, 1)

                y = m_top + self.data[j].glub // self.k * h // 200  # int()
                if y > m_top + h:
                    y = m_top + h
                num = self.data[j].m_man.strip()  # [8]
                if num:  # мануал метка 8
                    color = self.data[j].color_mm  # [9]
                    self.create_manmetka(j, num, color, y)
                numa = self.data[j].m_avto.strip()  # [10]
                if numa:  # авто метка 10
                    self.create_avtometka(j, numa, y)

    def create_tex(self, j, numerator: int, denominator: int) -> None:
        w, h, m_top, m_left = self.W, self.H, self.m_top, self.m_left
        k = w * numerator // denominator
        txt_x = time.strftime("%H:%M", self.data[j].timdata)
        text = self.canvw.create_text
        text(
            m_left + k,
            m_top + h + offset_y,
            text=f"{txt_x}",  # text_X_time_
            anchor="n",
            font=self.font,
            fill=color_t,
            tags="text",
        )
        if self.day != time.strftime("%d.%m", self.data[j].timdata):
            txt_xd = time.strftime("%d.%m", self.data[j].timdata)
            text(
                m_left + k + offset_d,
                m_top + h + offset_y,
                text=f"/{txt_xd}",  # text_X_data1
                anchor="n",
                font=self.font,
                fill=color_d,
                tags="text",
            )
            self.day = txt_xd

    def create_avtometka(self, j: int, numa: str, y: int) -> None:
        """Нарисовать автоматическую метку"""
        # font = ("tahoma", "8")
        font_ = self.font
        self.canvw.create_line(
            self.m_left + self.W - j,
            y,
            self.m_left + self.W - j,
            self.m_top - 1,
            fill="DodgerBlue2",
            width=1,
            tags="avto_metka",
        )
        txt = time.strftime("%H:%M", self.data[j].timdata)  # %d.%m.%y
        self.canvw.create_text(
            self.m_left + self.W - 16 - j,
            self.m_top - 25,
            text=txt,
            anchor="w",
            font=font_,
            fill="RoyalBlue4",
            tags="texta",
        )
        self.canvw.create_text(
            self.m_left + self.W - j - 3,
            self.m_top - 10,
            text=numa,
            anchor="w",
            font=font_,
            fill="RoyalBlue4",
            tags="texta",
        )

    def create_manmetka(self, j: int, num: str, color: str, y: int) -> None:
        """Нарисовать ручную метку"""
        # font = ("tahoma", "8")
        font_ = self.font
        color_ = "red" if color == "red" else "spring green"
        self.canvw.create_line(
            self.m_left + self.W - j,
            y,
            self.m_left + self.W - j,
            self.m_top,
            fill=color_,
            width="1",
            tags="man_metka",
        )
        self.canvw.create_text(
            self.m_left + self.W - j - 3,
            self.m_top - 10,
            text=num,
            anchor="w",
            font=font_,
            fill=color_,
            tags="man_img",
        )

    def info(self, event) -> None:
        """Инициализация переменных по данным"""
        index = self.index_(event)
        if index is not None:
            data = (
                self.data[index].format_,
                self.data[index].ku,
                self.data[index].depth,
                self.data[index].rej,
                self.data[index].frek,
                self.data[index].cnt,
                self.data[index].m,
                self.data[index].vz,
                self.data[index].zg,
            )
            glub = self.data[index].glub / 10.0  # глубина
            all_data = self.data[index].all_data
            for gl, amp, _ in all_data:
                if glub == gl / 10.0:
                    self.color__ = get_color(amp)
            if glub == 0:
                self.color__ = "gray85"
            # glub_ = f'{glub} м'
            try:
                ampl = self.data[index].ampl
                lenth = self.data[index].lenth
            except KeyError:
                ampl = ""
                lenth = ""

            # if int(self.data[index].m):
            #     ampl = self.data[index].ampl  # амплитуда
            #     lenth = self.data[index].lenth  # длительность
            # else:
            #     ampl = ""
            #     lenth = ""

            self.parent.frame_r.u_panel.set_info(
                glub, ampl, lenth, data
            )  # вывод в нижний лабель (из show_bso) !!!
            t = time.strftime("%d.%m %H:%M:%S", self.data[index].timdata)
            sh = self.data[index].shir.split()  # schirota
            if not sh:
                sh = ""
            dol = self.data[index].dolg.split()  # dolgota
            if not dol:
                dol = ""
            vs = self.data[index].vs  # скорость судна
            # vs_ = f'{vs} уз'
            if not vs:
                vs = ""
            kurs = self.data[index].kurs  # курс
            # kurs_ = f'{kurs}{0xB0:c}'
            if not kurs:
                kurs = ""
            try:
                # sh = f"{sh[0]}{0xB0:c} {sh[1]}{0xB4:c} {sh[2]}"
                # dol = f"{dol[0]}{0xB0:c} {dol[1]}{0xB4:c} {dol[2]}"
                sh = f"{sh[0]} {sh[1]} {sh[2]}"
                dol = f"{dol[0]} {dol[1]} {dol[2]}"
            except IndexError:
                sh = dol = ""
            # maxg = 100000.0 if self.metr_ else 6553.5
            if glub < 6000:  # maxg
                self.parent.head.set_(t, sh, dol, vs, kurs)
                return
        # self.clr_var()

    # def clr_var(self) -> None:
    #     """Очистка полей данных"""
    #     for var in self.var:
    #         var.set("")
        # self.parent.clr_var_h()        # очищаем нижний лабель (из show_bso)   !!!

    def index_(self, event) -> int:
        """Позиция в данных"""
        index = (
            (self.W + self.m_left) - event.x
            if event
            else (self.W + self.m_left) - self.start.x
        )
        if index < len(self.data):  # self.W
            return index

    def dno(self) -> None:
        """Cкрыть показать профиль"""
        self.dno_color = color_dno_b if self.thema else color_dno_w
        # self.dno_ = not self.dno_
        if self.dno_:
            self.dno_color = self.bg
        self.dno_ = not self.dno_
        self.canvw.itemconfigure("dno", fill=self.dno_color)
        if self.grid__:
            self.set_grid()
        self.parent.m_dno.set(1) if self.dno_ else self.parent.m_dno.set(0)

    def one_ceil(self) -> None:
        """Cкрыть показать все цели или одна цель"""
        self.flag_on_point = not self.flag_on_point
        self.update_data()

    def len_view(self) -> None:
        """Cкрыть показать протяженность цели"""
        self.flag_on_lentht = not self.flag_on_lentht
        self.update_data()
        self.parent.view_len.set(
            1
        ) if self.flag_on_lentht else self.parent.view_len.set(0)

    def metka(self) -> None:
        """Cкрыть показать все метки"""
        self.hide_ = not self.hide_
        self.update_data()
        self.parent.m_hide.set(1) if self.hide_ else self.parent.m_hide.set(0)

    def grid_(self) -> None:
        """Cкрыть или показать сетку"""
        self.clr_grid() if self.grid__ else self.set_grid()
        self.parent.m_grid.set(1) if self.grid__ else self.parent.m_grid.set(0)

    def next(self, arg=None) -> None:
        """На следующий экран"""
        if self.screen < self.n_screen:
            self.screen += 1
            self.datascreen()

    def prev(self, arg=None) -> None:
        """На предыдущий экран"""
        if self.screen > 1:
            self.screen -= 1
            self.datascreen()

    def up(self, arg=None) -> None:
        """Увеличить масштаб"""
        if self.scale < self.n__:  # 9 for 10000м
            self.scale += 1
            self.update_data()

    def down(self, arg=None) -> None:
        """Уменьшить масштаб"""
        if self.scale > 0:
            self.scale -= 1
            self.update_data()

    def full(self, arg=None) -> None:
        """Полный экран"""
        if self.parent.view_data:
            self.enter_() if self.fullscreen else self._dataFullscreen()
            for v in ("avto_metka", "texta", "man_metka", "man_img"):
                self.canvw.delete(v)
            # self.parent.tol_bar.config_btn()                                  # !!!

    def calk_data_lupa(self, x: int, y: int) -> list | None:
        """Подготовить данные для лупы"""
        """[Row(format_='DBK', glub=1477, ampl='0', lenth=0.48,
            timdata=time.struct_time(tm_year=2019, tm_mon=6, tm_mday=17, tm_hour=12, tm_min=5, tm_sec=19,
            tm_wday=0, tm_yday=168, tm_isdst=-1),
            shir='', dolg='', vs='', kurs='', vz='1500', zg='0.0', ku='15', depth='M', rej='R', frek='50',
            cnt=2, m='2', m_man='', color_mm='', m_avto='', all_data=[(1477, 20, 0.48), (1500, 62, 2.88)]), ...]"""
        x0 = self.W + self.m_left - x + 4
        y0 = y - self.m_top
        n = 40
        if x0 < 0 or y0 < 0 or y0 > self.H + self.m_top:
            return
        data = self.data[x0 - n // 2:x0 + n // 2]
        return data

    def _view_lupa(self, event) -> None:
        """Показать окно лупы"""
        self.bind_lupa()
        data = self.calk_data_lupa(event.x, event.y)
        if data:
            self.L.lenth = True if self.flag_on_lentht else False
            # geom = self.parent.get_geometry_root()
            geom = self.canvw.winfo_rootx(), self.canvw.winfo_rooty()
            # print(geom)
            # print(event.x, event.y)
            self.L.focus_force()
            self.L.geometry(f"+{geom[0] + event.x - 100}+{geom[1] + event.y - 100}")
            # print(self.L.geometry())
            # self.L.geometry(f"+{int(geom[1]) + event.x - 100}+{int(geom[2]) + event.y - 20}")
            # self.L.geometry(f"+{int(geom[1]) + event.x + 15}+{int(geom[2]) + event.y + 25}")
            self.L.deiconify()
            y0 = event.y - self.m_top
            self.L.draw(self.k, self.H, y0, data)

    def _move_lupa(self, event) -> None:
        """Переместить окно лупы"""
        self._view_lupa(event)
        self.canvw.bind("<ButtonPress-1>", self._view_lupa)

    def re_view_lupa(self, event) -> None:
        """Переместить окно лупы при шелчке внутри лупы"""
        s = self.L.geometry().split("+")  # lupa относительно экрана
        x, y = int(s[1]), int(s[2])
        new = f"+{x + event.x - 100}+{y + event.y - 100}"
        g = self.parent.geometry()
        # g = self.parent.get_geometry_root()
        x1, y1 = int(g[1]), int(g[2])
        data = self.calk_data_lupa(x - x1 + 100, y - y1)
        xx = x1 + self.W
        yy = y1 + self.H
        if (
            x + event.x < xx
            and x1 < x + event.x + self.m_left - 100
            and yy + self.m_top + 100 > y + event.y > y1 + 100
        ):
            self.L.geometry(new)
        if data:
            y0 = y - y1 - self.m_top + 20
            self.L.draw(self.k, self.H, y0, data)
        else:
            self.L.clr()

    def destroy_lupa(self, event=None) -> None:
        """Убрать лупу"""
        self.canvw.unbind_all("<Escape>")
        self.canvw.unbind("<B1-Motion>")
        self.L.unbind("<ButtonPress-1>")
        self.L.unbind("<ButtonRelease-1>")
        self.bind_()
        self.L.destroy_()

    def next_one(self, event) -> None:
        """Переместить маркер влево на 1px"""
        if self.start is not None:
            if self.W + self.m_left + 1 > self.start.x > self.m_left:
                self.canvw.delete("marker")
                self.start.x -= 1
                self._marker(self.canvw, self.start)

    def prev_one(self, event) -> None:
        """Переместить маркер вправо на 1px"""
        if self.start is not None:
            if self.W + self.m_left > self.start.x > self.m_left - 1:
                self.canvw.delete("marker")
                self.start.x += 1
                self._marker(self.canvw, self.start)

    def bind_lupa(self, arg=None) -> None:
        self.unbind_()
        self.canvw.bind("<B1-Motion>", self._move_lupa)
        self.L.bind("<Double-1>", self.destroy_lupa)
        self.L.bind("<B1-Motion>", self.re_view_lupa)
        self.canvw.bind_all("<Escape>", self.destroy_lupa)
        self.L.bind("<ButtonRelease-1>", self.destroy_lupa)  # !!!

    def bind_(self, arg=None) -> None:
        self.canvw.bind("<ButtonPress-1>", self._on_marker)
        self.canvw.bind("<ButtonRelease-1>", self._release)
        self.canvw.bind("<B1-Motion>", self._move_marker)
        self.canvw.bind("<Double-1>", self.enter_)
        self.canvw.bind_all("<Escape>", self._clear_marker)
        self.canvw.bind("<Control-1>", self._view_lupa)
        self.bind_2()

    def bind_2(self, arg=None) -> None:
        self.canvw.bind_all("<Home>", self._home)
        self.canvw.bind_all("<End>", self._end)
        self.canvw.bind_all("<Up>", self.up)
        self.canvw.bind_all("<Down>", self.down)
        self.canvw.bind_all("<Left>", self.next)
        self.canvw.bind_all("<Right>", self.prev)
        self.canvw.bind_all("<Control-Left>", self.next_one)
        self.canvw.bind_all("<Control-Right>", self.prev_one)

    def unbind_(self, arg=None) -> None:
        self.canvw.unbind("<ButtonPress-1>")
        self.canvw.unbind("<ButtonRelease-1>")
        self.canvw.unbind("<B1-Motion>")
        self.canvw.unbind("<Double-1>")
        self.canvw.unbind("<Double-2>")
        self.canvw.unbind_all("<Escape>")
        self.unbind_2()

    def unbind_2(self, arg=None) -> None:
        self.canvw.unbind_all("<Home>")
        self.canvw.unbind_all("<End>")
        self.canvw.unbind_all("<Up>")
        self.canvw.unbind_all("<Down>")
        self.canvw.unbind_all("<Left>")
        self.canvw.unbind_all("<Right>")
        self.canvw.unbind_all("<Control-Left>")
        self.canvw.unbind_all("<Control-Right>")

    def move_metka(self, d: int) -> None:
        """Переместить метки на d"""
        for v in ("avto_metka", "texta", "man_metka", "man_img"):
            self.canvw.move(v, d, 0)

    def resize(self, event=None) -> None:
        """Изменение размера холста при измкнении размера окна"""
        if self.canvw.winfo_geometry() != "1x1+0+0":
            canvw, canvh = self.canvw.winfo_width(), self.canvw.winfo_height()
            self.W, self.H = (
                canvw - self.m_left - self.m_right,
                canvh - self.m_bottom - self.m_top,
            )
        self.reconfig()

    def enter_(self, arg=None) -> None:
        """Обработка поля ввода номера экрана"""
        # self.parent.tol_bar.config_btn(Lupstate='normal')
        # self.screen = scr
        try:
            self.screen = int(self.parent.st_bar.get_scr())
            if self.screen > self.n_screen:
                self.screen = self.n_screen
            if self.screen < 1:
                self.screen = 1
            self.canvw.focus_set()
            self.datascreen()
        except ValueError:
            self.parent.st_bar.del_scr()
        # try:
        #     self.screen = int(self.parent.st_bar.src_.get())
        #     if self.screen > self.n_screen:
        #         self.screen = self.n_screen
        #     if self.screen < 1:
        #         self.screen = 1
        #     self.canvw.focus_set()
        #     self.datascreen()
        # except ValueError:
        #     self.parent.src_.delete(0, tk.END)

    # ------------------------------------scroll----------------------

    def _end(self, event=None) -> None:
        """На последний экран"""
        self.screen = self.n_screen
        self.datascreen()

    def _home(self, event=None) -> None:
        """На первый экран"""
        self.screen = 1
        self.datascreen()

    def _next(self, event=None) -> None:
        """На следующий экран"""
        if self.screen < self.n_screen:
            self.screen += 1
            self.datascreen()

    def _prev(self, event=None) -> None:
        """На предыдущий экран"""
        if self.screen > 1:
            self.screen -= 1
            self.datascreen()

    def _dataFullscreen(self, event=None) -> None:
        """Полный экран"""
        k = self.n_screen
        data = self.data_full[0:self.W * k:k]
        self.fullscreen = 1
        # self.parent.src_["foreground"] = 'red'                        # !!!
        if data:
            self.reload_fild(data)
        if self.start:  # not None (=event) когда есть маркер
            self.canvw.delete("marker")

    def update_scr(self) -> None:
        """Обновить номер экрана при полном экране"""
        x = self.start.x  # координата маркера
        scr_w = int(self.n_screen * (x - 20) / self.W)
        scr = self.n_screen - scr_w
        self.screen = scr
        # self.parent.numbersrc_.set(scr)
        self.parent.st_bar.set_curent_scr(scr)

    def datascreen(self) -> None:
        """Новый срез данных"""
        self.fullscreen = 0
        if self.screen > self.n_screen:
            self.screen = self.n_screen
        data = self.data_full[self.W * (self.screen - 1):self.W * self.screen]
        # self.parent.src_["foreground"] = 'blue'                                # !!! stbar
        if data:
            self.reload_fild(data)

    def reload_fild(self, data: list) -> None:
        """Подготовка для перирисовки поля"""
        self.data = data
        # self.parent.numbersrc_.set(self.screen)                       # !!!
        self.parent.st_bar.set_curent_scr(self.screen)

        if self.parent.avtoscale:
            self._calk_scale()
        self.update_data()

    def update_data(self) -> None:
        """Перерисовать поле и оси"""
        for v in (
            "text",
            "point",
            "point_all",
            "dno",
            "marker",
            "grid",
            "man_metka",
            "man_img",
            "avto_metka",
            "texta",
        ):
            try:
                self.canvw.delete(v)
            except Exception:
                # print('canvw.delete Exept')
                pass
        self.k = self.mult[self.scale]
        self.text_axis(self.canvw)
        self.set_data(self.canvw)
        if not self.hide_:
            self.move_metka(self.W + self.m_right)
        if self.dno_:
            self.canvw.itemconfigure("dno", fill=self.dno_color)
        if self.grid__:
            self.set_grid()
        if self.marker_on:
            self._marker(self.canvw)

    def reconfig(self, data: list = None) -> None:
        """Перерисовка всего холста при изменении его размера"""
        if data:
            self.data_full = data
        self.canvw.delete("fild")
        self.create_fild(self.canvw)
        self.canvw.delete("marker")  # иначе будет на другой позиции
        scr = self.get_maxscreen()

        # self.parent.stbar_scr.set(f'Число экранов = {scr}')           # !!!
        self.parent.st_bar.set_scr_info(scr)
        self.datascreen()  # вместо update_data() иначе не полностью перерисовываются данные

    # -----------------------------------------------------------------------

    def delete_data(self) -> None:
        """Очищаем поле"""
        for v in (
            "text",
            "point",
            "point_all",
            "dno",
            "marker",
            "grid",
            "man_metka",
            "man_img",
            "avto_metka",
            "texta",
        ):
            try:
                self.canvw.delete(v)
            except Exception:
                pass

    def _marker(self, canv, event=None) -> None:
        """Рисуем маркер"""
        color_m = "green"
        color_md = "magenta"  # red
        x = event.x if event else self.start.x
        y = self.m_top
        h = self.H
        line = canv.create_line
        line(x, y, x, y + h, width=1, fill=color_m, tags="marker")
        line(x + 1, y, x + 1, y + 5, width=1, fill=color_md, tags="marker")
        line(x + 2, y, x + 2, y + 3, width=1, fill=color_md, tags="marker")
        line(x - 1, y, x - 1, y + 5, width=1, fill=color_md, tags="marker")
        line(x - 2, y, x - 2, y + 3, width=1, fill=color_md, tags="marker")
        line(x + 1, y + h, x + 1, y + h - 5, width=1, fill=color_m, tags="marker")
        line(x + 2, y + h, x + 2, y + h - 3, width=1, fill=color_m, tags="marker")
        line(x - 1, y + h, x - 1, y + h - 5, width=1, fill=color_m, tags="marker")
        line(x - 2, y + h, x - 2, y + h - 3, width=1, fill=color_m, tags="marker")
        index = self.index_(event)  # light marker
        if index is not None:
            try:
                dat = self.data[index].glub / self.k * h / 200  # [1]
                if dat > h - 5:
                    dat = h - 5
                line(x, y + 5, x, y + dat, fill=color_md, tags="marker")
            except Exception:
                pass
        self.info(event)

    def update_screen(self, event) -> None:
        """Перейти на следующий или предыдущий экран"""
        if event.x <= self.m_left and self.m_top + self.H > event.y > self.m_top:
            self._next()
        if (
            event.x >= self.W + self.m_left
            and self.m_top + self.H > event.y > self.m_top
        ):
            self._prev()

    def a_cancel(self) -> None:
        """Отвязать пролистывание экранов после repid()"""
        if self.id:
            self.canvw.after_cancel(self.id)
            self.id = None

    def _release(self, event=None):  # отпускание кнопки 1 мыши
        self.canvw.configure(cursor="")
        self.a_cancel()

    def notfild(self) -> None:
        """Пролистываем экраны когда курсор не в поле"""
        if self.fullscreen == 0:
            self.marker_on = 0
            if self.id is None:
                self.repid()

    def _on_marker(self, event) -> None:
        """Показать маркер"""
        self.canvw.delete("marker")
        self.start = event  # запомнить позицию маркера
        if (
            self.W + self.m_left + 1 > event.x > self.m_left - 1
            and self.m_top + self.H > event.y > self.m_top
        ):
            self.canvw.configure(cursor="cross")  # cross, sb_h_double_arrow
            self.marker_on = 1
            self._marker(self.canvw, event)  # нарисовать маркер
            self.a_cancel()
            if self.fullscreen:
                self.update_scr()
        else:
            self.notfild()
        self.L.destroy_()  # убрать лупу

    def _move_marker(self, event) -> None:
        """Переместить маркер"""
        if (
            self.W + self.m_left + 1 > event.x > self.m_left - 1
            and self.m_top + self.H > event.y > self.m_top
        ):
            self.canvw.delete("marker")
            self.marker_on = 1
            self.start = event  # запомнить позицию маркера
            self._marker(self.canvw, event)  # нарисовать маркер
            self.a_cancel()
            if self.fullscreen:
                self.update_scr()
        else:
            self.notfild()

    def _clear_marker(self, event=None) -> None:
        """Погасить маркер"""
        self.canvw.delete("marker")
        self.marker_on = 0
        # self.clr_var()                        # !!!

    def repid(self) -> None:
        """Если надо, то сменить экран через 0.6 сек на след./предыд."""
        self.update_screen(self.start)
        self.id = self.canvw.after(
            800, self.repid
        )  # возвращает целый id для after_cancel

    def _calk_scale(self) -> None:
        """Вычислить масштаб"""
        mx = [i.glub + i.lenth * 10 for i in self.data]  # !!!  int() + float()
        m = max(mx) / 10
        for i, j in (
            (1, 0),
            (2, 1),
            (5, 2),
            (10, 3),
            (20, 4),
            (40, 5),
            (50, 6),
            (100, 7),
            (200, 8),
            (300, 9),
            (400, 10),
            (500, 11),
        ):
            if m / i < 20:
                self.scale = j
                break

    def scal_(self, event=None) -> None:
        """Изменить масштаб экрана"""
        self._calk_scale()
        self.update_data()

    def get_scale(self) -> int:
        """Вернуть масштаб 0-7"""
        return self.scale

    def get_src(self) -> int:
        """Вернуть номер экрана"""
        return self.screen

    def get_data(self) -> list:
        """Вернуть текущие данные"""
        return self.data

    def get_maxscreen(self) -> int:
        """Вернуть число экранов"""
        n_screen = int(math.ceil(len(self.data_full) * 1.0 / self.W))
        self.n_screen = n_screen
        return n_screen

    def get_filename(self) -> pathlib.Path | str:
        """Вернуть путь[1] с именем файла[0] данных"""
        path = self.parent.get_path()
        return path
