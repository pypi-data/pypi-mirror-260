# -*- coding: utf-8 -*-
import ctypes,sys,os
import Skin列表 as 皮肤
import she

_Skin路径 = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.abspath(__file__).replace('\\taowa_skin\\skin.py', '')
_Skin路径 += '\\taowa_skin\\she\\'
_skin = None


def 皮肤_加载(皮肤文件路径: str = '',密码: str = '',色调:int = 0,饱和度:int = 1,亮度:int = 0):
    global _skin

    '''
    :param 皮肤文件路径: 使用[皮肤.]查看列表,或自己提供皮肤文件路径
    :param 密码:可空
    :param 色调: -180-180,默认0
    :param 饱和度:1-255,默认1
    :param 亮度:-100-100,默认0
    :return:
    '''
    if not _skin:
        _skin = ctypes.CDLL(_Skin路径 + 'SkinH_EL.dll')
    _skin.SkinH_AttachRes.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int,ctypes.c_int]
    _skin.SkinH_AttachRes.restype = ctypes.c_int
    皮肤文件路径 = _Skin路径 + 皮肤文件路径 if 皮肤文件路径 else _Skin路径 + 皮肤.简约白
    if 皮肤文件路径:
        if not(皮肤文件路径.find('/') or 皮肤文件路径.find('\\')):
            皮肤文件路径 = _Skin路径 + 皮肤文件路径
    else:
        皮肤文件路径 = _Skin路径 + 皮肤.简约白 # 默认皮肤

    with open(皮肤文件路径, 'rb') as a:
        皮肤文件 = a.read()
    _skin.SkinH_AttachRes(皮肤文件, len(皮肤文件), 密码.encode('utf8'),色调,饱和度,亮度)


def 皮肤_卸载():
    _skin.SkinH_Detach()


def 皮肤_置阴影特效(是否开启: bool = True):

    '''
    :param 是否开启: 是否开启阴影特效,默认为Ture
    '''
    _skin.SkinH_SetAero.argtypes = [ctypes.c_int]
    _skin.SkinH_SetAero(int(是否开启))

def 皮肤_颜色调整(色调:int = 0,饱和度:int = 1,亮度:int = 0):

    '''
    :param 色调: -180-180,默认0
    :param 饱和度:1-255,默认1
    :param 亮度:-100-100,默认0
    '''
    _skin.SkinH_AdjustHSV.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_int]
    _skin.SkinH_AdjustHSV(色调,饱和度,亮度)


