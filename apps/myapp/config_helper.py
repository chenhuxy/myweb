#!/usr/bin/env python
# -*- coding:utf-8 -*-

import configparser


class CustomConfigParser(configparser.ConfigParser):
    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        for section in self.sections():
            fp.write(f"[{section}]\n")
            for key, value in self.items(section):
                # Assume key is not used, value contains the full line
                fp.write(f"{value}\n")
            fp.write("\n")