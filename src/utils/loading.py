import time

def loading_animation():
    dots = ""
    for i in range(3):
        dots += "."
        print("Thinking" + dots, end="\r")
        time.sleep(0.5)
    print(" " * len(dots), end="\r")