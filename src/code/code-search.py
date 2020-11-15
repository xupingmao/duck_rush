#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# @author xupingmao <578749341@qq.com>
# @since 2020/11/12 21:43:07
# @modified 2020/11/12 21:52:48

#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# @author xupingmao <578749341@qq.com>
# @since 2020/10/14 00:04:26
# @modified 2020/11/12 15:45:52
import os
import argparse
import sys
import chardet

CODE_EXT_SET = set([
    ".txt", 
    ".c", ".h", ".cc", ".cpp",
    ".java", 
    ".py", 
    ".html", ".js", ".css",
    ".rb",
    ".sql"
])

# [[func1, args], [func2, args2]]
COMMANDS = []
# 5M
FILE_SIZE_LIMIT = 1024 * 1024 * 5


def set_console_font_color(color):
    if color == "red":
        sys.stdout.write("\033[31m")
    if color == "green":
        sys.stdout.write("\033[32m")
    if color == "orange":
        sys.stdout.write("\033[33m")
    if color == "blue":
        sys.stdout.write("\033[34m")
    if color == "default":
        sys.stdout.write("\033[0m")

class CodeFinder:

    def __init__(self, fpath, source):
        self.fpath  = fpath
        self.lines  = []
        self.source = source
        self.encoding = None

    def get_result(self):
        if len(self.lines) > 0:
            return self
        return None

    def append(self, line):
        self.lines.append(line)

    def readfile(self, fpath):
        last_err = None
        ENCODING_TUPLE = ("utf-8", "gbk", "mbcs", "latin_1")

        for encoding in ENCODING_TUPLE:
            try:
                with open(fpath, encoding = encoding) as fp:
                    text = fp.read()
                    self.encoding = encoding
                    return text
            except Exception as e:
                last_err = e
        if raise_error:
            raise Exception("can not read file %s" % path, last_err)

    def do_find(self):
        text      = self.readfile(self.fpath)
        self.text = text

        for index, line in enumerate(text.split("\n")):
            if self.source in line:
                self.lines.append((index,line))

    def print_detail(self):
        set_console_font_color("blue")
        print("\nFile: %s" % self.fpath)
        set_console_font_color("default")

        for index, line in self.lines:
            print("%04d: %s" % (index,line))

def is_code_file(fpath):
    _, ext = os.path.splitext(fpath)
    return ext in CODE_EXT_SET


def get_file_size(fpath, format=False):
    st = os.stat(fpath)
    if st and st.st_size >= 0:
        return st.st_size
    return -1

def check_file_size(fpath):
    size = get_file_size(fpath)
    if size < 0:
        return "os.stat failed"
    if size > FILE_SIZE_LIMIT:
        return "file too large"

def readfile(fpath):
    last_err = None
    ENCODING_TUPLE = ("utf-8", "gbk", "mbcs", "latin_1")

    for encoding in ENCODING_TUPLE:
        try:
            with open(fpath, encoding = encoding) as fp:
                return fp.read()
        except Exception as e:
            last_err = e
    if raise_error:
        raise Exception("can not read file %s" % path, last_err)


def find_in_file(fpath, source):
    finder = CodeFinder(fpath, source)

    error = check_file_size(fpath)
    if error != None:
        print("WARN: READ_FILE_FAILED fpath: %s, error: %s" % (fpath, error))
        return

    finder.do_find()
    return finder.get_result()


def code_search(dirname, source = None):
    results = []

    for root, dirs, files in os.walk(dirname):
        for fname in files:
            fpath = os.path.join(root, fname)
            if not is_code_file(fpath):
                continue
            find_result = find_in_file(fpath, source)
            if find_result is None:
                continue
            results.append(find_result)

    for result in results:
        result.print_detail()

    if len(results) > 0:
        print("\nFind Code in %d files" % len(results))
    else:
        print("No file matched")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument("dirname")
    parser.add_argument("source")

    args    = parser.parse_args()
    dirname = "./"
    code_search(dirname, source = args.source)

