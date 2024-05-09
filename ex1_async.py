import asyncio
import aiofiles
from aiopath import AsyncPath
from argparse import ArgumentParser
import logging
import random
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    parser = ArgumentParser(description="Asynchronously sort files by extension.")
    parser.add_argument("--source", type=str, required=True, help="Source directory to read files from.")
    parser.add_argument("--dest", type=str, required=True, help="Destination directory to sort files into.")
    return parser.parse_args()


async def copy_file(source_path: AsyncPath, dest_path: AsyncPath):
    await dest_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(str(source_path), 'rb') as src, aiofiles.open(str(dest_path), 'wb') as dst:
        await dst.write(await src.read())
    logger.info(f"Copied {source_path} to {dest_path}")


async def read_folder(source: AsyncPath, dest: AsyncPath):
    async for path in source.glob('**/*'):
        if await path.is_file():
            extension = path.suffix[1:]
            dest_folder = dest / extension
            dest_path = dest_folder / path.name
            await copy_file(path, dest_path)


def create_test_directory(base_path: str, num_files=10000):
    os.makedirs(base_path, exist_ok=True)
    extensions = ['txt', 'jpg', 'png', 'pdf', 'docx']
    for _ in range(num_files):
        ext = random.choice(extensions)
        file_name = f"test_file_{random.randint(1, 100000)}.{ext}"
        file_path = os.path.join(base_path, file_name)
        with open(file_path, 'w') as file:
            file.write(f"Sample data for {file_name}")
        logger.info(f"Created test file {file_path}")


async def main():
    args = parse_args()
    # create_test_directory(args.source)
    source_path = AsyncPath(args.source)
    dest_path = AsyncPath(args.dest)
    await read_folder(source_path, dest_path)

if __name__ == "__main__":
    asyncio.run(main())
