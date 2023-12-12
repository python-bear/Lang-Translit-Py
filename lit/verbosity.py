import time
import colorama
from colorama import Fore as fr, Style as st, Back as bk


colorama.init(autoreset=True)


bac = "\x1b[D"


class Speaker:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.styles = {
            "title": f"{fr.MAGENTA}### {st.BRIGHT}",
            "heading": f"{fr.YELLOW}## {st.BRIGHT}",
            "error": f"{fr.WHITE}! {st.BRIGHT}{fr.RED}",
            "info": f"{fr.WHITE}! {st.BRIGHT}{fr.BLUE}",
            "success": f"{fr.WHITE}! {st.BRIGHT}{fr.CYAN}",
            "normal": "",
        }

    def speak(self, text: str | list, style: str = "normal", end: str = "\n", pause: float = 0):
        if self.verbose:
            if isinstance(text, list):
                if isinstance(text[0], str):
                    print(f"{self.styles[style]}{text[1]}{text[0]}", end=end, flush=True)
                    time.sleep(pause)
                else:
                    for line in text:
                        if isinstance(line, list):
                            print(f"{self.styles[style]}{line[1]}{line[0]}", end=end, flush=True)
                            time.sleep(pause)
                        else:
                            print(f"{self.styles[style]}{line}", end=end, flush=True)
                            time.sleep(pause)
            else:
                print(f"{self.styles[style]}{text}", end=end, flush=True)
                time.sleep(pause)


s = Speaker(True)
