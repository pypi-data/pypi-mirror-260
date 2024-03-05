import re


def regexp_extract_first(regexp):
    def m(string):
        match = re.search(regexp, string)
        return match.group(1) if match else None

    return m


class Entry:
    xhref = regexp_extract_first(r'HREF="(.*?)"')
    xdate = regexp_extract_first(r'ADD_DATE="(.*?)"')
    xtitle = regexp_extract_first(r"<A.*>(.*?)</A>")

    def __init__(self, folders, line):
        self.folders = [fo for fo in folders]
        self.url = self.__class__.xhref(line)
        self.date = self.__class__.xdate(line)
        self.title = self.__class__.xtitle(line)

    def __repr__(self):
        folder_str = "/".join(self.folders)
        return f"{folder_str}/{self.title}"


def read(bookmark_path):
    folder_start_pattern = r"<DT><H3"
    folder_end_pattern = r"</DL>"
    entry_pattern = r"<DT><A"
    extract_folder = regexp_extract_first(r"<H3.*>(.*?)</H3>")

    with open(bookmark_path) as f:
        stack = []
        for line in f:
            if re.search(entry_pattern, line):
                yield Entry(stack, line)
            elif re.search(folder_start_pattern, line):
                folder_name = extract_folder(line)
                stack.append(folder_name)
            elif re.search(folder_end_pattern, line) and len(stack) > 0:
                stack.pop()
            else:
                pass
