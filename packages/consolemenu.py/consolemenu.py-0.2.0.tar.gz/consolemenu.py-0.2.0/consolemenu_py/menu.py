#  SPDX-FileCopyrightText: 2024 Pirulax <patrikjankovics7@gmail.com>
#  SPDX-License-Identifier: MIT

import logging
import os
from typing import Optional

from aioconsole import ainput, aprint

from .menuitem import MenuItem

logger = logging.getLogger(__name__)

async def clear_console():
    """
    Clear the console - Works on both Linux and Windows
    """

    os.system("cls||clear") # https://stackoverflow.com/a/36941376

class Menu(MenuItem):
    """
    A menu that can contain MenuItem's [and/or other Menu's as well]
    """

    def __init__(
        self,
        name : str,
    ) -> None:
        """
        :arg name: The name (title) of the menu
        """

        super().__init__(
            name
        )

        self.items : list[MenuItem] = []
        self.prev_menu : Optional[Menu] = None

    def add_item(self, item : MenuItem):
        """
        Add an item to the console
        """

        self.items.append(item)
        return self # For chaining

    async def show(self):
        """
        Show the menu [print it to the console]
        """

        title = f'+---[{self.get_current_menu_path()}]----'
        await aprint(title)
        await aprint(f"|>\t{0}. {'Exit' if self.prev_menu is None else 'Return'}")
        for i, menu_item in enumerate(self.items):
            await aprint(f'|>\t{i + 1}. {menu_item.name}')
        await aprint(f'+{"-" * (len(title) - 1)}')

    async def await_user_interaction(self):
        """
        Await the user to select a menu item.
        Remember to show them the screen using `show()`
        """

        while True:
            try:
                selected_item_idx = int(await ainput("|> Select menu item: "))
            except ValueError:
                continue
            
            # Check if the index is valid
            if selected_item_idx >= len(self.items) + 1: # +1 for `Return`/`Exit`
                await aprint("Invalid menu number!")
                continue

            break

        if selected_item_idx == 0:
            # If we can't go back, that means we're done
            if self.prev_menu is None:
                return None, None
            
            # Otherwise go back to the previous menu
            return self.prev_menu, None
        else:
            # Process selected menu item
            selected_menu_item = self.items[selected_item_idx - 1]

            user_select_result = await selected_menu_item.on_user_select(self)

            if isinstance(selected_menu_item, Menu):
                return selected_menu_item, user_select_result
            
            return self, user_select_result

    async def on_user_select(self, from_menu : "Menu"):
        """
        Display this menu to the user
        """

        self.prev_menu = from_menu
        
        await clear_console()
        await self.show()

    def get_current_menu_path(self):
        """
        Get path to the current menu
        """

        path = []
        
        i = self
        while i:
            path.append(i)
            i = i.prev_menu

        return '/'.join(m.name for m in reversed(path))
        
class MainMenu(Menu):
    """
    The main menu.
    This menu is supposed to be the very first menu created, and all others Menu's
    are just sub-menus of it.
    After initializing it, just call the `run` function and it'll manage the rest.
    """

    async def run(self):
        """
        Main run function for the menu
        Call this on program startup

        NOTE: Doesn't return as long as the menu is visible
        """

        await clear_console()
        await self.show()

        current_menu = self
        
        while current_menu:
            try:
                # Wait for user interaction
                new_menu, user_select_result = await current_menu.await_user_interaction()

                # No new menu? So exit...
                if not new_menu:
                    logger.debug('MainMenu loop exited...')
                    return user_select_result 
                
                # Are we entering a different menu?
                if new_menu != current_menu:
                    await clear_console()
                    await new_menu.show()
                    current_menu = new_menu

            except Exception: # Catch exceptions here so prevent the main loop from stopping
                logger.exception("Ignoring exception in main menu loop")
