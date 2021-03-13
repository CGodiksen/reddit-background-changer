import json
import os


class Settings:
    def __init__(self):
        # If the settings file does not already exist then initialize the settings file.
        if "settings.json" not in os.listdir("../resources"):
            self.initialize_file()

        self.client_id = ""
        self.client_secret = ""
        self.user_agent = ""
        self.change_frequency = 0
        self.blacklist = []

        self.load_settings()

    def load_settings(self):
        """Loading the current settings from the settings file."""
        with open("../resources/settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            self.client_id = settings["client_id"]
            self.client_secret = settings["client_secret"]
            self.user_agent = settings["user_agent"]
            self.change_frequency = settings["change_frequency"]
            self.blacklist = settings["blacklist"]

    def save_settings(self):
        """Saving the current settings to the the settings file"""
        with open("../resources/settings.json", "w") as settings_file:
            json.dump({"client_id": self.client_id,
                       "client_secret": self.client_secret,
                       "user_agent": self.user_agent,
                       "change_frequency": self.change_frequency,
                       "blacklist": self.blacklist}, settings_file)

    @staticmethod
    def initialize_file():
        """Initializes the settings file."""
        with open("../resources/settings.json", "w+") as settings_file:
            json.dump({"client_id": "",
                       "client_secret": "",
                       "username": "",
                       "change_frequency": 30,
                       "blacklist": []}, settings_file)
