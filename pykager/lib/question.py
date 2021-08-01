import sys
from typing import List

import keyboard
from colorama import Fore

from ..utils import clear


class Question:

    def __init__(self, question: str, options: List[str]):
        self.__question = question
        self.__options = options
        self.__selected = 0
        self.__answered = False
        self.__has_printed = False

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
        if not self.__has_printed:
            clear()
            print(f"{Fore.GREEN}? {self.question}{Fore.RESET}")
            self.__has_printed = True
            prefix = "\r"
        else:
            prefix = "\033[A\033[A\r"

        thing = ""
        for index, option in enumerate(self.options):
            thing += f"{Fore.BLUE}> {option}" if index == self.selected else f"{Fore.WHITE}  {option}"
            thing += Fore.RESET if index + 1 == len(self.options) else "\n"

        sys.stdout.write(prefix + thing)
        sys.stdout.flush()

    def move_up(self):
        self.__selected = len(self.options) - 1 if self.selected < 1 else self.selected - 1
        self.write()

    def move_down(self):
        self.__selected = 0 if self.selected + 2 > len(self.options) else self.selected + 1
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
    q = Question("what's your favorite color", ["red", "yellow", "blue"])
    q.seek_answer()
