import pickle

def load_inverted_index(file_path: str) -> {str: [dict]}:
    with open(file_path, 'rb') as read_file:
        return pickle.load(read_file)


ii = load_inverted_index('./inverted_index')

print(len(ii))
print(ii)