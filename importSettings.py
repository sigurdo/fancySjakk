import toml

class Settings:
    def __init__(self):
        settings = toml.load("default_settings.toml")

        try:
            localSettings = toml.load("local_settings.toml")
            for key in settings:
                if key in localSettings:
                    settings[key] = localSettings[key]
        except FileNotFoundError as err:
            pass

        # Register all settings here:
        self.stockfishPath = settings["stockfishPath"]

settings = Settings()
