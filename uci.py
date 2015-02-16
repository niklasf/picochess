# Copyright (C) 2013-2014 Jean-Francois Romang (jromang@posteo.de)
#                         Shivkumar Shivaji ()
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from utilities import *
import chess.uci
import logging
import os
import spur
import paramiko
import io
import threading
from collections import deque


class Engine(chess.uci.Engine):

    def on_line_received(self, line):
        logging.debug("<-Engine [%s]", line)
        super(Engine, self).on_line_received(line)

    def send_line(self, line):
        logging.debug("->Engine [%s]", line)
        super(Engine, self).send_line(line)

    def set_level(self, level):
        """ Sets the engine playing strength, between 0 and 20. """
        if level < 0 or level > 20:
            logging.error('Level not in range (0,20) :[%i]', level)
        if 'Skill Level' in self.options:  # Stockfish uses 'Skill Level' option
            self.setoption({"Skill Level": level})
        elif 'UCI_LimitStrength' in self.options:  # Generic 'UCI_LimitStrength' option for other engines
            if level == 20:
                self.setoption({'UCI_LimitStrength': False})
            else:
                min_elo = float(self.options['UCI_Elo'].min)
                max_elo = float(self.options['UCI_Elo'].max)
                set_elo = min(int(min_elo + (max_elo-min_elo) * (float(level)) / 19.0), self.options['UCI_Elo'].max)
                self.setoption({
                    'UCI_LimitStrength': True,
                    'UCI_Elo': set_elo,
                })
        else:
            logging.warning("Engine does not support skill levels")
