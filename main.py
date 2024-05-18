import argparse
import os
import shutil
import time


def sync_folder(source_folder, replica_folder):
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    source_items = set(os.listdir(source_folder))
    replica_items = set(os.listdir(replica_folder))

    for item in replica_items - source_items:
        item_path = os.path.join(replica_folder, item)
        if os.path.isdir(item_path):
            for root, dirs, files in os.walk(item_path, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    os.remove(file_path)
                    log_changes("File removed", file_path)
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    os.rmdir(dir_path)
                    log_changes("Directory removed", dir_path)
            os.rmdir(item_path)
            log_changes("Directory removed", item_path)
        else:
            os.remove(item_path)
            log_changes("File removed", item_path)

    for item in source_items:
        source_item_path = os.path.join(source_folder, item)
        replica_item_path = os.path.join(replica_folder, item)

        if os.path.isdir(source_item_path):
            if not os.path.exists(replica_item_path):
                os.makedirs(replica_item_path)
                log_changes("Directory created", replica_item_path)
            sync_folder(source_item_path, replica_item_path)
        else:
            if not os.path.exists(replica_item_path):
                shutil.copy2(source_item_path, replica_item_path)
                log_changes("File created", replica_item_path)
            else:
                current_file = os.path.getmtime(source_item_path)
                replica_file = os.path.getmtime(replica_item_path)
                if current_file != replica_file:
                    shutil.copy2(source_item_path, replica_item_path)
                    log_changes("File updated", replica_item_path)


def log_changes(operation, current_file_path):
    log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {operation} - {current_file_path}"
    print(log_entry)
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='One-way folder synchronization with logging')
    parser.add_argument('-s', '--source_folder', required=True, help='Path to the source folder')
    parser.add_argument('-r', '--replica_folder', required=True, help='Path to the replica folder')
    parser.add_argument('-t', '--sync_interval', type=int, required=True, help='Sync interval in seconds')
    parser.add_argument('-l', '--log_file_path', required=True, help='Path to the log file')
    args = parser.parse_args()

    log_file_path = args.log_file_path

    while True:
        sync_folder(args.source_folder, args.replica_folder)
        time.sleep(args.sync_interval)
