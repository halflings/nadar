import argparse
import hashlib
import json
import os
from collections import defaultdict

class AppSignature(object):
    def __init__(self, path):
        self.path = path
        self.signatures = dict()
        _, top_level_dirs, _ = os.walk(self.path).next()
        for folder in top_level_dirs:
            folder_path = os.path.join(self.path, folder)
            self.signatures[folder] = DirSignature(folder_path)

            # DEBUG
            print folder
            print
            print self.signatures[folder].json()
            print '=' * 80

class DirSignature(object):

    def __init__(self, path, hash_func=hashlib.md5):
        self.path = path
        self.folder_name = os.path.split(self.path)[-1]

        self.hashes = defaultdict(dict)
        self.files = set()

        for root, dirs, files in os.walk(path):
            self.files.update(files)

            for filename in files:
                file_path = os.path.join(root, filename)
                file_rel_path = file_path[len(self.path):]
                with open(file_path) as file:
                    file_content = file.read()
                file_hash = hash_func(file_content).hexdigest()
                self.hashes[file_rel_path][file_hash] = self.folder_name

    def json(self, indent=4):
        output = dict(files=self.hashes)
        return json.dumps(output, indent=indent)

    def __str__(self):
        return "<Dir: '{}' - {} files>".format(self.path, len(self.hashes))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', help="path to the source directory")
    args = parser.parse_args()
    src_dir = args.path

    AppSignature(src_dir)