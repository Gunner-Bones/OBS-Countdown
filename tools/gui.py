import winsound
import sys
import os
import tools.clientinput as ci
import tkinter as tk

SECONDS = 1
MINUTES = 0
HOURS = 0

FONT_TIMER = "system 70"
FONT_ENTRY = "system 30"
FONT_PAUSER = "system 20"


def coreIsInt(a):
    try:
        b = int(a)
    except ValueError:
        return False
    return True


def corePYIPath(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


FINISH_SOUND = corePYIPath("power.wav")


def cdFormatTime():
    s = str(SECONDS)
    if int(s) < 10:
        s = "0" + s
    m = str(MINUTES)
    if int(m) < 10:
        m = "0" + m
    h = str(HOURS)
    if int(h) < 10:
        h = "0" + h
    return h + ":" + m + ":" + s

def cdInput(user_in):
    global HOURS, MINUTES, SECONDS
    # 23 -> 23 Seconds
    # 1:23 -> 1 Minute 23 Seconds
    # 3:01:23 -> 3 Hours 1 Minute 23 Seconds
    split_input = user_in.split(":")
    if len(split_input) == 1:
        if not coreIsInt(split_input[0]):
            return False
        if int(split_input[0]) > 59:
            return False
        SECONDS = int(split_input[0])
        MINUTES = 0
        HOURS = 0
        return True
    elif len(split_input) == 2:
        for i in split_input:
            if not coreIsInt(i):
                return False
        if int(split_input[1]) > 59 or int(split_input[0]) > 59:
            return False
        SECONDS = int(split_input[1])
        MINUTES = int(split_input[0])
        HOURS = 0
        return True
    elif len(split_input) == 3:
        for i in split_input:
            if not coreIsInt(i):
                return False
        if int(split_input[2]) > 59 or int(split_input[1]) > 59:
            return False
        SECONDS = int(split_input[2])
        MINUTES = int(split_input[1])
        HOURS = int(split_input[0])
        return True
    return False


class CountdownTimer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.winfo_toplevel().geometry('640x300')
        tk.Frame.configure(self, bg='black')
        self.winfo_toplevel().configure(bg='black')
        self.winfo_toplevel().title('Countdown Timer')

        self.active = False
        self.finished = False
        self.starting = True

        self.enter_time = tk.Entry(self, fg='white', bg='black', justify=tk.CENTER,
            font=FONT_ENTRY)
        self.enter_time.insert(0, 'HH:MM:SS')
        self.enter_time.grid(row=0, column=0, pady=20)

        self.timer = tk.Label(self, text=cdFormatTime(), fg='white', bg='black',
            font=FONT_TIMER)

        self.pauser = tk.Button(self, text="Start", font=FONT_PAUSER, command=lambda: 
            self.start_pause())
        self.pauser.grid(row=1, column=0, pady=20)

    def clear_wid(self, obj):
        if isinstance(obj, list):
            for b in obj:
                try:
                    b.grid_forget()
                except:
                    pass
        else:
            obj.grid_forget()

    def start_pause(self):
        if self.starting:
            valid_input = cdInput(self.enter_time.get())
            if valid_input:
                self.starting = False
                self.clear_wid(self.enter_time)
                self.timer.config(text=cdFormatTime())
                self.timer.grid(row=0, column=0, pady=0)

                self.active = True
                self.pauser.config(text="Pause")
                self.winfo_toplevel().after(1000, lambda: self.decrement())
        else:
            if self.finished:
                self.winfo_toplevel().destroy()
            else:
                if self.active:
                    self.active = False
                    self.pauser.config(text="Resume")
                else:
                    self.active = True
                    self.pauser.config(text="Pause")
                    self.winfo_toplevel().after(1000, lambda: self.decrement())

    def decrement(self):
        global SECONDS, MINUTES, HOURS
        if HOURS == 0 and MINUTES == 0 and SECONDS == 0:
            self.finished = True
        if not self.finished:
            if self.active:
                if SECONDS != 0:
                    SECONDS -= 1
                else:
                    SECONDS = 59
                    if MINUTES != 0:
                        MINUTES -= 1
                    else:
                        MINUTES = 59
                        HOURS -= 1
                self.timer.config(text=cdFormatTime())
                self.winfo_toplevel().after(1000, lambda: self.decrement())
        else:
            self.timer.config(fg='red')
            self.pauser.config(text="Exit")
            sound(FINISH_SOUND)


class TkView(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switch_frame(CountdownTimer)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()

def sound(name):
    if ci.is_win():
        winsound.PlaySound(name, winsound.SND_ALIAS | winsound.SND_ASYNC)