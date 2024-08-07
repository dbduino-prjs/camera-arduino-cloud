# Python ultra simple Web server
Web server implemented in Python using Flask that allows you to upload and download files. It works both on HTTP and HTTPS.

## How to use it

### Configure the ports

The server will listen both in HTTP and HTTPS. The listening ports can be modified by changing the following lines of `flask-web-server.py`

```python
PORT_HTTP  = 8080
PORT_HTTPS = 8443
```

### Run the script

To run the script, you can type the following command:

```
python3 flask-web-server.py
```

### Using the server with HTTPS

If you want to use HTTPS and you don't have any certificates, you also have to generate it. You can use the following command

```sh
DOMAIN="Your IP Address or domain name"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem -subj "/CN=${DOMAIN}" -addext "subjectAltName=IP:${DOMAIN}"
```

> Note: This command will work depending on your server. If you are using a public IP address, you should indicate that one. If you are using a domain, you should indicate the domain name.
> Note: As the certificate is self-signed, it's likely that you have to add it to the list of trusted certificates of your OS


## Test de server
File upload

```
curl -X POST -F "file=@/path/to/your/file" http://localhost:8080/upload
```

File download

```
curl -O http://localhost:8080/download/snapshot.jpg
```

