import datetime
from loader import LocalUploader

if __name__ == '__main__':
    uploader = LocalUploader()
    year = datetime.date.today().year
    date = datetime.date(year, 10, 7)
    uploader.copy_files_since(date=date, force_copy=False)
