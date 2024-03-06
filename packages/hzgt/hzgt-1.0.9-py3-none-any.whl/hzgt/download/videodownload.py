import os
import subprocess
import time

from ..strop import restrop
from ..CONST import INSTALLCMD

try:
    import you_get
except Exception as err:
    print(err)
    os.system(INSTALLCMD("you-get"))

def VideoDownload(url, savepath=os.path.join("download_Files", "youget")):
    current_path = os.path.join(os.getcwd(), savepath)
    cmd = f'you-get "{url}" -o "{current_path}"'
    print("cmd命令：", restrop(cmd, f=5))
    # process = subprocess.Popen(['cmd', '/c', cmd],
    #                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    from ..cmdline import get_cmd_stdout
    get_cmd_stdout(cmd)


if __name__ == "__main__":
    url = input('输入视频url地址：')
    VideoDownload(url)
