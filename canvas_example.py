import tkinter as tk
import tkinter.ttk as ttk

import tktween
        

window = tk.Tk()

window.geometry("640x480")

canvas = tk.Canvas(window)
square = canvas.create_polygon(
    20, 20+ 150,
    20, 70+ 150,
    70, 70+ 150,
    70, 20+ 150,
    fill='red'
)

circle = canvas.create_oval(
    80, 20,
    130, 70,
    fill='green'
)

circle_2 = canvas.create_oval(
    80 + 100, 20 + 100,
    130 + 100, 70 + 100,
    fill='green'
)


tween = tktween.CanvasTween(
    tktween.canvas.Translate(dx=100),
    duration=.75,
    easing=tktween.Easing.QUADRATIC_IN
).then(
    tktween.canvas.Translate(dy=100),
    duration=.75,
    easing=tktween.Easing.QUADRATIC_OUT
).parallel(
    tktween.canvas.FillColor(end_color='blue', mode='hsv'),
    easing=tktween.Easing.QUADRATIC_IN_OUT
)

tween.add_callback(lambda h: print("Tween finished (local)"))

canvas.pack(fill='both', expand=True)

tktween.on_tween_finished(lambda handle: print("Tween finished (global)"))

tween.run(canvas, square, True)
tween.run(canvas, circle, False)
tween.inverse().run(canvas, circle_2, False)

window.mainloop()