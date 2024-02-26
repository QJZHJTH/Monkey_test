# -*-coding:utf-8 -*-
from threading import Thread
from tkinter import messagebox

from MonkeyTest.Common.log import Logger
from MonkeyTest.Common.utils import *
from Page.home import Ui_MainWindow


class Ui_Action(Ui_MainWindow):
    def __init__(self):
        super(Ui_Action, self).__init__()
        self.count_time = None
        self.btn_start.bind("<Button-1>", self.thread_start_fun)
        self.btn_stop.bind("<Button-1>", self.stop_run)
        # 所有事件选项
        self.all_select = []


    # 启动执行
    def run(self):
        # 应用log
        self.sys_logger = log.Logger("result", self.file_path.get(), self.device, log_type="system")
        self.insert_run_log(text="开始执行")
        self.btn_start['state'] = "disable"
        self.btn_stop['state'] = "normal"
        # 数据校验
        if not self.msg_write_is_complete():
            return False
        cir_times = int(self.circulate_times.get())
        self.count_time = 0
        while cir_times != 0:
            # Monkeylog
            self.mk_logger = log.Logger("Monkey_result", self.monkey_path.get(), self.device, log_type="app")
            cir_times = cir_times - 1
            self.count_time += 1
            # 开启屏幕，进入主页面
            if not is_screenState(device=self.device):
                lightScreen(self.device)
            self.all_select = [
                self.touch_check.get() + " " + self.touch_per.get(),
                self.motion_check.get() + " " + self.motion_per.get(),
                self.pinchzoom_check.get() + " " + self.pinchzoom_per.get(),
                self.trackball_check.get() + " " + self.trackball_per.get(),
                self.rotation_check.get() + " " + self.rotation_per.get(),
                self.permission_check.get() + " " + self.permission_per.get(),
                self.nav_check.get() + " " + self.nav_per.get(),
                self.majornav_check.get() + " " + self.majornav_per.get(),
                self.syskeys_check.get() + " " + self.syskeys_per.get(),
                self.appswitch_check.get() + " " + self.appswitch_per.get(),
                self.flip_check.get() + " " + self.flip_per.get(),
                self.anyevent_check.get() + " " + self.anyevent_per.get(),
            ]
            while ' ' in self.all_select:
                self.all_select.remove(' ')
            msg = "第{}次Monkey测试".format(self.count_time)
            print(self.all_select)
            self.sys_logger.info(msg=msg)
            self.insert_run_log(text=msg)

            # 选择测试内容
            if self.test_type == "系统测试":
                self.insert_run_log("开始执行系统测试")
                flag = do_monkey(device_m=self.device, event_times=self.monkey_times.get(), log_rank=self.rankVar.get(),
                                 delay_time=self.event_delay.get(), type_m=self.test_type, event_list=self.all_select,
                                 logger=self.mk_logger)

            else:
                self.insert_run_log("开始执行应用测试")
                flag = do_monkey(device_m=self.device, event_times=self.monkey_times.get(), log_rank=self.rankVar.get(),
                                 delay_time=self.event_delay.get(), type_m=self.test_type, event_list=self.all_select,
                                 logger=self.mk_logger, pack=self.packVar.get())
            msg = "第{}次Monkey测试".format(self.count_time)
            self.insert_run_log(msg+"执行结束")
        # 结束Monkey任务
        self.insert_run_log("Monkey执行结束")
        self.btn_start['state'] = "normal"
        self.btn_stop['state'] = "disable"

    def stop_run(self, event):
        # 停止monkey执行
        # 停止运行循环
        print("停止")
        if not stop_monkey(device=self.device):
            messagebox.showwarning(title="警告", message="没有正在执行的monkey任务")
        else:
            self.btn_start['state'] = "normal"
            self.btn_stop['state'] = "disable"
            msg = "第" + str(self.count_time) + "次停止测试"
            self.sys_logger.info(msg=msg)
            messagebox.showinfo(title="提示", message="已停止monkey任务")

    # 线程
    def thread_start_fun(self, event):
        thread_start = Thread(target=self.run)
        thread_start.start()


if __name__ == '__main__':
    ui = Ui_Action()
    ui.root.mainloop()
