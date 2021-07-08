'''
Author = Leo
Date = 19.10.04
Subscription = main program for kirara
'''
from kirara_figure import *
from kirara_function import *
import psutil
import win32api,win32con

# 限制KL只能单开
def proc_exist(process_name):
    pl = psutil.pids()
    python_limit = 2        # 因为不知道哪里会自己开一个Python程序，所以多出来一个限制，此时KL只能开一个
    for pid in pl:
        if psutil.Process(pid).name() == process_name:
            python_limit -= 1
            #logging.debug(python_limit)
            if python_limit == 0:
                return pid
            else:
                pass

if __name__ == '__main__':
    if isinstance(proc_exist('pythonw.exe'),int):
        logging.debug('Kirara Leoworld is running')
        win32api.MessageBox(0, "Kirara Leoworld已经在运行", "提醒",win32con.MB_ICONWARNING)
    else:
        logging.debug('Kirara Leoworld opened')
        run_game()
