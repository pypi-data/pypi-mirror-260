import datetime
import threading
import os
import re
from functools import cached_property
from watchdog.events import FileSystemEventHandler
import shutil


def dates_since(date: datetime.date) -> list:
    """
    Get all the dates since a date
    :return: A list of all the dates since a date
    """
    dates = []
    start_date = date
    today = datetime.date.today()
    date = start_date
    while date <= today:
        dates.append(date)
        date += datetime.timedelta(days=1)
    return dates


class LocalUploader(FileSystemEventHandler):
    """"""
    def __init__(self,
                 origin_directory: str = r'C:/Users/mangg/AppData/Local/PokerTracker 4/Processed/Winamax',
                 history_directory: str = r'C:/Users/mangg/AppData/Roaming\winamax\documents\accounts\manggy94\history',
                 destination_directory: str = "C:/Users/mangg/ManggyTracker"
                 ):
        self.origin_directory = origin_directory
        self.history_directory = history_directory
        self.pattern = r"(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_(?P<tournament_name>.+)\((?P<tournament_id>\d+)\)_real_holdem_no-limit(?:_summary)?(?:_1)?\.txt"
        self.destination_directory = destination_directory

    def get_local_files(self) -> list:
        """
        Get all the files in the directory
        :return: A list of all the files in the directory
        """
        files = []
        for dirpath, _, filenames in os.walk(self.origin_directory):
            for file in filenames:
                if re.match(self.pattern, file):
                    files.append(os.path.join(dirpath, file))
        return files

    def extract_file_info(self, file_name: str) -> dict or None:
        """
        Extract information from the file name
        :param file_name: The name of the file
        :return: A dict with the information extracted from the file name( year, month, day, tournament_name,
        tournament_id, file_type)
        """
        match = re.match(self.pattern, file_name)

        if not match:
            return None

        if "_summary.txt" in file_name:
            file_type = "summary"
        else:
            file_type = "history"

        return {
            "year": int(match.group("year")),
            "month": int(match.group("month")),
            "day": int(match.group("day")),
            "tournament_name": match.group("tournament_name"),
            "tournament_id": match.group("tournament_id"),
            "file_type": file_type,
            "date": datetime.date(int(match.group("year")), int(match.group("month")), int(match.group("day")))
        }

    def get_files_info(self) -> list:
        """
        Get all the files info in the directory
        :return: A list of all the files info in the directory
        """
        files_info = []
        for dirpath, _, filenames in os.walk(self.origin_directory):
            for file in filenames:
                file_info = self.extract_file_info(file)
                if file_info:
                    files_info.append(file_info)
        return files_info

    @staticmethod
    def create_path(file_info: dict) -> str:
        """
        Create the path in for the object in the bucket
        :param file_info: The file info
        :return: The path of the object in the bucket
        """
        if file_info["file_type"] == "summary":
            path = f"data/summaries/{file_info['year']:04}/{file_info['month']:02}/{file_info['day']:02}/" \
                   f"{file_info['tournament_id']}_{file_info['tournament_name']}_summary.txt"
        else:
            path = f"data/histories/raw/{file_info['year']:04}/{file_info['month']:02}/{file_info['day']:02}/" \
                   f"{file_info['tournament_id']}_{file_info['tournament_name']}_history.txt"
        return path

    def set_file_dict(self, file_path: str) -> dict:
        """
        Set the file dict
        :param file_path: The path of the file
        :return: A dict with file_info, new_path and local_path
        """
        file_name = os.path.basename(file_path)
        file_info = self.extract_file_info(file_name)
        path = self.create_path(file_info)
        return {
            "file_info": file_info,
            "new_path": path,
            "local_path": file_path
        }

    @cached_property
    def organized_files(self) -> list:
        """
        Organize the files in the directory
        :return: A list of dict with the file info, the new path and the local path for each file
        """
        files_info = self.get_files_info()
        paths = [os.path.join(self.destination_directory, self.create_path(file_info)) for file_info in files_info]
        files = self.get_local_files()
        organized_files = [
            {
                "file_info": f_info,
                "new_path": p,
                "local_path": f}
            for f_info, p, f in zip(files_info, paths, files)
        ]
        return organized_files

    def organize_by_year(self, year: int):
        """
        Organize the files in the directory
        :param year: The year to filter
        :return: The same list as organized_files function, filtered by year
        """
        return [file for file in self.organized_files if file["file_info"]["year"] == year]

    def organize_by_month_of_year(self, month: int, year: int):
        """
        Organize the files in the directory
        :param month: The month to filter
        :param year: The year to filter
        :return: The same list as organized_files function, filtered by month and year
        """
        return [file for file in self.organize_by_year(year) if int(file["file_info"]["month"]) == int(str(month))]

    def organize_by_date(self, date: datetime.date):
        """
        Organize the files in the directory
        :param date: The date to filter
        :return: The same list as organized_files function, filtered by date
        """
        return [file for file in self.organized_files if file["file_info"]["date"] == date]

    @staticmethod
    def copy_file(file: dict):
        """
        Copy a file to the local directory with information from organized_files dict format
        :param file: The dict of the file to copy
        """
        source_path = file["local_path"]
        new_path = file["new_path"]
        if not os.path.isfile(source_path):
            print(f"Le fichier source {source_path} n'existe pas.")

        if not os.path.exists(new_path):
            os.makedirs(new_path)
        shutil.copy(source_path, new_path)

    @staticmethod
    def check_file_exists(file: dict):
        """
        Check if a file exists in the bucket
        :param file: The dict of the file to check
        :return: True if the file exists, False otherwise
        """
        return os.path.exists(file["new_path"])

    def copy_files(self, force_copy: bool = False):
        """
        Upload files to the bucket
        :param force_copy: If True, copy all the files, even if they already exist in the bucket
        """
        threads = []
        for file in self.organized_files:
            if force_copy or not self.check_file_exists(file):
                thread = threading.Thread(target=self.copy_file, args=(file,))
                thread.start()
                threads.append(thread)
        for thread in threads:
            thread.join()

    def copy_today_files(self, force_copy: bool = True):
        """
        Upload files of the day to the bucket
        :param force_copy: If True, copy all the files, even if they already exist in the bucket
        """
        threads = []
        for file in self.organize_by_date(datetime.date.today()):
            if force_copy or not self.check_file_exists(file):
                thread = threading.Thread(target=self.copy_file, args=(file,))
                thread.start()
                threads.append(thread)
        for thread in threads:
            thread.join()

    def copy_files_since(self, date: datetime.date, force_copy: bool = True):
        """
        Upload files since a date
        :param date: The date since which the files will be copyed
        :param force_copy: If True, copy all the files, even if they already exist in the bucket
        :return:
        """
        for date in dates_since(date):
            for file in self.organize_by_date(date):
                if force_copy or not self.check_file_exists(file):
                    self.copy_file(file)

    def on_created(self, event):
        """
        Upload a file when it is created
        :param event: The event of the file creation
        """
        file = event.src_path
        print(f"New hand history file observed at {event.src_path}")
        file_dict = self.set_file_dict(file)
        if file_dict:
            self.copy_file(file_dict)

    def on_modified(self, event):
        """
        Upload a file when it is modified
        :param event: The event of the file modification
        """
        file = event.src_path
        print(f"Hand history file modified at {event.src_path}")
        file_dict = self.set_file_dict(file)
        if file_dict:
            self.copy_file(file_dict)
