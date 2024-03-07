import curses
from curses.textpad import rectangle
from typing import List, Optional
import time
import json
import os
from fuck_game.game_level import dispatcher
import sys


class GameUI:

    def __init__(self):
        level = 1
        curr_path = os.path.dirname(os.path.abspath(__file__))
        self.conf_path = os.path.join(curr_path, os.path.pardir, 'game.json')
        if os.path.exists(self.conf_path):
            with open(self.conf_path, 'r') as f:
                conf = json.load(f)
                level = conf.get('level', 1)
        self.level = level
        self.game_level = dispatcher.get(level)(self)
        self.KEYS_DEL: List[int] = [127, 8, curses.KEY_DL, curses.KEY_DC, curses.KEY_BACKSPACE]
        self.stdscr = None
        self.height: None | int = None
        self.width: None | int = None
        self.x_center: None | int = None
        self.y_center: None | int = None
        self.ID_COLOR_RED: int = 1
        self.KEY_QUIT: int = ord('!')
        self.KEY_RESTART: int = ord('?')
        curses.wrapper(self.init_screen)

    def restart_game(self):
        self.level = 1
        self.game_level = dispatcher.get(self.level)(self)
        with open(self.conf_path, 'w') as f:
            json.dump({'level': self.level}, f)

    def init_screen(self, stdscr):
        self.stdscr = stdscr
        curses.use_default_colors()
        curses.start_color()
        curses.init_pair(self.ID_COLOR_RED, curses.COLOR_RED, -1)
        self.controller()

    def popup_error(self):
        self.stdscr.clear()
        error_message: str = 'Screen is to small, enlarge the window to play.'
        self.addstr(self.y_center-1, self.x_center - int(len(error_message)/2), error_message, self.ID_COLOR_RED)

    def refresh_screen(self):
        # Initialization
        self.stdscr.clear()
        self.height, self.width = self.stdscr.getmaxyx()
        self.x_center = int(self.width / 2)
        self.y_center = int(self.height / 2)

        # Render rectangle
        rectangle(self.stdscr, self.y_center-1, self.x_center-15, self.y_center+1, self.x_center+15)
        # Render input text
        start_x_input_text = self.x_center-15 + 1
        self.stdscr.addstr(self.y_center, start_x_input_text, self.game_level.input_text)

        # Render info
        info = "Try to write fuck"
        start_x_info = self.x_center - int(len(info)/2)
        self.stdscr.addstr(self.y_center+2, start_x_info, info)

        # Render level
        info_menu: str = f'(Level {self.level}) [?]new game [!]quit'
        self.stdscr.addstr(self.height - 1, 0, info_menu + ' ' * (self.width - len(info_menu) - 1), curses.A_STANDOUT)

        # cursor
        self.stdscr.move(self.y_center, start_x_input_text+len(self.game_level.input_text))

        # Refresh the screen
        self.stdscr.refresh()

    def controller(self):

        k = 0
        while k != self.KEY_QUIT:
            try:
                c = chr(k)
                if k in self.KEYS_DEL:
                    self.game_level.on_key_del()
                elif k == self.KEY_RESTART:
                    self.restart_game()
                elif ord('a') <= k <= ord('z') or ord('A') <= k <= ord('Z') or ord('0') <= k <= ord('9'):
                    c = c.lower()
                    self.game_level.on_key_press(c)
                if self.game_level.input_text == 'fuck':
                    self.level_up()
                    k = 127
                    continue
                self.refresh_screen()
            except curses.error as e:
                if str(e) == 'addwstr() returned ERR':
                    self.popup_error()
                else:
                    raise e
            except NotImplementedError:
                self.popup_game_done()
            k = self.stdscr.getch()

    def level_up(self):
        self.game_level.end()
        self.popup_level_up()
        curses.flushinp()
        self.level += 1
        if self.level not in dispatcher:
            raise NotImplementedError(f'{self.level} not implented yet')
        with open(self.conf_path, 'w') as f:
            json.dump({'level': self.level}, f)
        self.game_level = dispatcher.get(self.level)(self)

    def popup_level_up(self):
        self.stdscr.clear()
        curses.curs_set(0)  # make cursor invisible
        level_up_text = "Level up!!"
        start_x_level_up_text = self.x_center-15 + 1
        self.stdscr.addstr(self.y_center, start_x_level_up_text, level_up_text)
        self.stdscr.refresh()
        time.sleep(3)
        curses.curs_set(1)  # make cursor visible

    def popup_game_done(self):
        self.stdscr.clear()
        level_up_text = "You finish the game (it's still in dev mode). Press [?] to restart or [!] to quit"
        start_x_level_up_text = self.x_center-15 + 1
        self.stdscr.addstr(self.y_center, start_x_level_up_text, level_up_text)
        self.stdscr.refresh()
        while True:
            k = self.stdscr.getch()
            if k == self.KEY_QUIT:
                sys.exit(0)
            elif k == self.KEY_RESTART:
                self.restart_game()
                break

    def addstr(self, y: int, x: int, text: str, id_color_pair: Optional[int] = None):
        if id_color_pair:
            self.stdscr.attron(curses.color_pair(id_color_pair))
        self.stdscr.addstr(y, x, text)
        if id_color_pair:
            self.stdscr.attroff(curses.color_pair(id_color_pair))