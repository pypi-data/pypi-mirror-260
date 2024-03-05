import hashlib


def get_digest(filename):
    try:
        with open(filename, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except FileNotFoundError:
        return None


if __name__ == "__main__":
    print(get_digest(__file__))
