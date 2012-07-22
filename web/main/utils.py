def here(path):
    import os
    dir = os.path.dirname(__file__)
    return os.path.join(dir, path)