# folder_sync

This Python script performs one-way folder synchronization, maintaining a full copy of the source folder at the replica folder, whilst logging operations and errors.

## Features

- One-way synchronization from source to replica
- Periodical sync based on a given interval
- Logging file creation, copying, removal operations as well as errors

## Prerequisites

- Python 3.6 or higher

## Usage

1. Clone this repository or download the script files.
2. Install Python if it's not installed already. 
3. Run the script with the required arguments, for example: python3 main.py [arguments]

## Arguments

- '-s', '--source_folder': Path to the source folder.
- '-r', '--replica_folder': Path to the replica folder.
- '-t', '--sync_interval': Synchronization interval in seconds.
- '-l', '--log_file_path': Path to the log file.

## Example

This example will synchronize the source with the replica every 60 seconds and log operations to 'log.txt':

```sh
python3 main.py -s /path/to/source -r /path/to/replica -l /path/to/log.txt -t 60
