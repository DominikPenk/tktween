import tkinter as tk
import tkinter.ttk as ttk

import tktween
        

window = tk.Tk()
style = ttk.Style()
style.configure("my.TFrame", background="red")

window.geometry("640x480")

frame_1 = ttk.Frame(window, width=100, height=50)
frame_2 = ttk.Frame(window, style="my.TFrame", width=100, height=50)


tween = tktween.Tween(
    tktween.Translate(x=100),
    tktween.Background(end_color='blue'),
    duration=0.15
).then(
    tktween.Translate(y=50),
    duration=0.25
)

button_1 = ttk.Button(
    window,
    text="Start Tween",
    command=lambda: tween.run(frame_1)
)
button_2 = ttk.Button(
    window,
    text="Start Tween (red)",
    command=lambda: tween.run(frame_2)
)

button_1.place(x=5, y=5)
button_2.place(x=button_1.winfo_reqwidth() + 10, y=5)
frame_1.place(x=5, y= 10 + button_1.winfo_reqheight())
frame_2.place(x=215, y= 10 + button_1.winfo_reqheight())

window.mainloop()