#!/usr/bin/env python

import customtkinter as ctk
from common import font, font_size, load_image


class Info(ctk.CTkFrame):
    """Поле данных"""

    dict_ = {"L": "МГ", "M": "СГ", "H": "БГ", "R": "Ручной", "S": "Авто"}

    def __init__(self, frame):
        super().__init__(frame)
        self.im_korabl = load_image("korab.png", im_2=None, size=(48, 24))
        font_ = ctk.CTkFont(family=f"{font}", size=font_size)

        pw = 10
        pe = 10
        self.widget = []

        row = 0
        lb_ff = ctk.CTkLabel(
            master=self,
            text="Формат",
            width=120,
            font=font_,  # fg_color='grey35',
            padx=pw,
            pady=2,
            anchor="w",
        )
        lb_ff.grid(row=row, column=0, sticky="w", padx=3, pady=1)
        self.lb_ffg = ctk.CTkLabel(
            master=self,
            text="",  # fg_color='grey35',
            width=120,
            font=font_,
            padx=pe,
            pady=2,
            anchor="e",
        )
        self.lb_ffg.grid(row=row, column=1, sticky="e", padx=3, pady=1)
        self.widget.append(self.lb_ffg)
        row += 1
        lb_vz = ctk.CTkLabel(
            master=self,
            text="Скорость звука",
            width=100,
            font=font_,
            padx=pw,
            pady=2,
            anchor="w",
        )
        lb_vz.grid(row=row, column=0, sticky="w", padx=3, pady=1)
        self.lb_vzg = ctk.CTkLabel(
            master=self,
            text="",
            width=100,
            font=font_,
            padx=pe,
            pady=2,
            anchor="e",
        )
        self.lb_vzg.grid(row=row, column=1, sticky="e", padx=3, pady=1)
        self.widget.append(self.lb_vzg)
        row += 1
        lb_o = ctk.CTkLabel(
            master=self,
            text="Заглубление",
            width=100,
            font=font_,
            padx=pw,
            pady=2,
            anchor="w",
        )
        lb_o.grid(row=row, column=0, sticky="w", padx=3, pady=1)
        self.lb_og = ctk.CTkLabel(
            master=self,
            text="",
            width=100,
            font=font_,
            padx=pe,
            pady=2,
            anchor="e",
        )
        self.lb_og.grid(row=row, column=1, sticky="e", padx=3, pady=1)
        self.widget.append(self.lb_og)
        row += 1
        lb_dist = ctk.CTkLabel(
            master=self,
            text="Глубина",
            width=100,
            font=font_,
            padx=pw,
            pady=2,
            anchor="w",
        )
        lb_dist.grid(row=row, column=0, sticky="w", padx=3, pady=1)
        self.lb_glub = ctk.CTkLabel(
            master=self,
            text="",
            width=100,
            font=font_,
            padx=pe,
            pady=2,
            anchor="e",
        )
        self.lb_glub.grid(row=row, column=1, sticky="e", padx=3, pady=1)
        self.widget.append(self.lb_glub)
        row += 1
        lb_ut = ctk.CTkLabel(
            master=self,
            text="Уровень",
            width=100,
            font=font_,
            padx=pw,
            pady=2,
            anchor="w",
        )
        lb_ut.grid(row=row, column=0, sticky="w", padx=3, pady=1)
        self.lb_uv = ctk.CTkLabel(
            master=self,
            text="",
            width=100,
            font=font_,
            padx=pe,
            pady=2,
            anchor="e",
        )
        self.lb_uv.grid(row=row, column=1, sticky="e", padx=3, pady=1)
        self.widget.append(self.lb_uv)
        row += 1
        lb_lt = ctk.CTkLabel(
            master=self,
            text="Длительность",
            width=100,
            font=font_,
            padx=pw,
            pady=2,
            anchor="w",
        )
        lb_lt.grid(row=row, column=0, sticky="w", padx=3, pady=0)
        self.lb_lv = ctk.CTkLabel(
            master=self,
            text="",
            width=100,
            font=font_,
            padx=pe,
            pady=2,
            anchor="e",
        )
        self.lb_lv.grid(row=row, column=1, sticky="ew", padx=3, pady=0)
        self.widget.append(self.lb_lv)
        row += 1
        lb_et = ctk.CTkLabel(
            master=self,
            text="Эхо",
            width=100,
            font=font_,
            padx=pw,
            pady=2,
            anchor="w",
        )
        lb_et.grid(row=row, column=0, sticky="w", padx=3, pady=1)
        self.lb_ev = ctk.CTkLabel(
            master=self,
            text="",
            width=100,
            font=font_,
            padx=pe,
            pady=2,
            anchor="e",
        )
        self.lb_ev.grid(row=row, column=1, sticky="ew", padx=3, pady=1)
        self.widget.append(self.lb_ev)
        row += 1
        lb_upr = ctk.CTkLabel(
            master=self,
            text="Порог",
            width=100,
            anchor="w",
            font=font_,
            padx=10,
            pady=2,
        )
        lb_upr.grid(row=row, column=0, sticky="w", padx=3, pady=1)
        self.lb_uprg = ctk.CTkLabel(
            master=self,
            text="",
            width=100,
            font=font_,
            padx=pe,
            pady=2,
            anchor="e",
        )
        self.lb_uprg.grid(row=row, column=1, sticky="ew", padx=3, pady=1)
        self.widget.append(self.lb_uprg)
        row += 1
        lb_d = ctk.CTkLabel(
            master=self,
            text="Диапазон",
            width=100,
            anchor="w",
            font=font_,
            padx=10,
            pady=2,
        )
        lb_d.grid(row=row, column=0, sticky="w", padx=3, pady=1)
        self.lb_dg = ctk.CTkLabel(
            master=self,
            text="",
            width=100,
            font=font_,
            padx=pe,
            pady=2,
            anchor="e",
        )
        self.lb_dg.grid(row=row, column=1, sticky="ew", padx=3, pady=1)
        self.widget.append(self.lb_dg)
        row += 1
        lb_r = ctk.CTkLabel(
            master=self,
            text="Режим",
            width=100,
            anchor="w",
            font=font_,
            padx=10,
            pady=2,
        )

        lb_r.grid(row=row, column=0, sticky="w", padx=3, pady=1)
        self.lb_rg = ctk.CTkLabel(
            master=self,
            text="",
            width=100,
            font=font_,
            padx=pe,
            pady=2,
            anchor="e",
        )
        self.lb_rg.grid(row=row, column=1, sticky="ew", padx=3, pady=0)
        self.widget.append(self.lb_rg)
        row += 1
        lb_f = ctk.CTkLabel(
            master=self,
            text="Частота",
            width=100,
            anchor="w",
            font=font_,
            padx=10,
            pady=2,
        )
        lb_f.grid(row=row, column=0, sticky="w", padx=3, pady=1)
        self.lb_fg = ctk.CTkLabel(
            master=self,
            text="",
            width=100,
            font=font_,
            padx=pe,
            pady=2,
            anchor="e",
        )
        self.lb_fg.grid(row=row, column=1, sticky="ew", padx=3, pady=1)
        self.widget.append(self.lb_fg)

        self.clr_all()

    # @staticmethod
    # def cal_ampl(cod: int) -> float:
    #     """Вычислить амплитуды эхо в мв."""
    #     return round(1000 * cod * 3.3065 / 4096, 2)

    def clr_all(self) -> None:
        """Очистка данных"""
        for _ in self.widget:
            _.configure(text="")

    @staticmethod
    def cal_ampl(cod: int) -> float:
        """Вычислить амплитуды эхо в мв."""
        return round(1000 * cod * 2.5 / 255, 1)

    def set_info(self, glub, ampl, lenth, data) -> None:
        """Установка данных лога"""
        self.lb_glub.configure(text=f"{glub} м") if glub else self.lb_glub.configure(text="")
        amp = int(ampl)
        self.lb_uv.configure(text=f"{self.cal_ampl(amp)} мВ") if amp else self.lb_uv.configure(text="")
        # self.lb_uv.configure(text=f"{ampl}")
        # self.lb_lv.configure(text=f"{round(lenth, 2)} м")
        self.lb_lv.configure(text=f"{lenth} м") if lenth else self.lb_lv.configure(text="")
        self.lb_ffg.configure(text=f"{data[0]}")
        self.lb_uprg.configure(text=f"{data[1]}")
        self.lb_dg.configure(text=f"{self.dict_[data[2]]}")
        self.lb_rg.configure(text=f"{self.dict_[data[3]]}")
        self.lb_fg.configure(text=f"{data[4]} кГц")
        self.lb_ev.configure(text=f"{data[5]} / {data[6]}")
        self.lb_vzg.configure(text=f"{data[7]}")
        self.lb_og.configure(text=f"{data[8]}")
        # print(glub, ampl, lenth, data)
