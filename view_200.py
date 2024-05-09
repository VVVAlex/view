#!/usr/bin/env python

import csv
import hashlib
import io
import os
import pathlib
import shutil
import time
import tkinter as tk
# import tkinter.messagebox as box
from ctkmessagebox import CTkMessagebox as Box
from collections import namedtuple
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD  # ,DND_ALL

from btn import Btn
from common import Row, bakdir, load_image
from ctk_tooltip import CTkToolTip as ToolTip
from db_api import request_data_all, request_data_coment
from db_show import ViewMetka
from fild import Fild
from head import Head
from info import Info
from pdf import Pdf
from stbar import Footer
from title import TitleTop

# from pathlib import Path

Width = 1240  # 1340
Height = 760
# ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue"


class RightFrame(ctk.CTkFrame):
    """"""

    def __init__(self, root, **kwargs):
        super().__init__(root, corner_radius=0,  # fg_color=('#c0c2c5', '#343638'),
                         border_width=2, border_color="grey75", **kwargs)
        self.rowconfigure((0, 1, 2, 3), weight=0)
        self.columnconfigure(0, weight=0)
        self.btn_panel = Btn(self, root)  # панель кнопок
        self.u_panel = Info(self)
        ttk.Separator(master=self).grid(row=0, column=0, padx=5, sticky="we")
        self.u_panel.grid(row=1, column=0, pady=0, padx=2, sticky="nsew")
        ttk.Separator(self).grid(row=2, column=0, padx=5, pady=(2, 10), sticky="we")
        self.btn_panel.grid(row=3, column=0, pady=2, padx=2, sticky="nsew")


class App(ctk.CTk, TkinterDnD.DnDWrapper):
    """Корневой класс приложения"""

    WIDTH = 1340  # 1340
    HEIGHT = 900  #

    def __init__(self, gals_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
        self.after(300, lambda: self.iconbitmap("setup.ico"))
        self.title("")  # убрать титле CTk
        # self.withdraw()
        # self.focus_force()
        self.geometry(f"{Width}x{Height}+100+0")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.minsize(1080, 680)  # (1080, 680)
        self.wm_state = True  # во весь экран True
        self.filename = None
        self.gals_name = gals_name

        self.s = ttk.Style()
        # print(self.s.theme_use())             # clam, alt, classic, default, vista, xpnative
        # print(self.s.theme_names())
        self.s.theme_use("clam")  # default
        ctk.set_appearance_mode("Dark")
        # ctk.set_appearance_mode("Light")
        if ctk.get_appearance_mode() == 'Dark':
            self.s.configure("TSizegrip", background="grey19")  # for TSizegrip
        self.im_korabl = load_image("korab.png", im_2=None, size=(48, 24))
        self.tbname = self.dbname = None
        self.view_data = None
        self.avtoscale = 1
        self.dir = "."
        self.path = pathlib.Path(os.path.abspath("."))
        self.veiwstate = "disabled"
        (
            self.h_bar,
            self.m_grid,
            self.view_len,
            self.m_dno,
            self.m_avto,
            self.m_hide,
        ) = (
            tk.IntVar(self, 1),
            tk.IntVar(self, 1),
            tk.IntVar(self, 0),
            tk.IntVar(self, 0),
            tk.IntVar(self, 1),
            tk.IntVar(self, 1),
        )
        self.view_db = None
        # w_scr = self.winfo_screenwidth() - 296
        height = App.HEIGHT + 230
        width = App.WIDTH + 400
        self.get_tmp_file()
        if self.filename:  # сразу открыть файл
            self.view_mem()
            self.get_db_tb_name(self.gals_name)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.head = Head(self)  # панель координат
        self.board = Fild(self, width, height)  # экран эхограммы
        self.st_bar = Footer(self)  # строка состояния
        self.head.grid(row=0, column=0, padx=(2, 0), sticky="we")
        self.head.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.st_bar.grid(row=2, column=0, columnspan=2, sticky="we")
        self.st_bar.grid_columnconfigure(0, weight=1)
        self.board.grid(row=1, column=0, sticky="nsew", padx=(2, 0), pady=1)
        # self.board.grid_rowconfigure(0, weight=1)  # minsize=80
        # self.board.grid_columnconfigure(0, weight=1)

        self.frame_r = RightFrame(self)
        self.frame_r.grid(row=0, column=1, rowspan=2, sticky="ns", padx=2)

        # self.deiconify()
        # self.wait_visibility()
        self.drop_target_register(DND_FILES)  # DND_ALL
        self.dnd_bind("<<Drop>>", self.open_log_drop)

    def open_log_drop(self, event):
        """Открытие лога перетаскиванием"""
        # print(event.data)
        self.filename = event.data[:]
        if self.filename[0] == '{' and self.filename[-1] == '}':
            self.filename = event.data[1:-1]
        if self.filename:
            self.get_db_tb_name(self.filename)
            self.view_mem()

    def get_tmp_file(self) -> None:
        """Получить временный файл"""
        cur_path = pathlib.Path("tmp_file")  # имя файл
        if self.gals_name:
            self.filename = cur_path.joinpath(
                bakdir, cur_path
            )  # файл обьединить с врем дир
            try:
                shutil.copyfile(self.gals_name, bakdir)
            except IOError:
                self.filename = None

    @staticmethod
    def rev_file(file_: str | pathlib.Path) -> io.StringIO:
        """Реверс файла и слив в файлоподобный объект"""
        out = io.StringIO()
        with open(file_) as f:
            head = f.readline()
            s_list = f.readlines()
            s_list.reverse()
            out.write(head)
            out.writelines(s_list)
        out.seek(0)
        del s_list
        return out

    def open_file(self, dir_=".") -> str | None:
        """Вернуть путь к файлу"""
        ftypes = [("CSV files", ".csv"), ("All files", "*")]
        oname = askopenfilename(initialdir=dir_, filetypes=ftypes)
        if oname:
            self.get_db_tb_name(oname)
            return oname

    def get_db_tb_name(self, oname: str) -> None:
        """Опредилить tbname и dbname"""
        # path = pathlib.Path(oname).parent.parent if self.old_log else pathlib.Path(oname).parent
        path = pathlib.Path(oname).parent
        if path.parts[-1] == "Исходные данные":
            path = path.parent
        # print(f'path = {path}')
        fname = pathlib.Path(oname).stem
        # print(f'fname = {fname}')
        md5 = hashlib.md5(fname.encode("utf-8")).hexdigest()
        self.tbname = f"tb_{md5}"
        modif = "_25" if "_25" in fname else ""  # !!
        self.dbname = path.joinpath(path.name + modif + ".db")
        # print(f'dbname = {self.dbname}')
        # self.tol_bar.btn['Оперативные отметки'].config(state='normal')

    def read_csv(self) -> tuple:  # [Generator, TextIO]
        """Читаем csv файл direct=True если просмотр с галса"""
        # with open(self.filename) as out:
        #     f_csv = (filds for filds in csv.DictReader(out))
        #     self.dir = pathlib.Path(self.filename).parent
        #     return f_csv, out
        try:
            out = open(self.filename)
            f_csv = (filds for filds in csv.DictReader(out))  # ({}, {}, ...)
        except OSError:
            out = []
            f_csv = None
        self.dir = pathlib.Path(self.filename).parent
        return f_csv, out

    def canvas_data(self) -> list[namedtuple]:
        """Формируем из файла gl_N.csv данные в виде
        data=[шапка,
        ('format_','glub','ampl','lenth',timdata','shir','dolg','vs','kurs'
        'vz','zg','ku','depth','rej','frek','cht','m','m_man','color_mm','m_avto',
        'g0','a0','l0','g1','a1','l1', ...),...]
        """
        f_csv, out = self.read_csv()
        if f_csv is None:
            return
        num_line = 0
        data = []
        for line_dict in f_csv:
            num_line += 1
            try:
                glub = int(line_dict["glub"])  # глубина * (1 or 10)
            except (ValueError, KeyError):
                glub = 0
            try:
                lenth = float(line_dict["lenth"])  # длительность
            except (ValueError, KeyError):
                lenth = 0
            try:
                cnt = int(line_dict["cnt"])  # число стопов
                if cnt > 20:
                    cnt = 20  # cnt
            except (ValueError, KeyError):
                cnt = 0
            try:
                timdata = time.strptime(
                    line_dict["timdata"], "%d.%m.%y %H:%M:%S"
                )  # объект time
            except Exception:
                timdata = ""
            try:
                all_data = [
                    (
                        int(line_dict[f"g{i}"]),
                        int(line_dict[f"a{i}"]),
                        float(line_dict.get(f"l{i}", 0)),
                    )
                    for i in range(cnt)
                ]
            except ValueError:
                all_data = []
            tupl = Row(
                line_dict["format_"],
                glub,
                line_dict["ampl"],
                lenth,
                timdata,
                line_dict["shir"],
                line_dict["dolg"],
                line_dict["vs"],
                line_dict["kurs"],
                line_dict["vz"],
                line_dict["zg"],
                line_dict["ku"],
                line_dict["depth"],
                line_dict["rej"],
                line_dict["frek"],
                cnt,
                line_dict["m"],
                line_dict["m_man"],
                line_dict["color_mm"],
                line_dict["m_avto"],
                all_data,
            )
            data.append(tupl)  # for canvas_show self.can_show.run_()
            if not num_line % 50:
                # self.frame_fild.update()
                self.board.update()

        if out:
            out.close()
        return data

    def open_log(self, arg=None):
        """Открыть файл лога"""
        self.filename = self.open_file(self.dir)
        if self.filename:
            self.view_mem()

    def view_mem(self, arg=None) -> None:
        """Просмотр данных arg=None если запуск из просмотра лога"""
        self.focus_force()
        # self.frame_fild.configure(cursor="watch")
        self.board.configure(cursor="watch")
        data = self.canvas_data()  # > 4.1 сек
        if data:
            if self.view_data is None:
                self.veiwstate = "normal"  # надо вызывать меню для
                self.board.run_(data)
                self.view_data = True
                self.update()
                self.board.canvw.bind("<Configure>", self.board.resize)
                s = self.geometry()  # дёргаю геометрию иначе при разворачивании
                # окна и востановление не сохраняется предыдущий размер ???
                l_ = s.split("+")[0].split("x")
                l_[0] = str(int(l_[0]) + 1)
                l_[1] = str(int(l_[1]) + 1)
                self.geometry("x".join(l_))
            else:
                self.board.reconfig(data)
            name = self.get_path()[0]  # filename
            if name:  # !!!
                self.st_bar.set_file(f"{name}")
                self.st_bar.txt_e.set("Экран")
            self.board.resize()
            self.focus_force()
            self.frame_r.btn_panel.btn_set_state("normal")
        else:
            # box.showerror("?", f"Не прочитать файл {self.filename}!")
            Box(title="", message=f'Не прочитать файл {self.filename}!',
                font=("Roboto Medium", -16), icon="cancel")
            self.board.delete_data()
            self.st_bar.txt_e.set("")
            self.frame_r.btn_panel.btn_set_state("disabled")
        # self.frame_fild.configure(cursor="")
        self.board.configure(cursor="")

    def get_path(self) -> tuple[pathlib.Path, str]:
        """Вернуть пуПечать экранать и имя файла с данными или None"""
        return self.filename, self.dir

    def print_pdf(self, event=None) -> None:
        """"""
        self.get_pdf()

    def view_pdf(self, event=None) -> None:
        """Открыть экран в Foxit"""
        self.get_pdf(1)

    def get_pdf_data(self) -> tuple:
        """Получить данные для pdf"""
        src = self.board.get_src()  # int номер экрана
        data = self.board.get_data()  # данные или None  # canvas_show
        filename = self.get_path()[0]  # имя файла с данными
        w = self.board.W  # текущая ширина холста 768
        scale = self.board.get_scale()  # текущий масштаб
        return w, data, src, scale, filename

    def get_pdf(self, verbose=None) -> None:
        """Сразу печатаем (verbose=None) или запускаем Foxit (verbose=1)"""
        if self.view_data:
            Pdf(self, verbose)

    def gethide_metka(self) -> tuple:
        """Вернуть нужно отображать метки и длительность в pdf или нет"""
        return self.m_hide.get(), self.view_len.get()

    def avto_on_off(self, arg=None) -> None:
        """Установиь сбросить автомасштаб"""
        if self.view_data:
            self.board.scal_()
            if not self.avtoscale:
                self.m_avto.set(1)
                self.frame_r.btn_panel.btn_dict["avto_on_off"].configure(
                    image=self.frame_r.btn_panel.img.avtom
                )
                ToolTip(self.frame_r.btn_panel.btn_dict["avto_on_off"], message="Автомасштаб")
            else:
                self.m_avto.set(0)
                self.frame_r.btn_panel.btn_dict["avto_on_off"].configure(
                    image=self.frame_r.btn_panel.img.manualm
                )
                ToolTip(
                    self.frame_r.btn_panel.btn_dict["avto_on_off"], message="Ручной масштаб"
                )
            self.avtoscale = not self.avtoscale

    def op_db(self, arg=None) -> None:
        """Просмотр отметок в базе"""
        # print('op_db', self.dbname, self.tbname)
        result = request_data_all(self.dbname, self.tbname)
        self.view_db = ViewMetka(self, result)
        self.view_db.show_tree()  # (№ int, timedata, shir, dolg, glub int, '"" or "A" or "coment" or "Диапазон..."')
        self.view_db.set_name_db(self.dbname)
        # self.tol_bar.btn['Оперативные отметки'].config(state='disabled')          # !!!

    def data_coment(self, num: int) -> list:
        """Получить коментарий из базы"""
        return request_data_coment(self.dbname, self.tbname, num)

    def state_db_norm(self, arg=None) -> None:
        """Удалить окно просмотра меток и разблокировать кнопку db"""
        # self.tol_bar.btn['Оперативные отметки'].config(state='normal')            # !!!
        self.view_db.destroy()

    # def init_fild(self) -> None:
    #     """Создание нового полотна и очередей"""
    #     self.board.create_fild()
    #     self.update_idletasks()
    #     self.bind_()

    def bind_(self) -> None:
        """Привязки событий"""
        self.bind("<Alt-F4>", self.on_closing)
        self.bind("<Return>", lambda arg=None: None)
        self.bind("<Control-z>", self._full_scr)
        # self.bind("<Escape>", self._clr)

    def _full_scr(self, arg=None):
        """Развернуть на весь экран"""
        self.state("zoomed") if self.wm_state else self.state("normal")
        self.attributes("-fullscreen", self.wm_state)
        self.wm_state = not self.wm_state

    # def cal_len(self, cod: int) -> float:
    #     """Вычислить длительность эхо в см."""
    #     tic = 10
    #     # return round(cod * self._vz / 20000)   # round(cod * n * self.vz / 10000, 2) -> float
    #     return round(cod * self._vz * (tic / 1000000), 2)  #

    def on_closing(self, arg=None) -> None:
        """Выход"""
        # sys.stdout.flush()
        raise SystemExit()


if __name__ == "__main__":
    import sys

    file = sys.argv[1] if len(sys.argv) > 1 else None
    app = App(file)
    if sys.platform.startswith("win"):
        TitleTop(app, "Просмотр логoв 200")
    # app.attributes("-fullscreen", True)       # во весь экран без кнопок
    # app.state('zoomed')                       # развернутое окно
    app.mainloop()
