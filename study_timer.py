import customtkinter as ctk
import tkinter.filedialog as dir
import tkinter.messagebox as msg
import time
import subprocess,os,sys,ctypes,random
import threading
from PIL import Image

def resource_path(relative_path):
    
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)  # For PyInstaller
    return os.path.join(os.path.abspath("."), relative_path)

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
def disable_network():
    print("Disabling network...")
    subprocess.Popen(["netsh", "interface", "set", "interface", "Wi-Fi", "disable"], startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)

def enable_network():
    print("Enabling network...")
    subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "enable"], startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)


def start_timer():
    global seconds_remaining
    minutes = int(entry_minutes.get())
    seconds = int(entry_seconds.get())
    seconds_remaining = minutes * 60 + seconds
    update_timer_display()

    while seconds_remaining > 0:
        time.sleep(1)  
        seconds_remaining -= 1
        update_timer_display()
        
        if stop_timer_flag:
            print("Timer stopped.")
            break 

        # Disable Wi-Fi every 5 seconds , No 247 vids
        if seconds_remaining % 5 == 0:
            disable_network()
            
    if seconds_remaining <= 0 and not stop_timer_flag:
        
        disable_network()
        enable_network() 
        unlock_gui() 

def update_timer_display():
    minutes = seconds_remaining // 60
    seconds = seconds_remaining % 60
    timer_label.configure(text=f"{minutes:02}:{seconds:02}")

def frame_image():
    Image_frame.place_forget()
    image_path = dir.askopenfilename(title="Choose The Image",filetypes=[("Image","*.jpg"),("Image","*.png"),("Image","*.jpeg")])
    Image_frame.place(x=10,y=120)
    global Aiim   # JUST DO IT BUD
    Aiim = ctk.CTkImage(light_image=Image.open(image_path),size=(110,110))
    global frame
    frame = ctk.CTkLabel(root,width=110,height=110,text="",image=Aiim)
    frame.place(x=10,y=120)
def start_timer_thread():
    ask_first = msg.askyesno("WARNING!","You Won't be able to close this program untill the timer reaches zero , NO internet(you will automatically enable your internet after closing this), Are you sure you want to get to your goal? ")
    if ask_first:
        global stop_timer_flag
        stop_timer_flag = False  
        disable_gui()
        timer_thread = threading.Thread(target=start_timer)
        timer_thread.daemon = True
        timer_thread.start()
    else:
        msg.showinfo("yahoo!","We ain't reaching to our goal!!")

def reset_timer():
    global seconds_remaining, stop_timer_flag
    stop_timer_flag = True 
    seconds_remaining = 0
    update_timer_display()

def disable_gui():
    start_button.configure(state =ctk.DISABLED)
   
def rem_img():
    frame.destroy()
    Image_frame.place

def unlock_gui():
    start_button.configure(state = ctk.NORMAL)
    
    
   

# Function to disable Wi-Fi every 5 seconds , Can't Trust You Guys
def disable_wifi_periodically():
    while not stop_timer_flag:
        time.sleep(5)  
        disable_network()  

photo = Image.open(resource_path("background.png"))
bg = ctk.CTkImage(light_image=photo,dark_image=photo,size=(360,240))

bg1 = ctk.CTkImage(light_image=Image.open(resource_path("bg1.png")),dark_image=Image.open(resource_path("bg1.png")),size=(70,35))
bg2 = ctk.CTkImage(light_image=Image.open(resource_path("bg2.png")),dark_image=Image.open(resource_path("bg2.png")),size=(70,35))
root = ctk.CTk()

root.iconbitmap(resource_path("icon.ico"))

root.title("Aspirant's Timer")
root.geometry("360x240")
root.maxsize(360,240)
root.wm_attributes("-transparentcolor", 'grey')
background = ctk.CTkLabel(root,image=bg,text ="").place(x=0, y=0, relwidth=1, relheight=1)
# Timer label

timer_label = ctk.CTkLabel(root,text="00:00", font=("Arial", 40),image=bg1,fg_color=None,corner_radius=0)
timer_label.pack()

set_label = ctk.CTkLabel(root,text="Set Timer",font=("Halvetica",20),corner_radius=0,image=bg2)
set_label.place(x=20,y=20)

entry_minutes = ctk.CTkEntry(root, width=40,height=40,font=("Arial",25),bg_color="transparent",corner_radius=0)
entry_minutes.insert(0, "0")
entry_minutes.place(x=10,y=60)

entry_seconds = ctk.CTkEntry(root, width=40,height=40,font=("Arial",25),corner_radius=0)
entry_seconds.insert(0, "0")
entry_seconds.place(x=55,y=60)


start_button = ctk.CTkButton(root, corner_radius=0,text="Start Timer", command=start_timer_thread,width=120,height=35,font=("fixedsys",18))
start_button.place(x=160,y=190)


# Aim your FRAME ( f iit , overrated af)
global Image_frame
Image_frame = ctk.CTkButton(root,width=110,height=110,text="Image your AIM",command=frame_image)
Image_frame.place(x=10,y=120)

seconds_remaining = 0
stop_timer_flag = False


wifi_thread = threading.Thread(target=disable_wifi_periodically)
wifi_thread.daemon = True  
wifi_thread.start()

# Ensure the application closes gracefully ( no way )
def on_closing():  
    time_remaining = str(timer_label.cget("text"))
    on_time = time_remaining.split(":")
  
    
    if (int(on_time[0]) != 0):
        # 1 minute early leave for you guys ! khi khi khi
        
        root.do_not_stop_studying()
            
    else:
        enable_network()    
        root.destroy()  
# Note application

Notepad = ctk.CTkTextbox(root,width=180,height=120,corner_radius=0)

Notepad.place(x=160,y=60)
root.protocol("WM_DELETE_WINDOW", on_closing) # doent let us quit
close_image_button = ctk.CTkButton(root,text="",bg_color="red",width=10,height=10,command=rem_img,corner_radius=0,fg_color="red",)
close_image_button.place(x=320,y=10)

 


root.mainloop()



close_button = "ON YOUR  DREAMS"


# Padhle bkl , code review kahe ko kar raha 
# tu task manager se bhi band kar sakta hai I know -- but dekh tu kitna gir chuka hai , padhaayi bhi thikse nhi kiya jara