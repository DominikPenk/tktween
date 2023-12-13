import tkinter as tk
import tkinter.ttk as ttk

import tktween
        

window = tk.Tk()
style = ttk.Style()
style.configure("my.TFrame", background="red")

window.geometry("640x480")

canvas = tk.Canvas(window)
square = canvas.create_polygon(
    20, 20,
    20, 70,
    70, 70,
    70, 20,
    fill='red'
)

circle = canvas.create_oval(
    80, 20,
    130, 70,
    fill='green'
)

bouncy = canvas.create_oval(
    20, 200,
    30, 210,
    fill='gray'
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
    ),
    tktween.canvas.Scale(0.5),
    easing=tktween.Easing.QUADRATIC_IN_OUT
)

bouncy_tween = tktween.CanvasTween(
    tktween.canvas.Translate(dx=20),
    duration=0.3
)

canvas.pack(fill='both', expand=True)

tween.run(canvas, square, True)
tween.run(canvas, circle, False)
bouncy_tween.run(canvas, bouncy, True)

window.mainloop()