import os
import sys

from packed import translate_file

def main(args):
    if not args:
        print('Usage: packed_build <target_directory>')
        return 1
    target_directory = args[0]
    for root, dirs, files in os.walk(target_directory):
        for filename in files:
            if filename.endswith('.templix.py'):
                py_filename = filename.replace('.templix.py', '.py')
                full_pkd_path = os.path.join(root, filename)
                full_py_path = os.path.join(root, py_filename)
                translate_file(full_pkd_path, full_py_path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
