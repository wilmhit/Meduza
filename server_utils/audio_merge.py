import pickle

class audioMerge:
    def __init__(self, pck_list) -> None:
        self.audio_fragments = [pickle.loads(pck[0]) for pck in pck_list]
        self.empty_fragment = self.audio_fragments[0] - self.audio_fragments[0]
        self.users = [pck[1] for pck in pck_list]
        self.fragments_with_users = zip(self.users, self.audio_fragments)
        pass

    def get_audio_for_user(self, user):
        fragments_to_merge = []

        for x in self.fragments_with_users:
            if x[0] != user:
                fragments_to_merge.append(x[1])

        if len(fragments_to_merge) == 0:
            return pickle.dumps(self.empty_fragment)
        
        merged_audio = fragments_to_merge[0]

        for x in fragments_to_merge[1:]:
            merged_audio += x

        return pickle.dumps(merged_audio)
