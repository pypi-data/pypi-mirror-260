import re
import json
from urllib.parse import urlparse
from datetime import datetime


folder_start_pattern = r"<DT><H3.*>(.*?)</H3>"
folder_end_pattern = r"</DL>"
entry_pattern = r'^\s*<DT><A HREF="(.*)" ADD_DATE="([0-9]+)".*>(.*)</A>.*$'


class Entry:
    def __init__(self, folders, em):
        self.folders = [fo for fo in folders]
        self.url = em.group(1)
        self.datetime = datetime.fromtimestamp(float(em.group(2))).strftime("%F %T")
        self.title = em.group(3)

    @property
    def netloc(self):
        return urlparse(self.url).netloc if self.url is not None else None

    def to_json(self, *keys):
        data = {}
        for key in keys:
            data[key] = getattr(self, key)
        return json.dumps(data, ensure_ascii=False)

    def __repr__(self):
        folder_str = "/".join(self.folders)
        return f"{folder_str}/{self.title}"


def read(bookmark_path):
    with open(bookmark_path) as f:
        stack = []
        for line in f:
            entry_matcher = re.search(entry_pattern, line)
            if entry_matcher:
                yield Entry(stack, entry_matcher)
                continue

            folder_matcher = re.search(folder_start_pattern, line)
            if folder_matcher:
                folder_name = folder_matcher.group(1) if folder_matcher else None
                stack.append(folder_name)
            elif re.search(folder_end_pattern, line) and len(stack) > 0:
                stack.pop()
            else:
                pass
