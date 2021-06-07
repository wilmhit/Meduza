from collections import defaultdict

class InactivityStore:
    def __init__(self, inactivity_treshold=1000):
        self.treshold = inactivity_treshold
        self.keys = defaultdict(lambda: 0)

    def register_inactivity(self, keys):
        for key in keys:
            self.keys[key] += 1

    def remove_key(self, key):
        del self.keys[key]

    @property
    def inactive_keys(self):
        return [
            key for key, inactivity in self.keys.items()
            if inactivity >= self.treshold
        ]
