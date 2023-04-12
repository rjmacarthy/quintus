import time


def loading_animation():
    for x in range(0, 3):
        print("Thinking" + "." * x, end="\r")
        time.sleep(0.5)
