import os
from argparse import ArgumentParser
import logging
import random
import shutil


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    parser = ArgumentParser(description="Synchronously sort files by extension.")
    parser.add_argument("--source", type=str, required=True, help="Source directory to read files from.")
    parser.add_argument("--dest", type=str, required=True, help="Destination directory to sort files into.")
    return parser.parse_args()


def copy_file(source_path, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.move(source_path, dest_path)
    logger.info(f"Copied {source_path} to {dest_path}")


def read_folder(source, dest):
    for root, dirs, files in os.walk(source):
        for file in files:
            source_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1][1:]
            dest_folder = os.path.join(dest, extension)
            dest_path = os.path.join(dest_folder, file)
            copy_file(source_path, dest_path)


def create_test_directory(base_path, num_files=10):
    os.makedirs(base_path, exist_ok=True)
    extensions = ['txt', 'jpg', 'png', 'pdf', 'docx']
    for i in range(num_files):
        ext = random.choice(extensions)
        file_name = f"test_file_{random.randint(1, 1000)}.{ext}"
        file_path = os.path.join(base_path, file_name)
        with open(file_path, 'w') as file:
            file.write("Sample data for {file_name}")
        logger.info(f"Created test file {file_path}")


def main():
    args = parse_args()
    # create_test_directory(args.source)
    read_folder(args.source, args.dest)

if __name__ == "__main__":
    main()
