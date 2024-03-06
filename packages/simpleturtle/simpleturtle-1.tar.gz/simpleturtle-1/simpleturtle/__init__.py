# SimpleTurtle

import turtle

options = {
    "width": 800,
    "height": 600,
    "title": "SimpleTurtle"
}


def run():
    turtle.title(options["title"])
    turtle.screensize(options["width"], options["height"])
    turtle.mainloop()


def f(distance: float):
    turtle.forward(distance)


def b(distance: float):
    turtle.back(distance)


def r(distance: float):
    turtle.right(distance)


def l(distance: float):
    turtle.left(distance)


def clr():
    turtle.clearscreen()


def ps(width: int):
    turtle.pensize(width)


def ss(width: int, height: int):
    options["width"] = width
    options["height"] = height
