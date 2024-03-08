import argparse
import ftplib
import re
import sys

from shipyard_bp_utils import files as shipyard
from shipyard_templates import ShipyardLogger, ExitCodeException, CloudStorage

from shipyard_ftp.exceptions import EXIT_CODE_NO_MATCHES_FOUND
from shipyard_ftp.ftp import FtpClient

logger = ShipyardLogger.get_logger()


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", dest="host", default=None, required=True)
    parser.add_argument("--port", dest="port", default=21, required=True)
    parser.add_argument("--username", dest="username", default=None, required=False)
    parser.add_argument("--password", dest="password", default=None, required=False)
    parser.add_argument(
        "--file-name-match-type",
        dest="file_name_match_type",
        choices={"exact_match", "regex_match"},
        required=False,
        default="exact_match",
    )
    parser.add_argument("--source-file-name", dest="source_file_name", required=True)
    parser.add_argument(
        "--source-folder-name", dest="source_folder_name", default="", required=True
    )
    return parser.parse_args()


def find_files_in_directory(client, folder_filter, files, folders):
    """
    Pull in a list of all entities under a specific directory and categorize them into files and folders.
    """
    original_dir = client.pwd()
    names = client.nlst(folder_filter)
    for name in names:
        # Accounts for an issue where some FTP servers return file names
        # without folder prefixes.
        if "/" not in name:
            name = f"{folder_filter}/{name}"

        try:
            client.cwd(name)
            # If you can change the directory to the entity_name, it's a
            # folder.
            folders.append(name)
        except ftplib.error_perm as e:
            files.append(name)  # If you can't, it's a file.
            continue
        client.cwd(original_dir)

    folders.remove(folder_filter)

    return files, folders


def main():
    try:
        args = get_args()
        host = args.host
        port = args.port
        username = args.username
        password = args.password
        file_name_match_type = args.file_name_match_type
        file_name = args.source_file_name
        folder_name = shipyard.clean_folder_name(args.source_folder_name)

        client = FtpClient(host=host, port=port, user=username, pwd=password)
        client.get_client()  # Initialize the client to be used with find_files_in_directory

        if file_name_match_type == "regex_match":
            folders = [folder_name]
            files = []
            while folders:
                folder_filter = folders[0]

                files, folders = find_files_in_directory(
                    client=client.client, folder_filter=folder_filter, files=files, folders=folders
                )

            matching_file_names = shipyard.find_all_file_matches(
                files, re.compile(file_name)
            )

            number_of_matches = len(matching_file_names)

            if number_of_matches == 0:
                logger.info(f'No matches were found for regex "{file_name}".')
                sys.exit(EXIT_CODE_NO_MATCHES_FOUND)

            for index, file_name in enumerate(matching_file_names):
                logger.info(
                    f"Deleting file {index + 1} of {len(matching_file_names)} out of {number_of_matches}"
                )
                try:
                    client.remove(file_name)
                except Exception:
                    logger.error(f"Failed to delete {file_name}... Skipping")
        elif file_name_match_type == "exact_match":
            file_path = shipyard.combine_folder_and_file_name(folder_name, file_name)
            try:
                client.remove(file_path)
            except Exception as e:
                logger.error(
                    "Most likely, the file name/folder name you specified has typos or the full folder name was not "
                    "provided. Check these and try again."
                )
                raise e
    except ExitCodeException as e:
        logger.error(e.message)
        sys.exit(e.exit_code)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(CloudStorage.EXIT_CODE_UNKNOWN_ERROR)


if __name__ == "__main__":
    main()
