import os
import json
import tkinter as tk
import tkinter.messagebox
from alien_invasion import run_game
import webbrowser

def start_game():
    settings={}
    try:
        settings['screen_width']=int(width_entry.get())
        settings['screen_height']=int(height_entry.get())
        settings['speedup_scale']=float(scale.get())
        settings['ship_limit']=int(ship_limit.get())
        with open('settings.json', 'w') as file_object:
            json.dump(settings,file_object)

    except ValueError:
        tkinter.messagebox.showerror(title= 'Error!', message= '请输入整数！')
    else:
        window.destroy()
        run_game()

def show_help():
    tkinter.messagebox.showinfo(title= '帮助', message= '方向键←→移动，空格键发射子弹，P键开始游戏，Q键退出\n推荐设置：窗口尺寸1200x800，游戏节奏1.1，自机数3')

def reset_high_score():
    try:
        os.remove('high_score.json')
    except FileNotFoundError:
        pass
    tkinter.messagebox.showinfo(title="Done!",message= "已重置！")

def view_website():
    tkinter.messagebox.showinfo(title='Credit',message= 'Inspired by Eric Matthes,\nDeveloped by Springfield4ever')
    webbrowser.open('https://www.pygame.org/news')

window=tk.Tk()
window.title("Alien Invasion")
window.geometry('240x420')

image_file= tk.PhotoImage(file='.\\images\\pygame_logo.png')
view_website_button=tk.Button(window,image=image_file,command=view_website)
view_website_button.pack(side="top")

start_game_button=tk.Button(window,text= '开始!', font=("MSYH",14),width=10,height=1,command=start_game)
start_game_button.pack(side='bottom')

help_button=tk.Button(window,text= '帮助', font=("MSYH",14),width=10,height=1,command=show_help)
help_button.pack(side= 'bottom')

reset_high_score_button=tk.Button(window,text= '重置最高分', font=("MSYH",14),width=10,height=1,command=reset_high_score)
reset_high_score_button.pack(side='bottom')

width_entry=tk.Entry(window,show=None,width=12)
width_entry.place(x=10,y=100)
width_label=tk.Label(window, text= '窗口宽',font=("MSYH",12))
width_entry.delete(0,tk.END)
width_label.place(x=30,y=120)

height_entry=tk.Entry(window,show=None,width=12)
height_entry.place(x=130,y=100)
height_label=tk.Label(window, text= '窗口高',font=("MSYH",12))
height_entry.delete(0,tk.END)
height_label.place(x=150,y=120)

scale=tk.Scale(window,label= '游戏节奏',font=("MSYH",10),from_=1,to=2,orient=tk.HORIZONTAL,length=200,tickinterval=0.2,resolution=0.1)

scale.place(x=20,y=150)

ship_limit=tk.Scale(window,label= '自机数',font=("MSYH",10),from_=2,to=5,orient=tk.HORIZONTAL,length=200,tickinterval=1,resolution=1)

ship_limit.place(x=20,y=220)

try:
    with open('settings.json') as file_object:
        temp_settings=json.load(file_object)
except FileNotFoundError:
    width_entry.insert(0,1200)   
    height_entry.insert(0,800)
    scale.set(1.1)
    ship_limit.set(3)
else:
    width_entry.insert(0,int(temp_settings['screen_width']))   
    height_entry.insert(0,int(temp_settings['screen_height']))
    scale.set(float(temp_settings['speedup_scale']))
    ship_limit.set(int(temp_settings['ship_limit']))

window.mainloop()