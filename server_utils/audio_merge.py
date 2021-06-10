import pickle

class audioMerge:
    def __init__(self, pck_list) -> None:
        self.audio_fragments = {}
        for data, user in pck_list:
            self.audio_fragments[user] = pickle.loads(data)
            
        sample_packet = pickle.loads(pck_list[0][0])
        self.empty_fragment = sample_packet - sample_packet

    def get_audio_for_user(self, excluded_user):
        fragments_to_merge = []

        for user in self.audio_fragments:
            if user != excluded_user:
                fragments_to_merge.append(self.audio_fragments[user])

        if len(fragments_to_merge) == 0:
            return pickle.dumps(self.empty_fragment)
        
        merged_audio = fragments_to_merge[0]
        for x in fragments_to_merge[1:]:
            merged_audio += x

        return pickle.dumps(merged_audio)
