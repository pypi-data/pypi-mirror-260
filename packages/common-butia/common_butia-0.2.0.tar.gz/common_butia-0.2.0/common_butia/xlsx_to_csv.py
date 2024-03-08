import argparse
import errno
import re
import time
import pandas as pd
import os
from pandas.api.types import is_datetime64_any_dtype


class DataHandler:
    def __init__(self, directory: str) -> None:
        self.directory: str = directory

    def _check_directory(self) -> bool:
        return os.path.isdir(self.directory)

    def _try_finding_date(self, xlsx):
        if self._has_date_second_row(xlsx):
            xlsx.drop(xlsx.index[0], inplace=True)
            xlsx.rename(columns={xlsx.columns[0]: "Data"}, inplace=True)
            return xlsx
        else:
            raise ValueError("Date not found")

    def _has_date_second_row(self, xlsx):
        has_data = [bool(re.search(r"dat[ea]", str(row), flags=re.IGNORECASE)) for row in xlsx.iloc[:2, 0]]
        return any(has_data)

    def _check_xlsx(self, xlsx: pd.DataFrame, file_name: str) -> pd.DataFrame:
        # has two columns ?
        # head has date and indicator
        # date is datetime
        # indicator is float ?

        # check if date exists
        has_data: list[bool] = [bool(re.search(r"dat[ea]", col, flags=re.IGNORECASE)) for col in xlsx.columns]
        if not any(has_data):
            try:
                xlsx = self._try_finding_date(xlsx)
            except ValueError as e:
                print(e)

        # check if date is datetime
        date = xlsx.filter(regex="[Dd][aA][tT][aAeE]", axis=1)
        if not is_datetime64_any_dtype(date):
            try:
                xlsx.loc[:, date.columns[0]] = pd.to_datetime(xlsx.loc[:, date.columns[0]])
            except TypeError:
                raise TypeError("Couldn't convert date to datetime")
            except Exception as e:
                print(e)

        if len(xlsx.columns) == 2:
            # set column name to file name
            if file_name not in xlsx.columns:
                print(f"Renaming {xlsx.columns[1]} to {file_name}")
                xlsx.rename(columns={xlsx.columns[1]: file_name}, inplace=True)
        return xlsx

    def _to_csv(self, file: str) -> None:
        try:
            xlsx = pd.read_excel(file)
            file_name = file.split(".")[0]
            xlsx = self._check_xlsx(xlsx, file_name)
            xlsx.to_csv(f"{file_name}.csv", index=False)

        except ValueError as e:
            # not .xlsx
            print(e)
            pass

    def convert_files(self) -> None:
        if self._check_directory():
            os.chdir(self.directory)
            for file in os.listdir():
                if os.path.isdir(file):
                    continue
                self._to_csv(file)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.directory)


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description="Convert xlsx to csv")
    parser.add_argument("-d", "--directory", type=str, help="directory containing xlsx files")
    args = parser.parse_args()

    data = DataHandler(args.directory)
    data.convert_files()
    print()
    print(f"Done! Files in {args.directory}")
    print(f"--- Ran in {(time.time() - start_time)} seconds ---")
    print()
