#!/usr/bin/env python

import os
import customtkinter as ctk
import tkinter as tk
from PIL import Image
from tkinter import StringVar
from tkinter import ttk
from common import font, font_size          # , create_images

MAX_LEN_TXT = 34


class Footer(ctk.CTkFrame):
    """Строка состояния"""

    def __init__(self, root):
        self.root = root
        super().__init__(root)
        # parent = root.frame_bottom
        font_ = ctk.CTkFont(family=f'{font}', size=font_size)
        # self.im_tel = create_images(('open',), ('open2',))
        self.file_info = StringVar()
        self.scr_info = StringVar()
        self.num_scr = StringVar()
        self.txt_e = StringVar()
        self.file_info.set(" ")

        path_l = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', 'open2.png')
        path_d = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', 'open.png')
        my_image = ctk.CTkImage(light_image=Image.open(path_l),
                                dark_image=Image.open(path_d),
                                size=(20, 20))
        ctk.CTkLabel(self, textvariable=self.file_info,
                     image=my_image, compound=tk.LEFT, font=font_).pack(side=tk.LEFT, fill=tk.X)

        # ctk.CTkLabel(self, textvariable=self.file_info,
        #              image=self.im_tel.open, compound=tk.LEFT, font=font_,
        #              padx=10, pady=0).pack(side=tk.LEFT, fill=tk.X, ipadx=10)  # expand=Truу

        ttk.Sizegrip(self).pack(side=tk.RIGHT, padx=3)

        _src = ctk.CTkEntry(self, textvariable=self.num_scr,
                            width=68, font=font_,
                            takefocus=1, justify='center')
        _src.pack(side=tk.RIGHT, padx=10, pady=5)
        ctk.CTkLabel(self, textvariable=self.txt_e, font=font_,
                     padx=30, pady=0).pack(side=tk.RIGHT, fill=tk.X)
        ctk.CTkLabel(self, textvariable=self.scr_info,
                     width=68, font=font_).pack(side=tk.RIGHT, fill=tk.X)
        _src.bind("<Return>", self.root.board.enter_)

    def get_scr(self):
        return self.num_scr.get()
    
    def del_scr(self) -> None:
        self.num_src.set('')
    
    # def _enter(self, event=None) -> None:
    #     """Обработка поля ввода номера экрана"""
    #     try:
    #         scr = int(self.num_scr.get())
    #     except ValueError:
    #         scr = None
    #         self.num_scr.set('')
    #     if scr is not None:
    #         self.root.board.enter_(scr)

    def set_file(self, txt: str) -> None:
        """Файл галса"""
        # self.file_info.set('  Файл:  '  + txt)
        self.file_info.set(f'  Файл:  {txt}')

    def set_scr_info(self, txt: str) -> None:      # Path
        """Число экранов"""
        self.scr_info.set('Число экранов:    ' + str(txt))

    def set_curent_scr(self, txt: str) -> None:
        """Чекущий экран"""
        self.num_scr.set(txt)

    def set_txt(self, msg: str):
        """Надпись `экран`"""
        self.txt_e.set(msg)
