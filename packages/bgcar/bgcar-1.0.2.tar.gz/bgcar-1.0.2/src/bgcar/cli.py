import argparse
import logging
import pickle
import queue
import sys
import time
from pathlib import Path

import easyocr
import numpy
from PIL import ImageGrab
from pynput import keyboard, mouse
from rich.logging import RichHandler
from rich.console import Console


console = Console()
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)

click_q = queue.LifoQueue()


class ScreenPositions:

    store_btn_desc = "Store button"
    recall_btn_desc = "Recall button"
    reroll_btn_desc = "Reroll button"
    total_roll_desc = "Total roll score"

    # load cached param
    @classmethod
    def init_cached(cls, config_filename="config.json"):
        config_file_path = Path(__file__).with_name(config_filename)
        try:
            with config_file_path.open("rb") as config_file:
                return pickle.load(config_file)
        except FileNotFoundError:
            logger.error(
                "Config file '{0}' not found.\n"
                "Please initialize settings using '-i' parameter.".format(
                    config_filename
                )
            )
            sys.exit(1)

    def __init__(self, save=True):
        m_listener = mouse.Listener(on_click=self.on_click)
        m_listener.start()

        self.store_btn_pos = self.get_pos(ScreenPositions.store_btn_desc)
        self.recall_btn_pos = self.get_pos(ScreenPositions.recall_btn_desc)
        self.reroll_btn_pos = self.get_pos(ScreenPositions.reroll_btn_desc)

        total_roll_tl_pos = self.get_pos(
            "{} top left".format(ScreenPositions.total_roll_desc)
        )
        total_roll_br_pos = self.get_pos(
            "{} bottom right".format(ScreenPositions.total_roll_desc)
        )
        self.total_roll_pos = total_roll_tl_pos + total_roll_br_pos

        m_listener.stop()

        if save:
            self.write_settings()

    def on_click(self, x, y, button, pressed):
        if pressed:
            click_q.put([x, y])

    def get_pos(self, description):
        console.print("> Click on [cyan]{0}[white]".format(description))
        return click_q.get()

    def write_settings(self, config_filename="config.json"):
        config_file_path = Path(__file__).with_name(config_filename)
        with config_file_path.open("wb") as config_file:
            pickle.dump(self, config_file, protocol=pickle.HIGHEST_PROTOCOL)


class RollScore(ScreenPositions):

    def __init__(
        self, load=False, gpu=False, delay=0.03, highest_roll=0, current_roll=0
    ):
        if not load:
            super().__init__()
        else:
            cached_param_dict = self.init_cached().__dict__
            # inject cached param from parent class
            for cached_param_key in cached_param_dict:
                setattr(self, cached_param_key, cached_param_dict[cached_param_key])
        self.reader = easyocr.Reader(["en"], gpu=gpu)
        self.mouse_instance = mouse.Controller()
        self.delay = delay
        # recall previous (potential) previous highest roll
        self.recall_click()
        self._get_current_roll()
        self.highest_roll = self.current_roll

        logger.debug(self.__dict__)

    def _m_click(self, position):
        self.mouse_instance.position = position
        self.mouse_instance.click(mouse.Button.left, 1)
        time.sleep(self.delay)

    def store_click(self):
        self._m_click(self.store_btn_pos)

    def recall_click(self):
        self._m_click(self.recall_btn_pos)

    def reroll_click(self):
        self._m_click(self.reroll_btn_pos)
        self._get_current_roll()

    def grab_screen_array(self, bbox):
        return numpy.array(ImageGrab.grab(bbox=bbox))

    def _get_current_roll(self):
        try:
            self.current_roll = int(
                self.reader.readtext(
                    self.grab_screen_array(self.total_roll_pos),
                    allowlist=list(map(str, range(0, 10))),
                )[0][1]
            )
            logger.debug("Current roll: {}".format(self.current_roll))
        except IndexError:
            logger.info("OCR was unable to read value. Defaulting to 0")
            self.current_roll = 0


def on_press(key, abort_key="t"):
    try:
        keystroke = key.char
    except AttributeError:
        keystroke = key.name

    if keystroke == abort_key:
        return False


def parse_args():
    parser = argparse.ArgumentParser(
        prog="bgcar",
        description=(
            "Baldur's Gate Computer Assisted Reroll (BGCAR) helps one effortlessly "
            "reach high ability scores for one's CHARNAME by performing computer "
            "assisted reroll. This program performs live roll result analysis and "
            "only stores the highest value."
        ),
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="print debug level messages (each roll value, etc)",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-i",
        "--initialize",
        required=False,
        default=False,
        action="store_true",
        help=(
            "initialize required settings like button location -"
            " mandatory before program use"
        ),
    )
    parser.add_argument(
        "-t",
        "--time",
        required=False,
        default=0.03,
        type=float,
        help=(
            "time in second to wait between each click (one can use decimal values);"
            " a delay too short for your setup might cause the program to misbehave "
            "(eg. not store roll correctly) (default: %(default)s)"
        ),
    )
    parser.add_argument(
        "-m",
        "--max-roll-count",
        required=False,
        type=int,
        help=(
            "limit the maximum number of roll that you want the program to perform;"
            " by default {0} will run in infinite mode".format(parser.prog)
        ),
    )
    parser.add_argument(
        "--gpu",
        required=False,
        default=False,
        action="store_true",
        help=("enable GPU mode for OCR and accelerating program"),
    )
    return parser.parse_args()


def main():
    args = parse_args()

    logger.setLevel(args.loglevel)
    # Ensure game has enough time to store roll
    delay = 0.03 if args.time < 0.03 else args.time

    if args.initialize:
        with console.status("[magenta]Gathering user inputs", spinner="arc"):
            roll_score = RollScore(gpu=args.gpu, delay=delay)
    else:
        with console.status("[magenta]Loading settings", spinner="arc"):
            roll_score = RollScore(load=True, gpu=args.gpu, delay=delay)

    with console.status(
        "[magenta]Rolling hard...\n[white]Press 't' to exit",
        spinner="arc",
    ):
        break_key_listener = keyboard.Listener(on_press=on_press)
        break_key_listener.start()

        # Set roll_count above target_roll for infinity mode
        roll_count = 1

        console.print(
            "[green]Initiating roll. Starting value: [bold white]{0}\n".format(
                roll_score.highest_roll
            ),
        )
        while roll_count != args.max_roll_count and break_key_listener.is_alive():
            roll_score.reroll_click()
            if roll_count % 10 == 0:
                console.print(
                    "[cyan]Roll count: [bold white]{0}".format(roll_count),
                    "[cyan]Current maximum: [bold white]{0}".format(
                        roll_score.highest_roll
                    ),
                    "",
                    sep="\n",
                )
            if roll_score.current_roll > roll_score.highest_roll:
                roll_score.store_click()
                roll_score.highest_roll = roll_score.current_roll
                console.print(
                    "[green]New maximum: [bold white]{0}\n".format(
                        roll_score.highest_roll
                    )
                )
            roll_count += 1

        roll_score.recall_click()

    console.print(
        "[orange1]Rolling done...",
        "[green]Final highest roll: [bold white]{0}".format(roll_score.highest_roll),
        "[magenta]Final roll count: [white]{0}".format(roll_count),
        sep="\n",
    )


if __name__ == "__main__":
    main()
