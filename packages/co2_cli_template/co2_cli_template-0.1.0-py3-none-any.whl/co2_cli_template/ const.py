from pathlib import Path

from co2.const import Settings as SettingsInherit

_path = Path(__file__).absolute().parent


class Settings(SettingsInherit):
    ...


settings: Settings = Settings()
