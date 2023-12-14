import tkinter as tk
import tkinter.ttk as ttk

import tktween
        

window = tk.Tk()
style = ttk.Style()
style.configure("my.TFrame", background="red")

window.geometry("640x480")

frame_1 = ttk.Frame(window, width=100, height=50)
frame_2 = ttk.Frame(window, style="my.TFrame", width=100, height=50)
info = ttk.Label(window, width=100)


tween = tktween.Tween(
    tktween.Translate(x=100),
    duration=0.15
).then(
    tktween.Translate(y=50),
    duration=0.25
).parallel(
    tktween.Background(end_color='blue', mode='hsv'),
    duration=1.0
).synchronize().pause(0.5).then(
    tktween.Background(end_color='yellow'),
    tktween.Translate(y=-50),
    duration=0.35,
    easing=tktween.Easing.CUBIC_IN_OUT
)

handle = tween.run(frame_1, loop=True)

def toggle_animation():
    global handle
    if tween.is_running(frame_1):
        handle.cancel(revert=True)
        button_1.configure(text="Run Tween")
    else:
        handle = tween.run(frame_1, loop=True)
        button_1.configure(text="Cancel Tween")

button_1 = ttk.Button(
    window,
    text="Cancel Tween",
    command=toggle_animation
)
button_2 = ttk.Button(
    window,
    text="Start Tween (red)",
    command=lambda: tween.run(frame_2)
)

def update_info():
    if tween.is_running(frame_1):
        info.configure(text=f"Running: True")
    else:
        info.configure(text=f"Running: False")
    window.after(10, update_info)

window.after(10, update_info)

button_1.pack(side='left', anchor='n', padx=5)
button_2.pack(side='left', anchor='n', padx=5)
info.pack(side='left', anchor='n', padx=5)
frame_1.place(x=5, y= 10 + button_1.winfo_reqheight())
frame_2.place(x=215, y= 10 + button_1.winfo_reqheight())


window.mainloop()