import hashlib
import json
import sys
import os

class DirState(object):

    def __init__(self, path):
        self.path = path

        self.file_hashes = dict()
        self.files = set()

        self.dir_hashes = dict()



        for root, dirs, files in os.walk(path):
            self.files.update(files)

            folder_rel_path = root[len(self.path):]
            dir_hash = hashlib.md5()


            # folder_tokens = folder_rel_path.split('/')
            # parent_dirs = ['']

            for filename in files:
                file_path = os.path.join(root, filename)
                file_rel_path = file_path[len(self.path):]
                with open(file_path) as file:
                    file_content = file.read()
                self.file_hashes[file_rel_path] = hashlib.md5(file_content).hexdigest()
                dir_hash.update(file_content)

            self.dir_hashes[folder_rel_path] = dir_hash.hexdigest()

    def json(self, indent=4):
        output = dict(files=self.file_hashes, dirs=self.dir_hashes)
        return json.dumps(output, indent=indent)

    def __str__(self):
        return "<Dir: '{}' - {} files>".format(self.path, len(self.file_hashes))


if __name__ == '__main__':
    src_dir = sys.argv[1]
    print DirState(src_dir).json()