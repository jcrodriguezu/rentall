import os


def file_list_as_url(name, path="/scrapers-data/html/"):
    return [f"file:////{f.path}" for f in os.scandir(path=path)
            if f.is_file() and name in f.name]
