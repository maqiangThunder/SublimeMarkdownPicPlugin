#!/usr/bin/python
# coding=utf-8
"""
__author__ = 'maqiang'
__date__ = '2016/4/17'
__version__ = '0.1'
"""
import os
import re
import traceback
import win32api
import win32clipboard
import win32gui
from time import time

import win32con
from PIL import ImageGrab


# F:\hexo\source\_posts\hexo\开发一个在sublime下的markdown图片插件.md ? (_posts) - Sublime Text (UNREGISTERED)
# F:\hexo\source\_posts\hexo\
# 开发一个在sublime下的markdown图片插件.md
def handle_window(hwnd, nouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        try:
            # 判断是否是sublime窗口
            if win32gui.GetWindowText(hwnd).find('- Sublime Text') != -1 and win32gui.GetWindowText(hwnd).find('.md'):
                sublime_win_name = win32gui.GetWindowText(hwnd)
                print sublime_win_name

                result = re.search('(^.+)\\\(.+\\.md).*', sublime_win_name)
                md_path = result.group(1) + '\\'
                md_name = result.group(2).replace('.md', '')
                print md_path
                print md_name

                # 从剪切板获取图片
                im = ImageGrab.grabclipboard()
                md_image_path = md_path + r'\\' + md_name
                if not os.path.exists(md_image_path):
                    os.makedirs(md_image_path)
                image_file = '%d.png' % int(time())
                im.save(md_image_path + r'\\' + image_file, 'PNG')
                setText('![](%s)' % (md_name + r'/' + image_file))
                win32api.MessageBox(0, u'图片转化成功!', u'成功', win32con.MB_OK)
        except Exception, e:
            traceback.print_exc()
            win32api.MessageBox(0, u'图片转化失败', u'失败', win32con.MB_OK)


def setText(aString):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_TEXT, aString)
    win32clipboard.CloseClipboard()


if __name__ == '__main__':
    try:
        # win32gui.EnumWindows(handle_window, None)
        pwin = win32gui.FindWindow('PX_WINDOW_CLASS', None)
        sublime_win_name = win32gui.GetWindowText(pwin)
        print sublime_win_name

        result = re.search('(^.+)\\\(.+\\.md).*', sublime_win_name)
        md_path = result.group(1) + '\\'
        md_name = result.group(2).replace('.md', '')
        print md_path
        print md_name

        # 从剪切板获取图片
        im = ImageGrab.grabclipboard()
        if im is None:
            pass
        md_image_path = md_path + r'\\' + md_name
        print md_image_path
        if not os.path.exists(md_image_path):
            os.makedirs(md_image_path)
        image_file = '%d.png' % int(time())
        print image_file
        im.save(md_image_path + r'\\' + image_file, 'PNG')
        print  '![](%s)' % (md_name + r'/' + image_file)
        setText('![](%s)' % (md_name + r'/' + image_file))
        win32api.MessageBox(0, u'图片转化成功!', u'成功', win32con.MB_OK)
    except Exception, e:
        traceback.print_exc()
        win32api.MessageBox(0, u'图片转化失败', u'失败', win32con.MB_OK)
