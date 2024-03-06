# SimpleTurtle

import turtle

options = {
    "width": 800,
    "height": 600,
    "title": "SimpleTurtle Triangle Demo",
    "penwidth": 5
}


def run():
    turtle.title(options["title"])
    turtle.pensize(options["penwidth"])
    turtle.screensize(options["width"], options["height"])
    turtle.mainloop()


def f(distance: float):
    turtle.forward(distance)


def b(distance: float):
    turtle.back(distance)


def r(angle: float):
    turtle.right(angle)


def l(angle: float):
    turtle.left(angle)


def clr():
    turtle.clearscreen()


def ps(width: int):
    options["penwidth"] = width


def ss(width: int, height: int):
    options["width"] = width
    options["height"] = height
