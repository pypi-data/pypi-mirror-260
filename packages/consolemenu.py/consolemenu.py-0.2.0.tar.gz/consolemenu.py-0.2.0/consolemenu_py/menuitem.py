#  SPDX-FileCopyrightText: 2024 Pirulax <patrikjankovics7@gmail.com>
#  SPDX-License-Identifier: MIT

import inspect
import logging
from typing import Any, Awaitable, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .menu import Menu

logger = logging.getLogger(__name__)

class MenuItem:
    """
    Basic MenuItem
    Feel free to derive from it and implement your own `on_user_select` function
    """

    def __init_subclass__(cls, name : str = None) -> None:
        """
        This will allow us to do this:
        class MyMenuItem(MenuItem, name='My Menu Item'):
            pass
        """

        if name is not None:
            cls.name = name
        
    def __init__(
        self,
        name : str = None
    ) -> None:
        """
        :arg name: The name displayed to the user
        """

        if not hasattr(self, 'name'):
            if name is None:
                raise ValueError('MenuItem must have a `name`')
            else:
                self.name = name
        # else: Name is already set
    
    async def on_user_select(self, from_menu : "Menu"):
        """
        Do whatever the fuck is necessary in case the user selected this menu item

        :arg from_menu: The menu this item is in
        """

        raise NotImplementedError

class FunctionMenuItem(MenuItem):
    """
    A menu item that calls a function upon the user selecting it
    """

    def __init__(
        self, 
        name: str,
        fn : Callable[["Menu"], Any]
    ) -> None:
        """
        :arg name: The name of this menu item
        :arg fn: The function to call when this menu item is opened (This may be an awaitable function, lambad, or anything Callable)
        """

        super().__init__(
            name
        )

        self.fn = fn

    async def on_user_select(self, from_menu : "Menu"):
        """
        Call the function when the user has selected this menu item
        """

        logger.debug("[FunctionMenuItem]: Calling function (%s) [self=%s]", self.fn, self)

        fn_ret = self.fn(from_menu)
        if inspect.iscoroutine(fn_ret):
            fn_ret = await fn_ret
        return fn_ret
