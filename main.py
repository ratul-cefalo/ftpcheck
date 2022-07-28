from datetime import datetime
import typer
from ftplib import FTP
import pandas as pd
import json

CRED_PATH = ".env/ftp-creds.json"


def get_credentials(loader_name):
    with open(CRED_PATH, "r") as fp:
        creds = json.load(fp)
    return creds.get(loader_name)


def to_datetime(timestring):
    """
    202208062359 to datetime
    """
    return datetime(
        year=int(timestring[:4]),
        month=int(timestring[4:6]),
        day=int(timestring[6:8]),
        hour=int(timestring[8:10]),
        minute=int(timestring[10:12]),
        second=int(timestring[12:14]),
    )

    store = []
    files = ftp.mlsd(spectron["PATH"])
    for file in files:
        name = "__root__" if file[0] == "/" else file[0]
        timestring = file[1]["modify"]
        timestamp = datetime(
            year = int(timestring[:4]),
            month = int(timestring[4:6]),
            day = int(timestring[6:8]),
            hour = int(timestring[8:10]),
            minute = int(timestring[10:12]),
            second = int(timestring[12:14]),
        )
        store.append((name, timestamp))
    ftp.quit()
    df = pd.DataFrame(store, columns=("filename", "time"))
    df = df.set_index("time")

    print(df.sort_index(axis="columns", ascending=False))


if __name__ == "__main__":
    typer.run(main)
