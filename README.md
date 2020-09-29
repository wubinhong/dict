# Dict

dict for IELTS preparation

## Dev mode

### Backend

> Note: All commands runned at this project root directory

- Launch backend

```bash
python3 backend/app.py
```

- Run specified unittest method

```bash
python3 -m unittest -v test.test_word_import.TestWordImport.test_regex
```

- Export / import mongodb collection

```bash
# Export collection Word
mongoexport --uri=mongodb://root:123456@127.0.0.1:27017/dict -c Word -o Word.json
# Import Collection Word, Note: system import by _id by default and will skip docuemnt when encounting duplicate key, and new record will be import
mongoimport --uri=mongodb://root:123456@127.0.0.1:27017/dict -c Word Word.json
```

- Dump / restore mongodb database

```bash
# Dump to local file system as a directory. Both of the following two command are Okay.
# Note: Acoording to mongo docs, user with options "--authenticationDatabase=admin" has the highest privileges to access all database.
# In the other word, user who barely authenticated by specified db only have privilege to access to authenticated db.
# According above, user root merely authenticated by db dict can only dump and restore db dict.
# Unlike mongoexport, mongodump will generate a separate dir for each db and both bson and json files for each collection in the meantime.
mongodump --uri=mongodb://root:123456@127.0.0.1:27017/dict -o 20191209_0922
mongodump -h 127.0.0.1 -u root -p 123456 --authenticationDatabase=dict -d dict -o 20191209_0922

$ tree 20191209_0922
20191209_0922
└── dict
    ├── Admin.bson
    ├── Admin.metadata.json
    ├── Word.bson
    └── Word.metadata.json

# Restore from dumped directory.
# Note: mongorestore will scan sub dirs in dir 20191209_0922 and restore to corresponding db, so user should have the privileges to all restored dbs.
mongorestore -h 127.0.0.1 -u root -p 123456 --authenticationDatabase=dict 20191209_0922
# Only restore specified db and collection
mongorestore -h 127.0.0.1 -u root -p 123456 --authenticationDatabase=dict -d dict -c Word 20191209_0922/dict/Word.bson
```

## Product mode with docker

- Build docker image dict:v1 with Dockerfile and take current directory build context directory.

> Note: This process will be expected to be done at the host server.

```bash
docker build --target base -t dict:base -f Dockerfile .
(cd backend && find . -type d -name __pycache__ -exec rm -r {} + && find . -type f -name *.pyc -exec rm -r {} +)
(cd frontend && npm install && npm run build)
docker build --target app -t dict:v1 -f Dockerfile .
```

- Build container with image built above.
>
> * We specify the virtual volume for app logger output(`_host_local_directory_:_container_volume_`).
> * Volume definition /data/db and /data/configdb inherited from parent image mongo:bionic
> * Note: We usually do this process at the target server where the app run.
>
```bash
docker run --name dict_server1 -d -p 9000:80 -v /data/container/dict:/data -v /data/container/dict/db:/data/db dict:v1
```

> **Importance: A `build.sh` shell script was written to make building work more convenient.**

```bash
./build <image <base|app [frontend|mobile]>|container>
```

- Checkout container

```bash
docker container ls
```

- Healthy check

```bash
curl -iv http://localhost:8088
```

- Container log info checking

```bash
docker logs dict_server1
```

- Login container with bash: It's convenient to checkout the inner content of the container. It's useful when we debuging the docker images.

```bash
docker exec -it dict_server1 bash
```

## IDE Configuration

### Visual Studio Code

- Add python extention support
  - Found it hard to use default `Python Language Server` when downloading [python extension](https://pvsc.azureedge.net/python-language-server-stable/Python-Language-Server-osx-x64.0.5.51.nupkg)
  - Use `pylance` as alternative: `cmd + shift + x` --> search `pylance`

- Resolve problem `Pylint “unresolved import” error in Visual Studio Code`

  ```shell
  vim ${workspaceFolder}/.vscode/settings.json
  ```

  ```json
  {
      "python.autoComplete.extraPaths": ["./backend"],
  }
  ```

- Add unit test support and disable line characters limitation

  ```shell
  vim ${workspaceFolder}/.vscode/settings.json
  ```

  ```json
  {
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        "./backend",
        "-p",
        "test_*.py"
    ],
    "python.linting.pylintArgs": [
        "--ignore=E501"
    ],
  }
  ```

- Formatter related global setting

```shell
vim ~/Library/Application\ Support/Code/User/settings.json
```

```json
{
  "vetur.format.options.tabSize": 4,
  "python.formatting.autopep8Args": ["--max-line-length=120"]
}
```

## Userful command line

- Delete all __pycache__ directory

```bash
find . -type d -name __pycache__ -exec rm -r {} +
```

## Reference docs

[vuejs](https://vuejs.org/v2/guide/)
[element-ui](https://element.eleme.cn/#/zh-CN)
