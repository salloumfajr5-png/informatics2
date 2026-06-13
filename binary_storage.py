# Author = Саллум Фажр
# Group = P3212
# Date = 06.06.2025

import pickle


def serialize_binary(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def deserialize_binary(path):
    with open(path, 'rb') as f:
        return pickle.load(f)
