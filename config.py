import os
import ConfigParser


class Config():
    def __init__(self, config_path=None):
        self.EMAIL = ""
        self.SMTP_SERVER = ""
