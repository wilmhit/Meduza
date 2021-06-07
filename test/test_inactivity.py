import unittest
from server_utils.inactivity import InactivityStore

class InactivityTest(unittest.TestCase):
    def test_registering(self):
        store = InactivityStore(4)
        store.register_inactivity(["client_1", "client_2"])

        self.assertEqual(len(store.inactive_keys), 0)

        store.register_inactivity(["client_1", "client_2"])
        store.register_inactivity(["client_1"])
        store.register_inactivity(["client_1", "client_2"])

        self.assertEqual(len(store.inactive_keys), 1)

        store.register_inactivity(["client_1", "client_2"])
        store.register_inactivity(["client_1", "client_2"])
        store.register_inactivity(["client_1", "client_2"])

        self.assertEqual(len(store.inactive_keys), 2)

        store.remove_key("client_1")
        store.register_inactivity(["client_2"])
        self.assertEqual(len(store.inactive_keys), 1)
    
    def test_for_renewed_activity(self):
        store = InactivityStore(4)
        store.register_inactivity(["client"])
        store.register_inactivity(["client"])
        store.register_inactivity(["client"])
        store.register_inactivity([])
        store.register_inactivity(["client"])
        store.register_inactivity(["client"])
        store.register_inactivity(["client"])
        
        self.assertEqual(len(store.inactive_keys), 0)
