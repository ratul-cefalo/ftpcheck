# :construction: [WIP] ftpcheck :construction:

Check ftp for preset state.

## :sparkles: Features :sparkles: in oven :building_construction:

1. When was this folder last updated? (--last-modified)
2. Which file was last updated? (--latest-file)
3. When was this file last updated? (--file-status \<filename\>)

## Development environment

1. clone repo
2. run `pipenv install`
3. run `pipenv shell` to activate virtual environment
4. create a credential file in `.env` folder [see below]
5. run `python main.py <ftp name>`

### *Credentials file format*

```json
{
    "example": {
        "HOSTNAME": "ftpserver.example.com",
        "USERNAME": "exuser",
        "PASSWORD": "expass",
        "PATH" : "."
    }
}
```
