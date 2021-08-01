from typing import List

import keyboard
from colorama import Fore

from ..utils import clear


class Writer:

    def __init__(self, question: str, options: List[str]):
        self.__question = question
        self.__options = options
        self.__selected = 0
        self.__answered = False

    def seek_answer(self):
        self.__answered = False
        self.write()
        up = keyboard.on_press_key("up arrow", lambda e: self.move_up())
        down = keyboard.on_press_key("down arrow", lambda e: self.move_down())
        # waits for answer
        input()
        keyboard.unhook(up)
        keyboard.unhook(down)
        self.__answered = True

    def write(self):
        clear()
        print(f"{Fore.GREEN}? {self.question}")
        for index, option in enumerate(self.options):
            color = Fore.BLUE if index == self.selected else Fore.WHITE
            print(f"{color}{index + 1} {option}")
        print(Fore.RESET)

    def move_up(self):
        if self.selected < 1:
            self.__selected = len(self.options) - 1
        else:
            self.__selected = self.selected - 1
        self.write()

    def move_down(self):
        if self.selected + 2 > len(self.options):
            self.__selected = 0
        else:
            self.__selected = self.selected + 1
        self.write()

    @property
    def question(self):
        return self.__question

    @property
    def options(self):
        return self.__options

    @property
    def selected(self):
        return self.__selected

    @property
    def answered(self):
        return self.__answered


if __name__ == "__main__":
    w = Writer("what's your favorite color?", ["red", "yellow", "blue"])
    w.seek_answer()
