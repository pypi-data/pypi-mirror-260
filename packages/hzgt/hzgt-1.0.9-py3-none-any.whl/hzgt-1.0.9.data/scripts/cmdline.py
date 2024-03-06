# -*- coding: utf-8 -*-
import os
import sys
import locale
import subprocess
import threading
import time

from .CONST import INSTALLCMD

try:
    import click
except Exception as err:
    print(err)
    os.system(INSTALLCMD("click"))
    import click

from .strop import restrop
from .CONST import DEFAULT_ENCODING, PLATFORM, CURRENT_USERNAME


def get_cmd_stdout(cmd: str):
    """
        执行cmd命令时可以查看输出的内容

        建议指定编码encoding

        仅依靠cmd/shell的命令可以使用默认编码
        :param cmd: str 命令
        :param encoding: str 编码 默认使用用户指定的系统编码
        """
    def _get_cmdstdout(cmd: str):
        t = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        # 执行
        for line in iter(t.stdout.readline, b''):
            print(line.decode('gbk'))
        t.stdout.close()

    threading.Thread(target=_get_cmdstdout, args=(cmd,)).start()

@click.group()
def losf():
    """
    - d 命令行 下载模块\n
        - m: 必填~功能参数 1-文件下载 2-github仓库下载 3-音视频下载\n
        - u: 必填~文件/仓库/视频所在的url\n
        - s: 选填~保存路径
    """
    pass

@click.command()
@click.option("-m", "--mode", default=None, type=click.INT, help="必填~mode 1-文件下载 2-github仓库下载 3-音视频下载")
@click.option("-u", "--url", default=None, type=click.STRING, help="必填~url 文件/仓库/视频所在的url")
@click.option("-s", "--save", default='', type=click.STRING, help="选填~保存路径")
def d(mode, url, save):
    """
    命令行 下载
    """
    if mode is None:
        os.system("hzgt d --help")
        exit()
    if mode not in [1, 2, 3]:
        print(f"mode {mode} 无效")
        exit()
    from .download.download import downloadmain
    if save == '':
        if 'linux' in PLATFORM:  # linux
            downloadmain(mode, url, savepath=os.path.join("/home", CURRENT_USERNAME, "Download"))
        elif 'win' in PLATFORM:  # win
            downloadmain(mode, url, savepath="d:\\Download")
        else:
            currentpath = os.getcwd()
            downloadmain(mode, url, savepath=currentpath)
    else:
        downloadmain(mode, url, savepath=save)


losf.add_command(d)
if __name__ == "__main__":
    losf()