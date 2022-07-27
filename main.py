from datetime import datetime
import typer
from ftplib import FTP
import pandas as pd
import json

with open(".env/ftp-creds.json", "r") as fp:
    creds = json.load(fp)
spectron = creds["spectron"]
ftp = FTP(host=spectron["HOSTNAME"])
ftp.login(user=spectron["USERNAME"], passwd=spectron["PASSWORD"])


def main(inp: str):
    store = []
    files = ftp.mlsd(".")
    for file in files:
        name = "__root__" if file[0] == "/" else file[0]
        ts = file[1]["modify"]
        timestamp = datetime(
            int(ts[:4]),
            int(ts[4:6]),
            int(ts[6:8]),
            int(ts[8:10]),
            int(ts[10:12]),
            int(ts[12:14]),
        )
        store.append((name, timestamp))
    ftp.quit()
    df = pd.DataFrame(store, columns=("filename", "time"))
    df = df.set_index("time")

    print(df.sort_index(axis="columns", ascending=False))


if __name__ == "__main__":
    typer.run(main)
