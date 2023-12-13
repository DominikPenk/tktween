import tkinter as tk
import tkinter.ttk as ttk

import tktween
        

window = tk.Tk()
style = ttk.Style()
style.configure("my.TFrame", background="red")

window.geometry("640x480")

canvas = tk.Canvas(window)
circle = canvas.create_polygon(
    20, 20,
    20, 70,
    70, 70,
    70, 20,
    fill='red'
)


tween = tktween.CanvasTween(
    tktween.canvas.Translate(dx=100),
    tktween.canvas.Rotate(angle=180),
    duration=0.75,
    easing=tktween.Easing.CUBIC_IN
).then(
    tktween.canvas.Translate(dy=100),
    tktween.canvas.Rotate(angle=180),
    duration=0.75,
    easing=tktween.Easing.CUBIC_OUT
).parallel(
    tktween.canvas.FillColor(
        end_color='blue',
        mode='hsv'
    )
)

button = ttk.Button(
    window,
    text="Start Tween",
    command=lambda: tween.run(canvas, circle)
)

button.pack(side='top')
canvas.pack(fill='both', expand=True)
window.mainloop()