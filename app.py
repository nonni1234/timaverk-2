import PySimpleGUI as sg
from time import sleep

menu = [["People",["Nonni","Sessa"]],["Matur",["Epli","Banani"]]]
layout = [
    [sg.Menu(menu)],
    [sg.Text("Færðu þennan glugga til hægri eða vinstri")],
    [sg.Button(button_text="Left",key="a"),sg.Button(button_text="Right",key="d"),sg.Button(button_text="Up",key="w"),sg.Button(button_text="Down",key="s")]
]

window = sg.Window("Test Window", layout,button_color=("white","blue"), transparent_color=("cyan"),return_keyboard_events=True)

while True:
    event, values = window.read()
    location = window.current_location()
    x = location[0]
    y = location[1]
    if event in (None, 'Cancel',"Ok"):   # if user closes window or clicks cancel
        print('You entered ', values[0])
        break
    if event in ("Nonni"):
        print("uwu")
    if event == "a":
        x-=50
        window.move(x,y)
    if event == "d":
        x+=50
        window.move(x,y)
    if event == "s":
        y+= 50
        window.move(x,y)
    if event == "w":
        y-= 50
        window.move(x,y)
window.close()