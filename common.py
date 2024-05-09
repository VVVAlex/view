#!/usr/bin/env python

import functools
import operator
import os.path
import pathlib
import sys
import tempfile

# import tkinter.messagebox as box
from dataclasses import dataclass
from typing import NamedTuple

import customtkinter as ctk
from PIL import Image, ImageTk

# От вас и не ожидают, что вы это поймете.

font = "Roboto Medium"
font_size = -16


class LookupDict(dict):
    """Обращение к словарю не по ключу, а как к атрибуту"""

    def __init__(self, d):
        for key in d:
            setattr(self, key, d[key])
        super().__init__()

    def __getitem__(self, key):
        return self.__dict__.get(key, None)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)


class Row(NamedTuple):
    """Представление данных"""

    format_: str
    glub: int
    ampl: str
    lenth: int
    timdata: str
    shir: str
    dolg: str
    vs: str
    kurs: str
    vz: str
    zg: str
    ku: str
    depth: str
    rej: str
    frek: str
    cnt: int
    m: str
    m_man: str
    color_mm: str
    m_avto: str
    all_data: list


# @dataclass
# class ViewDataUpr:
#     """Представление данных"""
#     depth: str
#     ku: str
#     cnt: int = 0
#     m: int = 0
#     ampl: float = 0
#     len: float = 0
#     distance: int = 0


COLOR = (
    "#c40373",
    "#e32322",
    "#ea621f",
    "#f18e1c",
    "#fdc60b",
    "#f4e500",
    "#8cbb26",
    "#008e5b",
    "#0696bb",
    "#2a71b0",
    "#444e99",
    "#552f6f",
)

dict_color = {0x14: '#552f6f',
              0x2C: '#444e99',
              0x3E: '#2a71b0',
              0x4E: '#0696bb',
              0x60: '#008e5b',
              0x72: '#8cbb26',
              0x80: '#f4e500',
              0x90: '#fdc60b',
              0xA0: '#f18e1c',
              0xB6: '#ea621f',
              0xD0: '#e32322',
              0xFE: '#c40373'}

path = pathlib.Path(os.path.abspath("."))
# cwddir = os.path.abspath('.')
# path = pathlib.Path(cwddir)
bakdir = tempfile.mkdtemp()

img_path = path.joinpath("images")


def data_to_byte(kv: dataclass) -> bytes:
    """Преобразуем словарь данных в данные для передачи в модуль с добавлением ks"""
    data_str = "".join(i for i in kv.__dict__.values())
    ks = functools.reduce(operator.xor, (ord(i) for i in data_str[1:]), 0)
    r = ks.to_bytes(2, "big")
    # sum_l = chr(ks & 0x0F)
    # sum_h = chr((ks & 0xF0) >> 4)
    # return data_str.encode('latin-1') + f"{sum_h}{sum_l}".encode('latin-1') + b'\r\n'
    return data_str.encode("latin-1") + r + b"\r\n"


def get_color(arg: int) -> str:
    """Вернуть цвет по амплитуде как в ПУИ"""
    if not arg:
        return 'grey55'
    a = (0x14, 0x2C, 0x3E, 0x4E, 0x60, 0x72, 0x80, 0x90, 0xA0, 0xB6, 0xD0, 0xFE)
    # a = (11, 23, 45, 75, 111, 222, 330, 496, 740, 1100, 1480, 4096)
    for i,  j in enumerate(a):
        if arg <= j:
            return COLOR[11 - i]      # COLOR[0..11] от т красного до т синего
    return 'grey55'


def load_image(im, im_2=None, size: tuple = ()) -> ctk.CTkImage:
    """Загрузить изображения"""
    path_to_image = img_path.joinpath(im)
    if not size:
        size = (20, 20)
    if im_2:
        path_to_image2 = img_path.joinpath(im_2)
        return ctk.CTkImage(
            light_image=Image.open(path_to_image),
            dark_image=Image.open(path_to_image2),
            size=size,
        )
    else:
        return ctk.CTkImage(Image.open(path_to_image), size=size)


# img_records = load_image(im=img_path.joinpath('record2.png'),
#                          im_2=img_path.joinpath('record1.png'), size=(25, 25))


# img_pause = load_image(im=img_path.joinpath('pause2.png'),
#                        im_2=img_path.joinpath('pause1.png'), size=(25, 25))


def load_image_tk(im, size: tuple = ()) -> ImageTk.PhotoImage:
    """Загрузить изображения"""
    path_to_img = img_path.joinpath(im)
    if not size:
        size = (20, 20)
    return ImageTk.PhotoImage(Image.open(path_to_img).resize((size[0], size[1])))


def create_img(light: tuple, dark: tuple = None, size: tuple = (20, 20)) -> dict:
    """Создать словарь изображений в зависимости от темы"""
    img_dict = {}
    for i, j in enumerate(light):
        im = None if dark is None else f"{dark[i]}.png"
        img_dict[j] = load_image(f"{j}.png", im, size=size)
    return img_dict


if getattr(sys, "frozen", False):
    bundle_dir = sys._MEIPASS  # PyInstaller
else:
    bundle_dir = path

imgdir = path.joinpath(bundle_dir, "images")
