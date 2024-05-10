#!/usr/bin/env python

import os.path
import time
import pathlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics, ttfonts
from common import imgdir, get_color, bakdir

# import sys, subprocess

#  система координат x0, y0 левый нижний угол x1, y1 правый верхний угол


class Pdf:
    """Создание и печать pdf документа"""
    # w=768, data=None, src=None, scale = None, filename=None, verbose=None
    def __init__(self, master, verbose):
        # [Row(format_, glub, ampl, timdata, shir, dolg, vs, kurs, m_man, color_mm_, m_avto, all_data)...]
        self.master = master            # show_bso
        self.w, self.data, self.scr, self.scale, self.name = self.master.get_pdf_data()
        self.W = 756.0              # слева на право 768.0
        self.H = 450                # снизу вверх                   # 400 !!!
        self.dx = 30                # слева
        self.dy = 90                # снизу
        self.stic = 7               # засечка на осях
        self.dl = 15                # удление надписий от осей
        self.k = self.W / self.w
        # self.list_scale = [(0, 2), (1, 1), (2, 0.2), (3, 0.1),
        # (4, 0.05), (5, 0.02), (6, 0.01), (7, 4.0/600), (8, 0.005), (9, 0.004)]
        self.list_scale = [(0, 2.0), (1, 1.0), (2, 0.4), (3, 0.2), (4, 0.1), (5, 0.05),
                           (6, 0.02), (7, 0.01), (8, 4.0/600)]
        my_font_object = ttfonts.TTFont('Arial', 'arial.ttf')
        pdfmetrics.registerFont(my_font_object)
        self.dir = '.'
        cur_path = pathlib.Path('temp.pdf')
        self.tmp_name = cur_path.joinpath(bakdir, cur_path)
        if self.data:
            # name = os.path.join(bakdir, 'temp.pdf')
            # self.c = canvas.Canvas("temp.pdf", pagesize=landscape(A4))  # файл "temp.pdf" в текущем каталоге
            self.c = canvas.Canvas(f"{self.tmp_name}", pagesize=landscape(A4))
            # print(self.c.getAvailableFonts())                         # все зарегистрированные шрифты
            self.asix()
            self.grid()
            self.c.setFillColor('darkblue')
            self.c.drawString(self.dx + self.W + self.dl, self.dy + self.H - 5, "0")
            self.data_pdf()
            self.pasteimg()
            self.run()
            self.go(verbose)

    def pasteimg(self) -> None:
        """Рисуем кораблик и логотип"""
        file = os.path.join(imgdir, 'korabl.gif')
        self.c.drawInlineImage(file, self.W, self.dy // 2 - 20, 48, 24)    # 5

    def data_pdf(self) -> None:
        """Рисуем данные в масштабе, масштаб как и в просмоторщике
        'глубина','амплитуда','%d.%m.%y %H:%M:%S','широта','долгота',
        'метка ручн', 'метка txt(avto)', [all].
        """
        w, h, dx, dy = self.W, self.H, self.dx, self.dy
        y_ = 10          # смещение гор. надписи относит. верха оси X
        hide_met, view_len = self.master.gethide_metka()
        print(f'->{hide_met}, ->{view_len}')
        dat = [i.glub / 1.0 for i in self.data]           # глубина  [1]       .glub
        # glub = [i[2] for i in self.data]                 # амплитуда  [2]     .ampl
        dat_all = None
        try:
            dat_all = [g.all_data for g in self.data]     # [[(),(),...],[(), (),...],...]  .all_data [-1]
        except Exception:
            pass
        man_met = [i.m_man for i in self.data]            # ручн. метка           .m_man  [8]
        color_mm = [i.color_mm for i in self.data]        # цвет ручн. метки      .color_mm []
        avt_met = [i.m_avto for i in self.data]           # авт.. метка           .m_avto  [10]
        txt = [i.timdata for i in self.data]              # объект времени        .timdata  [3]
        # scal = ([5, 10, 15, 20], [10, 20, 30, 40], [50, 100, 150, 200], [100, 200, 300, 400],
        #         [200, 400, 600, 800], [500, 1000, 1500, 2000], [1000, 2000, 3000, 4000],
        #         [1500, 3000, 4500, 6000], [2000, 4000, 6000, 8000], [2500, 5000, 7500, 10000])
        scal = ([5, 10, 15, 20], [10, 20, 30, 40], [25, 50, 75, 100], [50, 100, 150, 200], [100, 200, 300, 400],
                [200, 400, 600, 800], [500, 1000, 1500, 2000], [1000, 2000, 3000, 4000],
                [1500, 3000, 4500, 6000])
        j, n = self.list_scale[self.scale] if self.scale else self.list_scale[0]
        self.c.saveState()
        self.c.setDash([])
        self.c.setFont('Helvetica', 10)
        self.xy_dat(scal[j])
        self.c.restoreState()
        # self.k = self.k * 2     #
        for i in range(self.w):
            if i >= len(self.data):
                break  # если данных меньше чем w то будет except
            if not self.master.board.flag_on_point:      # если показ всех целей
                if dat_all[i]:                           # [(), (),...]
                    for gl in dat_all[i]:                # проход по всем (глубинам, амплитудам) можно сменить цвет
                        if i != 0:
                            if gl[0] / 1.0 <= scal[j][-1] * 10:  # 100000 подрезка выпадающих за низ холста
                                color = get_color(gl[1])
                                self.c.setFillColor(color)
                                # self.c.setStrokeColor(color)
                                if not view_len:
                                    self.c.circle(dx + w - i * self.k - 1, dy + h - round(gl[0] * n) * h / 400,
                                                  0.8, stroke=0, fill=1)
                                else:
                                    ln = round(gl[-1] * 10 * n) * h / 400
                                    yi = h - round(gl[0] * n * h / 400)
                                    lnn = yi if ln > yi else ln
                                    self.c.rect(dx + w - i * self.k - 1, dy + yi,                      # 450/400 = 1.125
                                                1, 1 - lnn, stroke=0, fill=1)
            else:                             # показ одной цели
                if dat[i]:                    # 10km
                    if dat[i] <= 100000:      # выкидываю > 10км, чтобы не вылезало за ось снизу
                        # color1 = get_color(glub[i])
                        # color1 = get_color(dat_all[i][0][1])
                        color1 = '#444'                     #
                        self.c.setFillColor(color1)
                        # self.c.setStrokeColor(color1)
                        self.c.circle(dx + w - i * self.k - 1, dy + h - round(dat[i] * n) * h / 400,      #
                                      0.80, stroke=0, fill=1)
            self.c.saveState()
            self.c.setDash([])
            self.c.setFont('Helvetica', 10)
            if dat[i] != 0:
                y = dy + h - round(dat[i] * n) * h / 400
                if y < dy:
                    y = dy
            else:
                y = dy + h
            numa = avt_met[i].strip()
            if numa and hide_met:             # авто метка
                self.c.setFillColor('blue')
                self.c.setStrokeColor('blue')
                self.c.setLineWidth(0.25)
                self.c.line(dx + w - i * self.k, y, dx + w - i * self.k, dy + h + 5)    # avto_metka
                self.c.translate(dx + w - i * self.k - 6, dy + y_ + h + 15)
                self.c.drawCentredString(5, -15, f'{numa}')
                self.c.setFillColor('blue')
                self.c.setStrokeColor('blue')
                self.c.drawCentredString(5, 0, self.txt_time(txt[i]))
            num = man_met[i].strip()
            if num and hide_met:              # ручная метка
                color_ = color_mm[i]                # "red" or "green"
                if color_ == 'spring green':        # 00ff7f
                    color_ = 'green'
                self.c.setFillColor(color_)
                self.c.setStrokeColor(color_)
                self.c.setLineWidth(0.5)
                self.c.line(dx + w - i * self.k, y, dx + self.W - i * self.k, dy + h + 5)    # man_metka
                self.c.translate(dx + w - i * self.k - 6, dy + y_ + h)
                self.c.drawCentredString(5, 0, f'{num}')
            self.c.restoreState()
        self.c.setFillColor('#777')
        self.c.setFont('Arial', 11)
        self.c.drawString(dx * 1.2, dy // 2 - 12, self.info())    # 2

    @staticmethod
    def txt_time(t) -> str:
        """Возвращает отформатированное время"""
        return time.strftime('%H:%M', t)

    def xy_dat(self, y_scal) -> None:
        """Подпись по оси Y и X"""
        w, h, dx, dy, dl = self.W, self.H, self.dx, self.dy, self.dl
        x_string = []
        d_y = 3
        self.c.drawString(dx + w + dl, dy + h * 3 // 4 - d_y, str(y_scal[0]))         # Y
        self.c.drawString(dx + w + dl, dy + h // 2 - d_y, str(y_scal[1]))
        self.c.drawString(dx + w + dl, dy + h // 4 - d_y, str(y_scal[2]))
        self.c.drawString(dx + w + dl, dy - d_y, str(y_scal[3]))
        for i, j, x in ((0, 0, 0), (self.w // 4, 1, w // 4), (self.w // 2, 2, w // 2),
                        (self.w * 3 // 4, 3, w * 3 // 4), (self.w - 1, 4, w - 1)):
            try:
                s = time.strftime("%d.%m %H:%M", self.data[int(i)].timdata)     # .timdata [3]
                x_string.append(s)
            except IndexError:
                x_string.append('')
            self.c.drawCentredString(dx + w - x, dy - dl - 2, x_string[j])         # X

    def asix(self) -> None:
        """Рисуем оси"""
        w, h, dx, dy = self.W, self.H, self.dx, self.dy
        self.c.setLineWidth(2.0)
        self.c.line(dx + w, dy, dx + self.W, dy + h)                    # Y
        self.c.line(dx, dy + h, dx + self.W, dy + h)                   # X  с верху
        self.c.line(dx, dy, dx + self.W, dy)                           # X_ с низу
        for i in [0, h // 4, h // 2, h * 3 // 4, h]:
            self.c.line(dx + w, dy + i, dx + w + self.stic, dy + i)
        for i in [0, w // 4, w // 2, w * 3 // 4, w]:
            self.c.line(dx + i, dy, dx + i, dy - self.stic)

    def grid(self) -> None:
        """Рисуем сетку"""
        w, h, dx, dy = self.W, self.H, self.dx, self.dy
        self.c.setLineWidth(0.5)
        self.c.setDash([1, 2])
        self.c.grid([dx, w // 4 + dx, w // 2 + dx, w * 3 // 4 + dx,
                     w + dx], [dy, h // 4 + dy, h // 2 + dy, h * 3 // 4 + dy, h + dy])

    def info(self) -> str:
        """Формируем строку info"""
        if self.scr is None:
            self.scr = '*'
        # st = time.ctime(time.time())
        # locale.setlocale(locale.LC_ALL, "Russian_Russia.1251")        #####
        # s = "%A %d %B %Y %H:%M:%S"
        s = "%d %B %Y %H:%M:%S"
        st = time.strftime(s)
        istr = f"Файл = {self.name},  экран = {self.scr},  {st}"
        return istr

    def run(self) -> None:
        """Сохранить pdf файл на диск"""
        self.c.showPage()
        self.c.save()

    # @staticmethod
    # def go_(verbose):
    #     """FRportable.exe -filename то откывает документ,
    #     -/p -filename то сразу печать"""
    #     import subprocess
    #     #file = os.path.join(bundle_dir, 'frp.exe')  ## если frp.exe включать в сборку (смотри bso_5.spec)
    #     file = os.path.abspath(os.path.join('.', 'frp.exe'))  # иначе
    #     name = 'temp.pdf'
    #     subprocess.Popen(f'{file} {name}') if verbose \
    #         else subprocess.Popen(f'{file} /p {name}')
    # subprocess.run(['explorer', 'csyntax.pdf'])

    def go(self, verbose) -> None:
        command = 'open' if verbose else 'print'
        try:
            # os.startfile('temp.pdf', command)
            # cur_path = pathlib.Path('temp.pdf')
            # name = cur_path.joinpath(bakdir, cur_path)
            os.startfile(f'{self.tmp_name}', command)
        except (FileNotFoundError, NameError):
            pass

    # def go2(self, verbose):
    #     command = 'open' if verbose else 'print'
    #     if sys.platform == "win32":
    #         os.startfile(f'{self.tmp_name}', command)
    #     else:
    #         self.opener = "open" if sys.platform == "darwin" else "xdg-open"
    #         subprocess.call([f'{self.opener}', f'{self.tmp_name}'])

    # def open_file(filename):
    #     if sys.platform == "win32":
    #         os.startfile(filename)
    #     else:
    #         opener = "open" if sys.platform == "darwin" else "xdg-open"
    #         subprocess.call([opener, filename])
