#!/usr/bin/env python

import tkinter as tk
from tkinter import StringVar
import customtkinter as ctk
from common import font, font_size


class Head(ctk.CTkFrame):
    """Информационный верхний лабель"""

    def __init__(self, root):
        super().__init__(root, corner_radius=0, border_width=2, border_color="grey75")
        # self.root = root
        font_ = ctk.CTkFont(family=f'{font}', size=font_size)
        (self.t_var, self.sh_var, self.d_var,
         self.zona_var, self.skor_var, self.kurs_var) = (StringVar() for _ in range(6))     # self.zona_var !!!
        text_ = ('Широта', 'Долгота', 'Путевой угол', 'Путевая скорость')
        t_var_ = (self.sh_var, self.d_var, self.kurs_var, self.skor_var)
        # frame_ = self.root.frame_top
        # frame_.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        ctk.CTkLabel(self, text='Время', font=font_,
                     anchor=tk.CENTER).grid(
            row=0, column=0, padx=2, pady=2, sticky="we")
        ctk.CTkLabel(self, textvariable=self.t_var, font=font_).grid(
            row=1, column=0, padx=2, pady=2, sticky="we")
        for i, j in enumerate(zip(text_, t_var_), 1):
            ctk.CTkLabel(self, text=j[0], font=font_, anchor=tk.CENTER).grid(
                row=0, column=i, padx=2, pady=0, sticky="we")
            ctk.CTkLabel(self, textvariable=j[1], font=font_).grid(
                row=1, column=i, padx=2, pady=0, sticky="we")
        # self.set_utc()

    # def set_utc(self, t=True) -> None:
    #     """Установка UTC, u = временной сдвиг"""
    #     if t and self.root.zona:
    #         self.zona_var.set(f'Время  UTC ( {self.root.zona:+.1f} )')
    #     elif t:
    #         self.zona_var.set('Время  UTC ( 0.0 )')
    #     else:
    #         self.zona_var.set('Время  системное')

    @staticmethod
    def dop_gradus(st: str) -> str:
        """Вставляем знак градуса и минуту"""
        if st:
            d = st.split()
            d[0] = f'{d[0]}{0xB0:c} '
            d[1] = f'{d[1]}{0xB4:c} '
            st = ''.join(d)
        return st

    def set_sh(self, sh: str) -> None:
        """Установка широты"""
        sh = self.dop_gradus(sh)
        self.sh_var.set(f'{sh}')

    def set_d(self, d: str) -> None:
        """Установка долготы"""
        d = self.dop_gradus(d)
        self.d_var.set(f'{d}')

    def set_t(self, t: str) -> None:
        """Установка времени"""
        self.t_var.set(f'{t}')

    def set_vs(self, vs: str) -> None:
        """Установка путевой скорости"""
        self.skor_var.set(f'{vs} уз') if vs else self.skor_var.set('')

    def set_k(self, k: str) -> None:
        """Установка путевого угла"""
        self.kurs_var.set(f'{k}{0xB0:c}') if k else self.kurs_var.set('')

    def set_(self, *arg) -> None:
        """Обновляем StringVar"""
        self.set_sh(arg[1])
        self.set_d(arg[2])
        self.set_vs(arg[3])
        self.set_k(arg[4])
        self.set_t(arg[0])
        # self.set_utc(arg[5])
