from dataclasses import dataclass

import config


@dataclass
class HistoriqueSynchronisation:
    date: str
    synchro_message: str

    def save_synchronisation(self):
        pass
