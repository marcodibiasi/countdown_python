from tkinter import *
import time
import threading 
from PIL import ImageTk, Image
from datetime import date

class PomodoroTimer:

    root = Tk()
    t_copy, add_mins = int, int
    timer = Label(root)
    stop_thread = threading.Event() 

    start_button = Button(root)
    stop_button = Button(root)
    reset_button = Button(root)
    add_button = Button(root)


    def __init__(self) -> None:
        self.root.geometry("600x400")
        self.root.config(background="#b4b3b4")

        #VARIABLES
        self.t_copy, self.add_mins = 0, 0

        #IMAGES
        play_button_img = Image.open('/Users/marcodibiasi/Desktop/Programmazione/Python/Pomodoro/Assets/Button_play3.png')
        resized_play_button_img = ImageTk.PhotoImage(play_button_img.resize((250, 250), Image.ANTIALIAS))
        stop_button_img = Image.open('/Users/marcodibiasi/Desktop/Programmazione/Python/Pomodoro/Assets/Button_stop.png')
        resized_stop_button_img = ImageTk.PhotoImage(stop_button_img.resize((250, 250), Image.ANTIALIAS))
        plus_button_img = Image.open('/Users/marcodibiasi/Desktop/Programmazione/Python/Pomodoro/Assets/Button_plus.png')
        resized_plus_button_img = ImageTk.PhotoImage(plus_button_img.resize((150, 150), Image.ANTIALIAS))
        reset_button_img = Image.open('/Users/marcodibiasi/Desktop/Programmazione/Python/Pomodoro/Assets/Button_reset.png')
        resized_reset_button_img = ImageTk.PhotoImage(reset_button_img.resize((150, 150), Image.ANTIALIAS))

        #BUTTONS
        self.start_button.config(image=resized_play_button_img, width=200, height=200, command=self.new_thread)
        self.start_button.place(relx=0.5, rely=0.7, anchor="center")
        self.stop_button.config(image=resized_stop_button_img, width=200, height=200, command=self.stop)
        self.reset_button.config(image=resized_reset_button_img, width=140, height=140, command=self.reset)
        self.reset_button.place(relx=0.67, rely=0.7, anchor="w") 
        self.add_button.config(image=resized_plus_button_img, width=140, height=140, command=self.add)
        self.add_button.place(relx=0.32, rely=0.7, anchor="e")
        # Entry(self.root, textvariable=self.time_value, background="#d7d6d8").place(relx=0.5, rely=0.35, anchor="center")

        #TIMER
        self.timer.config(text=" 00:00:00 ", font="Helvetica 130", fg="#a5f3a7", background="#b4b3b4")
        self.timer.place(relx=0.5, rely=0.25, anchor="center")
        self.time_value = StringVar()

        self.root.mainloop()


    def countdown(self, t):   
        self.t_copy = t
        while self.t_copy > -1: 
            mins, secs = divmod(self.t_copy, 60)
            hours = 0
            if mins >= 60:
                hours, mins = divmod(mins, 60)    
            
            stored_hours, stored_mins, stored_secs = self.store_variables(t)

            timer_text="{:02d}:{:02d}:{:02d}".format(hours, mins, secs)  
            self.timer.config(text=timer_text)       
            self.root.update()
            self.t_copy-=1
            time.sleep(1)    

            if self.t_copy == -1: 
                with open("/Users/marcodibiasi/Desktop/Programmazione/Python/Pomodoro/datas.txt", mode="a+") as file:
                    datas = file.write("Day: " + str(self.today) + "\nStudied: {:02d}:{:02d}:{:02d}\n\n".format(stored_hours, stored_mins, stored_secs))
            if self.stop_thread.is_set(): break    


    def store_variables(self, t):    
        self.mins, self.secs = divmod(t, 60)
        self.hours = 0
        if self.mins >= 60:
            self.hours, self.mins = divmod(self.mins, 60) 

        return self.secs, self.mins, self.hours 


    def new_thread(self):
        self.to_stop(True)
        value = int(self.time_value.get())
        self.stop_thread.clear()     
        t = threading.Thread(target=self.countdown, args=(value, ))
        self.time_value.set(0)
        t.start()  


    def reset(self):
        self.stop_thread.set()
        self.time_value.set(0)
        self.add_mins, self.t_copy = 0, 0
        self.timer.config(text="00:00:00")


    def stop(self):
        self.to_stop(False)
        self.time_value.set(self.t_copy)
        self.stop_thread.set()


    def add(self):
        self.add_mins += 1
        self.time_value.set(self.add_mins * 60)
        timer_text="00:{:02d}:00".format(self.add_mins) 
        self.timer.config(text=timer_text)
        self.root.update() 
 

    def to_stop(self, stopped):
        print()
        if stopped:
            self.add_button.place_forget()
            self.start_button.place_forget()
            self.stop_button.place(relx=0.5, rely=0.7, anchor="center")
        else:
            self.add_button.place(relx=0.3, rely=0.7, anchor="e")
            self.stop_button.place_forget()
            self.start_button.place(relx=0.5, rely=0.7, anchor="center")


PomodoroTimer()
