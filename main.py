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


def main(ftp_name: str):
    store = []

    cred_meta = get_credentials(ftp_name)
    ftp = FTP(host=cred_meta["HOSTNAME"])
    ftp.login(user=cred_meta["USERNAME"], passwd=cred_meta["PASSWORD"])
    files = ftp.mlsd(path=cred_meta["PATH"])
    for file in files:
        name = "__root__" if file[0] == "/" else file[0]
        timestring = file[1]["modify"]  # example 202208062359
        timestamp = to_datetime(timestring)
        store.append((name, timestamp))
    ftp.quit()
    df = pd.DataFrame(store, columns=("filename", "time")).set_index("time")

    print(df.sort_index(axis="index", ascending=False))
    df.to_csv("op.DataFrame.csv")


if __name__ == "__main__":
    typer.run(main)
