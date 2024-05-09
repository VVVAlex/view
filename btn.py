#!/usr/bin/env python

import customtkinter as ctk
from common import font, font_size, load_image, create_img
from ctk_tooltip import CTkToolTip as ToolTip

list_images = (
    "info",
    "kol",
    "up",
    "down",
    "right",
    "left",
    "print",
    "all",
    "db",
    "pdf",
    "sloi_on",
    "sloi_off",
    "len_on",
    "len_off",
    "grid_on",
    "grid_off",
    "marker_on",
    "marker_off",
    "metki_on",
    "metki_off",
    "manualm",
    "avtom",
)


class Btn(ctk.CTkFrame):
    """Класс кнопок управления"""

    def __init__(self, frame, root):
        super().__init__(frame)
        self.root = root

        self.im_korabl = load_image("korab.png", im_2=None, size=(48, 24))
        font_ = ctk.CTkFont(family=f"{font}", size=font_size)
        self.img = create_img(list_images)

        pdx_l = (13, 0)
        pdx_r = (13, 0)
        w_4 = 50
        w_2 = 115
        h_4 = 40
        h_2 = 40

        self.btn_dict = {}
        self.btn_list = []

        row = 0
        self.bt_l = ctk.CTkButton(
            master=self,
            image=self.img['left'],
            text="",
            width=w_4,
            height=h_4,
            border_width=2,
            # fg_color='transparent',
            # fg_color="gray40", hover_color="gray25",
            command=self.root.board.next,
        )
        ToolTip(self.bt_l, message="Следующий экран")
        self.btn_list.append(self.bt_l)
        self.bt_l.grid(row=row, column=0, padx=pdx_r, pady=(2, 2), sticky="w")
        self.bt_r = ctk.CTkButton(
            master=self,
            image=self.img['right'],
            text="",
            width=w_4,
            height=h_4,
            border_width=2,
            command=self.root.board.prev,
        )
        ToolTip(self.bt_r, message="Предыдущий экран")
        self.btn_list.append(self.bt_r)
        self.bt_r.grid(row=row, column=1, padx=pdx_r, pady=(2, 2), sticky="w")
        self.bt_up = ctk.CTkButton(
            master=self,
            image=self.img['up'],
            text="",
            width=w_4,
            height=h_4,
            border_width=2,
            command=self.root.board.up,
        )
        ToolTip(self.bt_up, message="Увеличить масштаб")
        self.btn_list.append(self.bt_up)
        self.bt_up.grid(row=row, column=2, padx=pdx_r, pady=(2, 2), sticky="w")
        self.bt_down = ctk.CTkButton(
            master=self,
            image=self.img['down'],
            text="",
            width=w_4,
            height=h_4,
            border_width=2,
            command=self.root.board.down,
        )
        ToolTip(self.bt_down, message="Уменьшить масштаб")
        self.btn_list.append(self.bt_down)
        self.bt_down.grid(row=row, column=3, padx=pdx_r, pady=(2, 2), sticky="w")

        row += 1
        self.btn_1 = ctk.CTkButton(
            master=self,
            image=self.img['sloi_on'],
            text="",
            width=w_2,
            height=h_2,
            border_width=2,
            command=self.one_ceil,
        )
        self.btn_list.append(self.btn_1)
        self.btn_1.grid(
            row=row, column=0, columnspan=2, padx=pdx_l, pady=(2, 2), sticky="w"
        )
        self.btn_2 = ctk.CTkButton(
            master=self,
            image=self.img['len_off'],
            text="",
            width=w_2,
            height=h_2,
            border_width=2,
            font=font_,
            command=self.len_view,
        )
        self.btn_list.append(self.btn_2)
        self.btn_2.grid(
            row=row, column=2, columnspan=2, padx=pdx_l, pady=(2, 2), sticky="w"
        )

        row += 1
        self.btn_3 = ctk.CTkButton(
            master=self,
            image=self.img['grid_on'],
            text="",
            width=w_2,
            height=h_2,
            border_width=2,
            command=self.grid__,
        )
        self.btn_list.append(self.btn_3)
        self.btn_3.grid(
            row=row, column=0, columnspan=2, padx=pdx_l, pady=(2, 2), sticky="w"
        )
        self.btn_4 = ctk.CTkButton(
            master=self,
            image=self.img['marker_off'],
            text="",
            width=w_2,
            height=h_2,
            border_width=2,
            font=font_,
            command=self.dno,
        )
        self.btn_list.append(self.btn_4)
        self.btn_4.grid(
            row=row, column=2, columnspan=2, padx=pdx_l, pady=(2, 2), sticky="w"
        )

        row += 1
        self.btn_5 = ctk.CTkButton(
            master=self,
            image=self.img['metki_on'],
            text="",
            width=w_2,
            height=h_2,
            border_width=2,
            command=self.metka,
        )
        self.btn_list.append(self.btn_5)
        self.btn_5.grid(
            row=row, column=0, columnspan=2, padx=pdx_l, pady=(2, 2), sticky="w"
        )
        self.btn_6 = ctk.CTkButton(
            master=self,
            image=self.img['avtom'],
            text="",
            width=w_2,
            height=h_2,
            border_width=2,
            font=font_,
            command=self.root.avto_on_off,
        )
        self.btn_list.append(self.btn_6)
        self.btn_6.grid(
            row=row, column=2, columnspan=2, padx=pdx_l, pady=(2, 2), sticky="w"
        )

        row += 1
        self.btn_7 = ctk.CTkButton(
            master=self,
            image=self.img['all'],
            text="",
            width=w_2,
            height=h_2,
            border_width=2,
            command=self.root.board.full,
        )
        ToolTip(self.btn_7, message="Весе экраны")
        self.btn_list.append(self.btn_7)
        self.btn_7.grid(
            row=row, column=0, columnspan=2, padx=pdx_l, pady=(2, 2), sticky="w"
        )
        self.btn_8 = ctk.CTkButton(
            master=self,
            image=self.img['db'],
            text="",
            width=w_2,
            height=h_2,
            border_width=2,
            font=font_,
            command=self.root.op_db,
        )
        ToolTip(self.btn_8, message="Просмотр меток")
        self.btn_list.append(self.btn_8)
        self.btn_8.grid(
            row=row, column=2, columnspan=2, padx=pdx_l, pady=(2, 2), sticky="w"
        )

        row += 1
        self.btn_9 = ctk.CTkButton(
            master=self,
            image=self.img['print'],
            text="",
            width=w_2,
            height=h_2,
            border_width=2,
            command=self.root.print_pdf,
        )
        ToolTip(self.btn_9, message="Печать экрана")
        self.btn_list.append(self.btn_9)
        self.btn_9.grid(
            row=row, column=0, columnspan=2, padx=pdx_l, pady=(2, 2), sticky="w"
        )
        self.btn_10 = ctk.CTkButton(
            master=self,
            image=self.img['pdf'],
            text="",
            width=w_2,
            height=h_2,
            border_width=2,
            font=font_,
            command=self.root.view_pdf,
        )
        ToolTip(self.btn_10, message="Просмотр экрана в pdf")
        self.btn_list.append(self.btn_10)
        self.btn_10.grid(
            row=row, column=2, columnspan=2, padx=pdx_l, pady=(2, 2), sticky="w"
        )

        self.btn_open = ctk.CTkButton(
            master=self,
            image=self.im_korabl,
            text="Выбрать лог",
            width=80,
            text_color=("gray10", "gray90"),
            height=42,
            border_width=2,
            corner_radius=10,
            compound="bottom",
            border_color="#D35B58",
            font=font_,
            fg_color=("gray84", "gray25"),
            hover_color="#C77C78",
            command=self.root.open_log,
        )
        self.btn_open.grid(row=6, column=0, columnspan=4, padx=(13, 0), pady=20, sticky="swe")

        self.btn_dict["one_ceil"] = self.btn_1
        self.btn_dict["len_view"] = self.btn_2
        self.btn_dict["grid"] = self.btn_3
        self.btn_dict["dno"] = self.btn_4
        self.btn_dict["metka"] = self.btn_5
        self.btn_dict["avto_on_off"] = self.btn_6

        ToolTip(self.btn_open, alpha=0.85, message="Выберете файл лога \n или перетащите файл на экран")
        ToolTip(self.btn_dict["dno"], message="Нет подсветки")
        ToolTip(self.btn_dict["one_ceil"], message="Все цели")
        ToolTip(self.btn_dict["len_view"], message="Длительность  скрыта")
        ToolTip(self.btn_dict["metka"], message="Показать метки")
        ToolTip(self.btn_dict["grid"], message="Сетка выкл.")
        ToolTip(self.btn_dict["avto_on_off"], message="Автомасштаб")

        self.btn_set_state("disabled")

    def btn_set_state(self, state: str) -> None:
        """Установка статуса кнопок ('normal', 'disabled')"""
        for widget in self.btn_list:
            widget.configure(state=state)

    def dno(self, arg=None) -> None:
        """Cкрыть показать профиль"""
        (im, tip) = (
            (self.img['marker_off'], "Нет подсветки")
            if self.root.board.dno_
            else (self.img['marker_on'], "Подсветка вкл.")
        )
        self.btn_dict["dno"].configure(image=im)
        ToolTip(self.btn_dict["dno"], message=tip)
        self.root.board.dno()

    def one_ceil(self, arg=None) -> None:
        """Cкрыть показать все цели или одна цель"""
        (im, tip) = (
            (self.img['sloi_on'], "Все цели")
            if self.root.board.flag_on_point
            else (self.img['sloi_off'], "Одна цель")
        )
        self.btn_dict["one_ceil"].configure(image=im)
        ToolTip(self.btn_dict["one_ceil"], message=tip)
        self.root.board.one_ceil()

    def len_view(self, arg=None) -> None:
        """Cкрыть показать протяженность цели"""
        (im, tip) = (
            (self.img['len_off'], "Длительность  скрыта")
            if self.root.board.flag_on_lentht
            else (self.img['len_on'], "Длительность видна")
        )
        self.btn_dict["len_view"].configure(image=im)
        ToolTip(self.btn_dict["len_view"], message=tip)
        self.root.board.len_view()

    def metka(self, arg=None) -> None:
        """Cкрыть показать все метки"""
        (im, tip) = (
            (self.img['metki_off'], "Показать метки")
            if self.root.board.hide_
            else (self.img['metki_on'], "Скрыть метки")
        )
        self.btn_dict["metka"].configure(image=im)
        ToolTip(self.btn_dict["metka"], message=tip)
        self.root.board.metka()

    def grid__(self, arg=None) -> None:
        """Cкрыть показать сетку"""
        (im, tip) = (
            (self.img['grid_off'], "Сетка выкл.")
            if self.root.board.grid__
            else (self.img['grid_on'], "Сетка вкл.")
        )
        self.btn_dict["grid"].configure(image=im)
        ToolTip(self.btn_dict["grid"], message=tip)
        self.root.board.grid_()
