import argparse
import os
import shutil
import time


def sync_folder():
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    source_files = set(os.listdir(source_folder))
    replica_files = set(os.listdir(replica_folder))

    for file in replica_files - source_files:
        os.remove(os.path.join(replica_folder, file))
        log_changes("File removal", os.path.join(replica_folder, file))

    for file in source_files - replica_files:
        shutil.copy2(os.path.join(source_folder, file), replica_folder)
        log_changes("File creation", os.path.join(replica_folder, file))

    for file in source_files:
        current_file = os.path.getmtime(os.path.join(source_folder, file))
        replica_file = os.path.getmtime(os.path.join(replica_folder, file))
        if current_file != replica_file:
            shutil.copy2(os.path.join(source_folder, file), replica_folder)
            log_changes("File copying", os.path.join(replica_folder, file))


def log_changes(operation, current_file_path):
    log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {operation} {current_file_path}"
    print(log_entry)
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='One-way folder synchronization with logging')
    parser.add_argument('-s', '--source_folder', dest='source_folder', required=True, help='Path to the source folder')
    parser.add_argument('-r', '--replica_folder', required=True, help='Path to the replica folder')
    parser.add_argument('-t', '--sync_interval', type=int, required=True, help='Sync interval in seconds')
    parser.add_argument('-l', '--log_file_path', required=True, help='Path to the log file')
    args = parser.parse_args()

    log_file_path = args.log_file_path
    source_folder = args.source_folder
    replica_folder = args.replica_folder

    while True:
        sync_folder()
        time.sleep(args.sync_interval)
