from collections import defaultdict

class InactivityStore:
    def __init__(self, inactivity_treshold=100):
        self.treshold = inactivity_treshold
        self.keys = defaultdict(lambda: 0)

    def register_inactivity(self, inactive_keys):
        for key in inactive_keys:
            self.keys[key] += 1
        active_keys = [key for key in self.keys.keys() if key not in inactive_keys]
        for key in active_keys:
            del self.keys[key] 

    def remove_key(self, key):
        del self.keys[key]

    @property
    def inactive_keys(self):
        return [
            key for key, inactivity in self.keys.items()
            if inactivity >= self.treshold
        ]
