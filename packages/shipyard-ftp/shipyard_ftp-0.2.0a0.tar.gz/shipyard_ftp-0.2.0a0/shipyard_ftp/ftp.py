import ftplib

from shipyard_templates import CloudStorage, ShipyardLogger

from shipyard_ftp import exceptions

logger = ShipyardLogger().get_logger()


class FtpClient(CloudStorage):
    def __init__(self, host: str, user: str, pwd: str, port: int = None) -> None:
        self.client = None
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port or 21

    def connect(self):
        try:
            self.client = self.get_client()
        except Exception:
            return 1
        else:
            return 0

    def move(self, source_full_path, destination_full_path):
        """
        Move a single file from one directory of the ftp server to another
        """
        if not self.client:
            self.get_client()
        current_dir = self.client.pwd()
        source_path = os.path.normpath(os.path.join(current_dir, source_full_path))
        dest_path = os.path.normpath(os.path.join(current_dir, destination_full_path))
        try:
            self.client.rename(source_path, dest_path)
        except Exception as e:
            raise exceptions.MoveError(
                f"Failed to move {source_path}. Ensure that the source/destination file name and folder name are "
                f"correct. Error message from server: {e} ",
            ) from e

        logger.info(f"{source_path} successfully moved to " f"{dest_path}")

    def remove(self, file_path):
        if not self.client:
            self.get_client()
        try:
            self.client.delete(file_path)
            logger.info(f"Successfully deleted {file_path}")
        except Exception as e:
            raise exceptions.DeleteError(
                f"Failed to delete file {file_path}. Ensure that the folder path and file name our correct"
                f"Message from server: {e}"
            )

    def upload(self, source_full_path, destination_full_path):
        if not self.client:
            self.get_client()
        try:
            with open(source_full_path, "rb") as f:
                self.client.storbinary(f"STOR {destination_full_path}", f)
        except Exception as e:
            raise exceptions.UploadError(f"Failed to upload {source_full_path} to FTP server") from e

        logger.info(f"{source_full_path} successfully uploaded to " f"{destination_full_path}")

    def get_client(self):
        """
        Attempts to create an FTP client at the specified host with the
        specified credentials
        """
        logger.info(f"Connecting to FTP server at {self.host}:{self.port} with user {self.user}...")
        try:
            self.client = ftplib.FTP(timeout=300)
            self.client.connect(self.host, int(self.port))
            self.client.login(self.user, self.pwd)
            self.client.set_pasv(True)
            self.client.set_debuglevel(0)
            logger.info(f"Connected to FTP server at {self.host}:{self.port} successfully.")
            return  self.client
        except Exception as e:
            raise exceptions.InvalidCredentials(
                f"Error accessing the FTP server with the specified credentials\n"
                f"The server says: {e}")from e

    def download(self, file_name, destination_full_path=None):
        """
        Download a selected file from the FTP server to local storage in
        the current working directory or specified path.
        """
        if not self.client:
            self.get_client()
        os.mkdir(os.path.dirname(destination_full_path), exist_ok=True)
        try:
            logger.info(f"Attempting to download {file_name}...")
            with open(destination_full_path, "wb") as f:
                self.client.retrbinary(f"RETR {file_name}", f.write)
            logger.info(f"{file_name} successfully downloaded to {destination_full_path}")
        except Exception as e:
            os.remove(destination_full_path)
            raise exceptions.DownloadError(f"Failed to download {file_name}. Message from server: {e}") from e

        logger.info(f"{file_name} successfully downloaded to {destination_full_path}")


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())
    credentials = {"host": os.getenv("FTP_HOST"), "port": os.getenv("FTP_PORT"), "user": os.getenv("FTP_USERNAME"),
                   "pwd": os.getenv("FTP_PASSWORD"), }

    ftp = FtpClient(credentials["host"], credentials["user"], credentials["pwd"], credentials["port"])

    print(ftp.connect())
