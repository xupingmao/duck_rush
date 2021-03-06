#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# @author xupingmao <578749341@qq.com>
# @since 2020/02/23 22:09:31
# @modified 2020/10/14 00:05:03
import os
import time
import sys
import platform


MUSIC_EXT_SET = set([".mp3", ".m4a", ".midi", ".wav"])

DOC_EXT_SET = set([
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", 
    ".html", ".md", ".xmind", ".txt",
    ".key", ".numbers"
])

VIDEO_EXT_SET = set([
    ".mp4", ".mkv", ".avi", ".rmvb"
])

IMAGE_EXT_SET = set([
    ".jpg", ".jpeg", ".gif", ".jfif", ".ico", ".cur", 
    ".png", ".webp", ".bmp", ".svg"
])

ARCHIVE_EXT_SET = set([
    ".zip", ".rar", ".gz",
    ".apk", ".dmg", ".pkg",
    ".exe", ".msi", ".iso"
])

# device
def is_mac():
    return platform.system() == "Darwin"

def is_windows():
    return os.name == "nt"

def makedirs(dirname):
    '''检查并创建目录(如果不存在不报错)'''
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        return True
    return False

def get_mac_birth_year(fpath):
    stat = os.stat(fpath)
    st   = time.localtime(stat.st_birthtime)
    return time.strftime("%Y", st)

def get_win_birth_year(fpath):
    stat = os.stat(fpath)
    st   = time.localtime(stat.st_ctime)
    return time.strftime("%Y", st)

def get_birth_year(fpath):
    if is_mac():
        return get_mac_birth_year(fpath)
    return get_win_birth_year(fpath)

def is_hidden_file(fname):
    # Unix/Linux hidden files
    if fname[0] == '.':
        return True
    # Mac OS hidden file
    if fname == '.DS_Store':
        return True
    return False

def check_file_by_ext(fname, ext_set):
    name, ext = os.path.splitext(fname)
    return ext.lower() in ext_set

def get_music_dir():
    # Mac和Win都是Music
    return os.path.join(os.environ['HOME'], "Music")

def get_document_dir():
    return os.path.join(os.environ['HOME'], "Documents")

def get_image_dir():
    return os.path.join(os.environ['HOME'], "Pictures")

def get_video_dir():
    if is_mac():
        return os.path.join(os.environ['HOME'], "Movies")
    return os.path.join(os.environ['HOME'], "Videos")

def get_download_dir():
    return os.path.join(os.environ['HOME'], 'Downloads')

def get_archive_dir():
    download_dir = get_download_dir()
    return os.path.join(download_dir, "Archives")

class DocumentClassifier:

    def check(self, fpath):
        return check_file_by_ext(fpath, DOC_EXT_SET)

    def get_target_path(self, fpath):
        fname = os.path.basename(fpath)
        return os.path.join(get_document_dir(), get_birth_year(fpath), fname)

class MusicClassifier:

    def check(self, fpath):
        return check_file_by_ext(fpath, MUSIC_EXT_SET)

    def get_target_path(self, fpath):
        fname = os.path.basename(fpath)
        return os.path.join(get_music_dir(), get_birth_year(fpath), fname)

class ImageClassifier:

    def check(self, fpath):
        return check_file_by_ext(fpath, IMAGE_EXT_SET)

    def get_target_path(self, fpath):
        fname = os.path.basename(fpath)
        return os.path.join(get_image_dir(), get_birth_year(fpath), fname)

class VideoClassifier:

    def check(self, fpath):
        return check_file_by_ext(fpath, VIDEO_EXT_SET)

    def get_target_path(self, fpath):
        fname = os.path.basename(fpath)
        return os.path.join(get_video_dir(), get_birth_year(fpath), fname)

class ArchiveClassifier:

    def check(self, fpath):
        return check_file_by_ext(fpath, ARCHIVE_EXT_SET)

    def get_target_path(self, fpath):
        fname = os.path.basename(fpath)
        return os.path.join(get_archive_dir(), get_birth_year(fpath), fname)

CLASSIFIER_LIST = [
    DocumentClassifier(),
    MusicClassifier(),
    ImageClassifier(),
    VideoClassifier(),
    ArchiveClassifier()
]

def get_target_path(fpath):
    for classifier in CLASSIFIER_LIST:
        if classifier.check(fpath):
            return classifier.get_target_path(fpath)


def classify0(dirname = '.', confirmed = False):
    found = False
    count = 0
    for fname in os.listdir(dirname):
        fpath = os.path.join(dirname, fname)

        if is_hidden_file(fname):
            continue

        if not os.path.isfile(fpath):
            continue

        target_path = get_target_path(fpath)
        if target_path is None:
            continue

        if not confirmed:
            count += 1
            found = True
            print(u"[%03d] Move `%s` To `%s`" % (count, fname, target_path))
        else:
            target_dirname = os.path.dirname(target_path)
            makedirs(target_dirname)
            os.rename(fpath, target_path)
    return found

def classify(dirname = '.', confirmed = False):
    found = classify0(dirname, False)
    if not found:
        print("Nothing found to move")
        return
    user_input = input(u"\nConfirmed to move?(y/n):")
    if user_input == "y":
        classify0(dirname, True)


if __name__ == '__main__':
    classify()