import argparse
import logging
import os
import shutil
import time


def files_are_identical(file1: str, file2: str) -> bool:
    """
    Compare two files to determine if they are identical.

    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.

    Returns:
        bool: True if files are identical, False otherwise.
    """
    return os.path.getsize(file1) == os.path.getsize(file2) and open(file1, 'rb').read() == open(file2, 'rb').read()


def create_directory(replica_dir: str) -> None:
    """
    Create a directory at the specified path.

    Args:
        replica_dir (str): Path to the directory to be created.
    """
    os.makedirs(replica_dir)
    logging.info('Created directory: %s', replica_dir)


def create_file(source_file: str, replica_file: str) -> None:
    """
    Create a file at the specified path by copying from the source file.

    Args:
        source_file (str): Path to the source file.
        replica_file (str): Path to the replica file to be created.
    """
    os.makedirs(os.path.dirname(replica_file), exist_ok=True)
    shutil.copy2(source_file, replica_file)
    logging.info('Created file: %s', replica_file)


def copy_file(source_file: str, replica_file: str) -> None:
    """
    Copy the source file to the replica file path.

    Args:
        source_file (str): Path to the source file.
        replica_file (str): Path to the replica file.
    """
    shutil.copy2(source_file, replica_file)
    logging.info('Copied file: %s', replica_file)


def delete_file(replica_file: str) -> None:
    """
    Delete the specified file.

    Args:
        replica_file (str): Path to the file to be deleted.
    """
    os.remove(replica_file)
    logging.info('Deleted file: %s', replica_file)


def delete_directory(replica_dir: str) -> None:
    """
    Delete the specified directory and all its contents.

    Args:
        replica_dir (str): Path to the directory to be deleted.
    """
    shutil.rmtree(replica_dir)
    logging.info('Deleted directory: %s', replica_dir)


def traverse_source_files(source_files: Set[str], source: str, replica: str) -> None:
    """
    Traverse the source directory and handle file/directory creation and copying.

    Args:
        source_files (Set[str]): Set to store paths of files in the source directory.
        source (str): Path to the source directory.
        replica (str): Path to the replica directory.
    """
    for root, dirs, files in os.walk(source):
        entries = dirs + files
        for entry in entries:
            source_file_path = os.path.join(root, entry)
            replica_file_path = os.path.join(replica, os.path.relpath(source_file_path, source))
            source_files.add(source_file_path)

            if not os.path.exists(replica_file_path):
                if os.path.isfile(source_file_path):
                    create_file(source_file_path, replica_file_path)
                else:
                    create_directory(replica_file_path)
            elif os.path.isfile(replica_file_path) and not files_are_identical(source_file_path, replica_file_path):
                copy_file(source_file_path, replica_file_path)


def traverse_replica_files(replica_files: set[str], source_files: set[str], source: str, replica: str) -> None:
    """
    Traverse the replica directory and handle file/directory deletion.

    Args:
        replica_files (Set[str]): Set to store paths of files in the replica directory.
        source_files (Set[str]): Set to store paths of files in the source directory.
        source (str): Path to the source directory.
        replica (str): Path to the replica directory.
    """
    for root, dirs, files in os.walk(replica):
        entries = dirs + files
        for entry in entries:
            replica_file_path = os.path.join(root, entry)
            replica_files.add(replica_file_path)
            if os.path.relpath(replica_file_path, replica) not in [os.path.relpath(f, source) for f in source_files]:
                if os.path.isfile(replica_file_path):
                    delete_file(replica_file_path)
                else:
                    delete_directory(replica_file_path)


def sync_folders(source: str, replica: str) -> None:
    """
    Synchronize the contents of the source directory with the replica directory.

    Args:
        source (str): Path to the source directory.
        replica (str): Path to the replica directory.
    """
    if not os.path.exists(source):
        logging.error("Source directory does not exist: %s", source)
    if not os.path.exists(replica):
        logging.error("Replica directory does not exist: %s", replica)
    if not os.path.exists(source) or not os.path.exists(replica):
        return

    source_files = set()
    replica_files = set()

    traverse_source_files(source_files, source, replica)
    traverse_replica_files(replica_files, source_files, source, replica)


def main() -> None:
    """
    Main function to parse command-line arguments and start the synchronization process.
    """
    parser = argparse.ArgumentParser(description='Sync folders')
    parser.add_argument('--source', type=str, help='Source folder')
    parser.add_argument('--replica', type=str, help='Replica folder')
    parser.add_argument('--log', type=str, help='Log file')
    parser.add_argument('--interval', type=int, help='Interval in seconds', default=15)

    args = parser.parse_args()

    logging.basicConfig(filename=args.log, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logging.getLogger().addHandler(console)

    while True:
        logging.info('Start sync folders')
        sync_folders(args.source, args.replica)
        logging.info('End sync folders')
        time.sleep(args.interval)


if __name__ == '__main__':
    main()
