## What's this?
A simple Python console (terminal) menu that work's on any OS and is navigable by only using a keyboard.

## Usage
#### Example code:
```py
import consolemenu_py as cm

async def main():
    # Create the main menu. The name should usually be the name of your program
    mm = cm.MainMenu("Example Program")

    # This will enter an empty sub-menu
    mm.add_item(cm.Menu("A sub-menu!"))

    # This will print "Hello World!" to the console
    mm.add_item(cm.FunctionMenuItem("A function menu item", lambda _: print("Hello World!")))

    # This will only return if the user exists the main menu
    await mm.run()
```

#### Will look like this:
![](https://raw.githubusercontent.com/Pirulax/consolemenu.py/master/docs/img/example.png)

## License
This package is licensed under MIT, see `LICENSE`