from pico_hid.serial_com import send


def move(
    x: int,
    y: int,
    monitor_width: int = 1920,
    monitor_height: int = 1080,
):
    x_normalized = x * 32767 // monitor_width
    y_normalized = y * 32767 // monitor_height
    return send(f"mouse_move,{x_normalized},{y_normalized}\n")


def press(button: str = "left"):
    return send(f"mouse_press_{button}\n")


def release():
    return send(f"mouse_release\n")


def click(button: str = "left"):
    return send(f"mouse_click_{button}\n")
