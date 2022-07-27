from datetime import datetime
import typer
from ftplib import FTP
import pandas as pd
import json

CRED_PATH = ".env/ftp-creds.json"

with open(CRED_PATH, "r") as fp:
    creds = json.load(fp)
energinet = creds["energinet"]


def main(inp: str):
    ftp = FTP(host=energinet["HOSTNAME"])
    ftp.login(user=energinet["USERNAME"], passwd=energinet["PASSWORD"])
    store = []
    files = ftp.mlsd(energinet["PATH"])
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


# get last most recent modified file timestamp from ftp using ftplib
def get_last_modified(ftp, path):
    ftp.cwd(path)
    files = tuple(ftp.mlsd())
    # ftp.cwd("..")
    return files[-1][1]["modify"]





def test():
    with open(CRED_PATH, "r") as fp:
        creds = json.load(fp)
    spectron = creds["spectron"]
    with FTP(host=spectron["HOSTNAME"]) as ftp:
        ftp.login(user=spectron["USERNAME"], passwd=spectron["PASSWORD"])

        print(get_last_modified(ftp, spectron["PATH"]))


if __name__ == "__main__":
    typer.run(test)
