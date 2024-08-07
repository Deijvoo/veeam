# Folder Synchronization Tool

## Overview
This tool synchronizes two folders: source and replica. It ensures that the replica folder is an exact copy of the source folder, maintaining one-way synchronization.

## Features
- One-way synchronization
- Periodic synchronization
- Logging to file and console
- Command line arguments support
- Optional checksum verification

## Requirements
- Python 3.x

## Installation
Clone the repository:
```sh
git clone git@github.com:Deijvoo/veeam.git
cd veeam
```

## Usage
Run the synchronization tool with the following command:

```sh
python sync_tool.py --source <source_folder_path> --replica <replica_folder_path> --interval <sync_interval_in_seconds> --log <log_file_path> [--checksum]
```

## Arguments
**--source**: Path to the source folder.
**--replica**: Path to the replica folder.
**--interval**: Synchronization interval in seconds.
**--log**: Path to the log file.
**--checksum**: Optional. Use checksums to verify file content.

## Example
```sh
python sync_tool.py --source /path/to/source --replica /path/to/replica --interval 60 --log /path/to/logfile.log --checksum
```

## Run tests
```sh
python -m unittest tests/test_veeam.py
```

## Author
Dávid Husár
