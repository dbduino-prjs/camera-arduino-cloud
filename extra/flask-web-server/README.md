# Python ultra simple Web server
Web server implemented in Python using Flask that allows you to upload and download files

## How to use it

```
python3 flask-web-server.py
```


## Test de server
File upload

```
curl -X POST -F "file=@/path/to/your/file" http://localhost:8080/upload
```

File download

```
curl -O http://localhost:8080/download/snapshot.jpg
```

