# -*-coding:utf-8 -*-
import tkinter
from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog

from MonkeyTest.Common.utils import get_devices, get_all_packages


class Ui_MainWindow:
    def __init__(self):

        self.root = Tk()
        self.root.title("Monkey测试")
        self.root.geometry("800x600+550+250")
        self.root.resizable(width=False, height=False)

        # 操作的设备
        self.device = ""
        self.devices = []
        self.deviceVar = StringVar()
        self.file_path = StringVar()
        self.monkey_path = StringVar()
        self.packVar = StringVar()
        self.pack = ""
        self.packs = []
        self.rank = ""
        self.ranks = ['-v', '-v-v', '-v-v-v']
        self.rankVar = StringVar()

        self.test_type = "系统测试"

        self.event_total_per = 0
        self.touch_check = StringVar()
        self.motion_check = StringVar()
        self.pinchzoom_check = StringVar()
        self.trackball_check = StringVar()
        self.rotation_check = StringVar()
        self.permission_check = StringVar()
        self.nav_check = StringVar()
        self.majornav_check = StringVar()
        self.syskeys_check = StringVar()
        self.appswitch_check = StringVar()
        self.flip_check = StringVar()
        self.anyevent_check = StringVar()
        # 事件百分比参数
        self.touch_per = StringVar()
        self.motion_per = StringVar()
        self.pinchzoom_per = StringVar()
        self.trackball_per = StringVar()
        self.rotation_per = StringVar()
        self.permission_per = StringVar()
        self.nav_per = StringVar()
        self.majornav_per = StringVar()
        self.syskeys_per = StringVar()
        self.appswitch_per = StringVar()
        self.flip_per = StringVar()
        self.anyevent_per = StringVar()

        # 事件选中
        self.monkey_times = StringVar()
        self.circulate_times = StringVar()
        self.event_delay = StringVar()

        self.btn_2 = None
        self.btn_1 = None

        self.main_mud()

    def main_mud(self):

        top_frm = Frame(self.root)
        top_frm.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        cen_frame = LabelFrame(self.root, text="模式选择（默认全局）")
        cen_frame.grid(row=1, column=0, padx=5, pady=15)
        bot_frame = LabelFrame(self.root, text="参数设置", width=550)
        bot_frame.grid(row=2, column=0, padx=5, pady=15)
        bot_run_frame = Frame(self.root)
        bot_run_frame.grid(row=3, column=0, pady=15)

        # 选择设备
        tl_fm = Frame(top_frm)
        tl_fm.grid(row=0, column=0, padx=5, pady=5)
        label_dev = Label(tl_fm, text="选择设备：")
        label_dev.grid(row=0, column=0, padx=5, pady=5)
        self.combox_devices = ttk.Combobox(tl_fm, textvariable=self.deviceVar, values=self.devices, width=10,
                                           state="readonly")
        self.combox_devices.grid(row=0, column=1, pady=5)
        self.combox_devices.bind('<<ComboboxSelected>>', self.select_device_event)
        self.combox_devices.bind('<Button-1>', self.device_combox_select)
        # 结果存放路径
        tr_fm = Frame(top_frm)
        tr_fm.grid(row=0, column=1, pady=5, padx=5)
        label_resultPath = Label(tr_fm, text="执行日志路径：")
        label_resultPath.grid(row=0, column=0)
        entry_path = Entry(tr_fm, textvariable=self.file_path, state="readonly")
        entry_path.grid(row=0, column=1)
        btn_select_path = Button(tr_fm, text="选择", command=self.select_file_path)
        btn_select_path.grid(row=0, column=2, padx=5)
        label_Monkey_resultPath = Label(tr_fm, text="Monkey路径：")
        label_Monkey_resultPath.grid(row=0, column=3)
        entry_Monkey_path = Entry(tr_fm, textvariable=self.monkey_path, state="readonly")
        entry_Monkey_path.grid(row=0, column=4)
        btn_select_Monkey_path = Button(tr_fm, text="选择", command=self.select_Monkey_path)
        btn_select_Monkey_path.grid(row=0, column=5, padx=5)

        # 切换
        self.btn_1 = Button(cen_frame, text="系统测试", width=50, state='disable', command=self.sys_form, bg='Orange')
        self.btn_2 = Button(cen_frame, text="应用测试", width=50, command=self.app_form)
        self.btn_1.grid(row=0, column=0, padx=5, pady=5, ipady=5, ipadx=10)
        self.btn_2.grid(row=0, column=1, padx=5, pady=5, ipady=5, ipadx=10)

        #
        bt_frame = Frame(bot_frame)
        bt_frame.grid(row=0, column=0, padx=5, pady=5)

        lab_m_times = Label(bt_frame, text="Monkey执行次数：")
        lab_m_times.grid(row=0, column=0, pady=5)
        entry_m_times = Entry(bt_frame, textvariable=self.monkey_times, width=10)
        entry_m_times.grid(row=0, column=1, padx=5, pady=5)

        lab_c_times = Label(bt_frame, text="循环执行次数：")
        lab_c_times.grid(row=0, column=2, pady=5)
        entry_c_times = Entry(bt_frame, textvariable=self.circulate_times, width=10)
        entry_c_times.grid(row=0, column=3, padx=5, pady=5)

        lab_event_delay = Label(bt_frame, text="事件延时：")
        lab_event_delay.grid(row=0, column=4, pady=5)
        entry_event_delay = Entry(bt_frame, textvariable=self.event_delay, width=6)
        entry_event_delay.grid(row=0, column=5, pady=5)
        lab_util = Label(bt_frame, text="秒")
        lab_util.grid(row=0, column=6)

        self.packs = get_all_packages()
        lab_pack_select = Label(bt_frame, text="包选择：")
        lab_pack_select.grid(row=0, column=7, pady=5)
        combox_packs = ttk.Combobox(bt_frame, textvariable=self.packVar, values=self.packs,
                                    state="readonly")
        combox_packs.grid(row=0, column=8, pady=5)
        combox_packs.bind('<<ComboboxSelected>>', self.select_pack_event)

        bc_frame = Frame(bot_frame)
        bc_frame.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        bc_l_frame = LabelFrame(bc_frame, text="Monkey事件占比：")
        bc_l_frame.grid(row=0, column=0)

        # 触摸事件：--pct - touch
        # 手势事件：--pct - motion
        # 二指缩放事件：--pct - pinchzoom
        # 轨迹事件：--pct - trackball
        # 屏幕旋转事件：--pct - rotation
        # 运行时权限开关事件（新增事件）：--pct - permission
        # 基本导航事件：--pct - nav
        # 主要导航事件：--pct - majornav
        # 系统按键事件：--pct - syskeys
        # 启动Activity事件：--pct - appswitch
        # 键盘事件：--pct - flip
        # 其他类型事件：--pct - anyevent

        # 触摸事件
        self.check_touch_event = tkinter.Checkbutton(bc_l_frame, text="触摸事件", variable=self.touch_check,
                                                     onvalue="--pct-touch", offvalue='')
        self.check_touch_event.grid(row=0, column=0, pady=5, padx=5)
        self.entry_touch_per = Entry(bc_l_frame, textvariable=self.touch_per, state="readonly")
        self.entry_touch_per.grid(row=0, column=1, padx=5, pady=5)
        self.check_touch_event.bind("<Button>", self.touch_check_entry)
        # 手势事件
        self.check_motion_event = tkinter.Checkbutton(bc_l_frame, text="手势事件", variable=self.motion_check,
                                                      onvalue="--pct-motion", offvalue="")
        self.check_motion_event.grid(row=0, column=2, pady=5, padx=5)
        self.entry_motion_per = Entry(bc_l_frame, textvariable=self.motion_per, state="readonly")
        self.entry_motion_per.grid(row=0, column=3, padx=5, pady=5)
        self.check_motion_event.bind("<Button>", self.motion_check_entry)
        # 缩放事件
        self.check_pinchzoom_event = tkinter.Checkbutton(bc_l_frame, text="缩放事件", variable=self.pinchzoom_check,
                                                         onvalue="--pct-pinchzoom",
                                                         offvalue="")
        self.check_pinchzoom_event.grid(row=1, column=0, pady=5, padx=5)
        self.entry_pinchzoom_per = Entry(bc_l_frame, textvariable=self.pinchzoom_per, state="readonly")
        self.entry_pinchzoom_per.grid(row=1, column=1, padx=5, pady=5)
        self.check_pinchzoom_event.bind("<Button>", self.pinchzoom_check_entry)
        # 轨迹事件
        self.check_trackball_event = tkinter.Checkbutton(bc_l_frame, text="轨迹事件", variable=self.trackball_check,
                                                         onvalue="--pct-trackball",
                                                         offvalue="")
        self.check_trackball_event.grid(row=1, column=2, pady=5, padx=5)
        self.entry_trackball_per = Entry(bc_l_frame, textvariable=self.trackball_per, state="readonly")
        self.entry_trackball_per.grid(row=1, column=3, padx=5, pady=5)
        self.check_trackball_event.bind("<Button>", self.trackball_check_entry)
        # 旋转事件
        self.check_rotation_event = tkinter.Checkbutton(bc_l_frame, text="旋转事件", variable=self.rotation_check,
                                                        onvalue="--pct-rotation", offvalue="")
        self.check_rotation_event.grid(row=2, column=0, pady=5, padx=5)
        self.entry_rotation_per = Entry(bc_l_frame, textvariable=self.rotation_per, state="readonly")
        self.entry_rotation_per.grid(row=2, column=1, padx=5, pady=5)
        self.check_rotation_event.bind("<Button>", self.rotation_check_entry)
        # 权限事件
        self.check_permission_event = tkinter.Checkbutton(bc_l_frame, text="权限事件", variable=self.permission_check,
                                                          onvalue="--pct-permission",
                                                          offvalue="")
        self.check_permission_event.grid(row=2, column=2, pady=5, padx=5)
        self.entry_permission_per = Entry(bc_l_frame, textvariable=self.permission_per, state="readonly")
        self.entry_permission_per.grid(row=2, column=3, padx=5, pady=5)
        self.check_permission_event.bind("<Button>", self.permission_check_entry)
        # 基导事件
        self.check_nav_event = tkinter.Checkbutton(bc_l_frame, text="基导事件", variable=self.nav_check,
                                                   onvalue="--pct-nav", offvalue="")
        self.check_nav_event.grid(row=3, column=0, pady=5, padx=5)
        self.entry_nav_per = Entry(bc_l_frame, textvariable=self.nav_per, state="readonly")
        self.entry_nav_per.grid(row=3, column=1, padx=5, pady=5)
        self.check_nav_event.bind("<Button>", self.nav_check_entry)
        # 主导事件
        self.check_majornav_event = tkinter.Checkbutton(bc_l_frame, text="主导事件", variable=self.majornav_check,
                                                        onvalue="--pct-majornav", offvalue="")
        self.check_majornav_event.grid(row=3, column=2, pady=5, padx=5)
        self.entry_majornav_per = Entry(bc_l_frame, textvariable=self.majornav_per, state="readonly")
        self.entry_majornav_per.grid(row=3, column=3, padx=5, pady=5)
        self.check_majornav_event.bind("<Button>", self.majornav_check_entry)
        # 按键事件
        self.check_syskeys_event = tkinter.Checkbutton(bc_l_frame, text="按键事件", variable=self.syskeys_check,
                                                       onvalue="--pct-syskeys", offvalue="")
        self.check_syskeys_event.grid(row=4, column=0, pady=5, padx=5)
        self.entry_syskeys_per = Entry(bc_l_frame, textvariable=self.syskeys_per, state="readonly")
        self.entry_syskeys_per.grid(row=4, column=1, padx=5, pady=5)
        self.check_syskeys_event.bind("<Button>", self.syskeys_check_entry)
        # 应用事件
        self.check_appswitch_event = tkinter.Checkbutton(bc_l_frame, text="应用事件", variable=self.appswitch_check,
                                                         onvalue="--pct-appswitch",
                                                         offvalue="")
        self.check_appswitch_event.grid(row=4, column=2, pady=5, padx=5)
        self.entry_appswitch_per = Entry(bc_l_frame, textvariable=self.appswitch_per, state="readonly")
        self.entry_appswitch_per.grid(row=4, column=3, padx=5, pady=5)
        self.check_appswitch_event.bind("<Button>", self.appswitch_check_entry)
        # 键盘事件
        self.check_flip_event = tkinter.Checkbutton(bc_l_frame, text="键盘事件", variable=self.flip_check,
                                                    onvalue="--pct-flip", offvalue="")
        self.check_flip_event.grid(row=5, column=0, pady=5, padx=5)
        self.entry_flip_per = Entry(bc_l_frame, textvariable=self.flip_per, state="readonly")
        self.entry_flip_per.grid(row=5, column=1, padx=5, pady=5)
        self.check_flip_event.bind("<Button>", self.flip_check_entry)
        # 类型事件
        self.check_anyevent_event = tkinter.Checkbutton(bc_l_frame, text="类型事件", variable=self.anyevent_check,
                                                        onvalue="--pct-anyevent", offvalue="")
        self.check_anyevent_event.grid(row=5, column=2, pady=5, padx=5)
        self.entry_anyevent_per = Entry(bc_l_frame, textvariable=self.anyevent_per, state="readonly")
        self.entry_anyevent_per.grid(row=5, column=3, padx=5, pady=5)
        self.check_anyevent_event.bind("<Button>", self.anyevent_check_entry)

        bc_r_frame = Frame(bc_frame)
        bc_r_frame.grid(row=0, column=1, sticky="N")
        lab_rank = Label(bc_r_frame, text="日志等级：")
        lab_rank.grid(row=0, column=0, padx=5, pady=5)
        self.rankVar.set(self.ranks[-1])
        combox_rank = ttk.Combobox(bc_r_frame, textvariable=self.rankVar, values=self.ranks, state="readonly")
        combox_rank.grid(row=0, column=1, padx=5)
        combox_rank.bind('<<ComboboxSelected>>', self.select_rank_event)

        self.text_run = Text(bc_r_frame, width=35, height=16, bg='black', fg='white')
        self.text_run.grid(row=1, column=0, rowspan=4, columnspan=3, padx=10, pady=5)
        scrollbar = tkinter.Scrollbar(bc_r_frame)
        scrollbar.config(command=self.text_run.yview)
        self.text_run.config(yscrollcommand=scrollbar.set)

        self.btn_start = Button(bot_run_frame, text="启动", width=20, bg='green')
        self.btn_start.grid(row=0, column=0, padx=5, pady=5)
        self.btn_stop = Button(bot_run_frame, text="停止", width=20, bg='red', state="disable")
        self.btn_stop.grid(row=0, column=1, padx=5, pady=5)

    # 添加日志
    def insert_run_log(self, text):
        self.text_run.insert(END, text+'\n')

    # 系统测试
    def sys_form(self):
        self.btn_1['state'] = 'disable'
        self.btn_2['state'] = 'normal'
        self.btn_1['bg'] = 'Orange'
        self.btn_2['bg'] = 'Snow'
        self.test_type = '系统测试'

    def app_form(self):
        self.btn_2['state'] = 'disable'
        self.btn_1['state'] = 'normal'
        self.btn_2['bg'] = 'Orange'
        self.btn_1['bg'] = 'Snow'
        self.test_type = '应用测试'

    # 选择设备事件
    def select_device_event(self, event):
        self.device = self.deviceVar.get()

    # 下拉设备事件
    def device_combox_select(self, event):
        self.devices = get_devices()
        self.combox_devices["value"] = self.devices

    # 选择文件路径事件
    def select_file_path(self):
        select_folder = filedialog.askdirectory()
        self.file_path.set(select_folder)
        print(self.file_path)

    def select_Monkey_path(self):
        select_folder = filedialog.askdirectory()
        self.monkey_path.set(select_folder)

    # 选择包事件
    def select_pack_event(self, event):
        self.pack = self.packVar.get()
        print("选中的应用：{}".format(self.pack))

    def select_rank_event(self, event):
        self.rank = self.rankVar.get()
        print("日志等级：{}".format(self.rank))

    # 复选框事件处理
    def touch_check_entry(self, event):
        if self.touch_check.get() == '':
            self.entry_touch_per.config(state="normal")
        else:
            self.entry_touch_per.config(state="readonly")

    def motion_check_entry(self, event):
        if self.motion_check.get() == '':
            self.entry_motion_per.config(state="normal")
        else:
            self.entry_motion_per.config(state="readonly")

    def pinchzoom_check_entry(self, event):
        if self.pinchzoom_check.get() == '':
            self.entry_pinchzoom_per.config(state="normal")
        else:
            self.entry_pinchzoom_per.config(state="readonly")

    def trackball_check_entry(self, event):
        if self.trackball_check.get() == '':
            self.entry_trackball_per.config(state="normal")
        else:
            self.entry_trackball_per.config(state="readonly")

    def rotation_check_entry(self, event):
        if self.rotation_check.get() == '':
            self.entry_rotation_per.config(state="normal")
        else:
            self.entry_rotation_per.config(state="readonly")

    def permission_check_entry(self, event):
        if self.permission_check.get() == '':
            self.entry_permission_per.config(state="normal")
        else:
            self.entry_permission_per.config(state="readonly")

    def nav_check_entry(self, event):
        if self.nav_check.get() == '':
            self.entry_nav_per.config(state="normal")
        else:
            self.entry_nav_per.config(state="readonly")

    def majornav_check_entry(self, event):
        if self.majornav_check.get() == '':
            self.entry_majornav_per.config(state="normal")
        else:
            self.entry_majornav_per.config(state="readonly")

    def syskeys_check_entry(self, event):
        if self.syskeys_check.get() == '':
            self.entry_syskeys_per.config(state="normal")
        else:
            self.entry_syskeys_per.config(state="readonly")

    def appswitch_check_entry(self, event):
        if self.appswitch_check.get() == '':
            self.entry_appswitch_per.config(state="normal")
        else:
            self.entry_appswitch_per.config(state="readonly")

    def flip_check_entry(self, event):
        if self.flip_check.get() == '':
            self.entry_flip_per.config(state="normal")
        else:
            self.entry_flip_per.config(state="readonly")

    def anyevent_check_entry(self, event):
        if self.anyevent_check.get() == '':
            self.entry_anyevent_per.config(state="normal")
        else:
            self.entry_anyevent_per.config(state="readonly")

    # 数据判断
    def msg_write_is_complete(self):
        self.event_total_per = 0
        if self.device == "":
            messagebox.showwarning(title="警告", message="请选择测试设备")
            return False
        if self.file_path.get() == "":
            messagebox.showwarning(title="警告", message="请选择运行日志路径")
            return False
        if self.monkey_path.get() == "":
            messagebox.showwarning(title="警告", message="请选择Monkey结果路径")
            return False
        if self.monkey_times.get() != "":
            if not self.monkey_times.get().isdigit():
                messagebox.showwarning(title="警告", message="monkey次数请填写数字")
                return False
        if self.touch_check.get() != "":
            if self.entry_touch_per.get() == "" or not self.entry_touch_per.get().isdigit():
                messagebox.showwarning(title="警告", message="请填写数字")
                return False
            self.event_total_per = self.event_total_per + int(self.entry_touch_per.get())
        if self.motion_check.get() != "":
            if self.entry_motion_per.get() == "" or not self.entry_motion_per.get().isdigit():
                messagebox.showwarning(title="警告", message="请填写数字")
                return False
            self.event_total_per = self.event_total_per + int(self.entry_motion_per.get())
        if self.pinchzoom_check.get() != "":
            if self.entry_pinchzoom_per.get() == "" or not self.entry_pinchzoom_per.get().isdigit():
                messagebox.showwarning(title="警告", message="请填写数字")
                return False
            self.event_total_per = self.event_total_per + int(self.entry_pinchzoom_per.get())
        if self.trackball_check.get() != "":
            if self.entry_trackball_per.get() == "" or not self.entry_trackball_per.get().isdigit():
                messagebox.showwarning(title="警告", message="请填写数字")
                return False
            self.event_total_per = self.event_total_per + int(self.entry_trackball_per.get())
        if self.rotation_check.get() != "":
            if self.entry_rotation_per.get() == "" or not self.entry_rotation_per.get().isdigit():
                messagebox.showwarning(title="警告", message="请填写数字")
                return False
            self.event_total_per = self.event_total_per + int(self.entry_rotation_per.get())
        if self.permission_check.get() != "":
            if self.entry_permission_per.get() == "" or not self.entry_permission_per.get().isdigit():
                messagebox.showwarning(title="警告", message="请填写数字")
                return False
            self.event_total_per = self.event_total_per + int(self.entry_permission_per.get())
        if self.nav_check.get() != "":
            if self.entry_nav_per.get() == "" or not self.entry_nav_per.get().isdigit():
                messagebox.showwarning(title="警告", message="请填写数字")
                return False
        if self.majornav_check.get() != "":
            if self.entry_majornav_per.get() == "" or not self.entry_majornav_per.get().isdigit():
                messagebox.showwarning(title="警告", message="请填写数字")
                return False
        if self.syskeys_check.get() != "":
            if self.entry_syskeys_per.get() == "" or not self.entry_syskeys_per.get().isdigit():
                messagebox.showwarning(title="警告", message="请填写数字")
                return False
        if self.appswitch_check.get() != "":
            if self.entry_appswitch_per.get() == "" or not self.entry_appswitch_per.get().isdigit():
                messagebox.showwarning(title="警告", message="请填写数字")
                return False
        if self.flip_check.get() != "":
            if self.entry_flip_per.get() == "" or not self.entry_flip_per.get().isdigit():
                messagebox.showwarning(title="警告", message="请填写数字")
                return False
        if self.anyevent_check.get() != "":
            if self.entry_anyevent_per.get() == "" or not self.entry_anyevent_per.get().isdigit():
                messagebox.showwarning(title="警告", message="请填写数字")
                return False
        if self.event_total_per > 100:
            messagebox.showwarning(title="警告", message="所有事件百分比不能超过100")
            return False
        if self.test_type == "应用测试":
            if self.packVar.get() == '':
                messagebox.showwarning(title='警告', message="选择测试的应用")
                return False
        return True


if __name__ == '__main__':
    ui = Ui_MainWindow()
    ui.root.mainloop()
