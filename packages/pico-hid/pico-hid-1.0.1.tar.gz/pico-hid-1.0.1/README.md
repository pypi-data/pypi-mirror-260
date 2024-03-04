# pico-hid

Python package to control pico spoofed as keyboard/mouse via serial pins (uart)

## Installation

You can install the package via pip:

```bash
pip install pico-hid
```

## Usage

```python
from pico_hid import keyboard
from pico_hid import mouse

mouse.move(100, 100)
mouse.click()

keyboard.press("control_left")
keyboard.press_and_release("a")
keyboard.release("control_left")
keyboard.write("hello world")
```

## License

This project is licensed under the terms of the MIT license.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact

If you want to contact me you can reach me at pradish@sandbox.com.np.
