import argparse
import logging
import os
import shutil
import time

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def setup_logging(log_file_path):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt=TIME_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def log_changes(operation, current_file_path, level=logging.INFO):
    logger.log(level, f'{operation} - {current_file_path}')


def sync_folder(source_folder, replica_folder):
    try:
        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)
            log_changes("Directory created", replica_folder)

        source_items = set(os.listdir(source_folder))
        replica_items = set(os.listdir(replica_folder))

        for item in replica_items - source_items:
            item_path = os.path.join(replica_folder, item)
            if os.path.isdir(item_path):
                try:
                    for root, dirs, files in os.walk(item_path, topdown=False):
                        for name in files:
                            file_path = os.path.join(root, name)
                            try:
                                os.remove(file_path)
                                log_changes("File removed", file_path)
                            except OSError as e:
                                log_changes(f"Error {e} trying to remove", {file_path}, level=logging.ERROR)
                        for name in dirs:
                            dir_path = os.path.join(root, name)
                            try:
                                os.rmdir(dir_path)
                                log_changes("Directory removed", dir_path)
                            except OSError as e:
                                log_changes(f"Error {e} trying to remove", {dir_path}, level=logging.ERROR)
                    os.rmdir(item_path)
                    log_changes("Directory removed", item_path)
                except Exception as e:
                    log_changes(f"Error {e} trying to remove", {item_path}, level=logging.ERROR)
            else:
                try:
                    os.remove(item_path)
                    log_changes("File removed", item_path)
                except OSError as e:
                    log_changes(f"Error {e} trying to remove", {item_path}, level=logging.ERROR)

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
                    try:
                        shutil.copy2(source_item_path, replica_item_path)
                        log_changes("File created", replica_item_path)
                    except Exception as e:
                        log_changes(f"Error {e} trying to copy {source_item_path}",
                                    {replica_item_path}, level=logging.ERROR)
                else:
                    current_file = os.path.getmtime(source_item_path)
                    replica_file = os.path.getmtime(replica_item_path)
                    if current_file != replica_file:
                        try:
                            shutil.copy2(source_item_path, replica_item_path)
                            log_changes("File updated", replica_item_path)
                        except Exception as e:
                            log_changes(f"Error {e} trying to update", {replica_item_path}, level=logging.ERROR)
    except Exception as e:
        logging.exception(f"Error while syncing: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='One-way folder synchronization with logging')
    parser.add_argument('-s', '--source_folder', required=True, help='Path to the source folder')
    parser.add_argument('-r', '--replica_folder', required=True, help='Path to the replica folder')
    parser.add_argument('-t', '--sync_interval', type=int, required=True, help='Sync interval in seconds')
    parser.add_argument('-l', '--log_file_path', required=True, help='Path to the log file')
    args = parser.parse_args()

    setup_logging(args.log_file_path)
    logger = logging.getLogger()

    try:
        while True:
            sync_folder(args.source_folder, args.replica_folder)
            time.sleep(args.sync_interval)
    except KeyboardInterrupt:
        logger.info("Synchronization interrupted")
        exit(0)
