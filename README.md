Get Keycloak docs
=================

Get Keycloak latest docs all in one file and convert them to epub, markdown and other formats.

## How to use it:

### Execute it directly on your computer

```
pip3 install -r requirements.txt
python get_keycloak_docs.py -v --format epub --output /tmp/keycloak_docs.epub
```

### On a Container 🐋 (recommended)

```
sudo docker run -i -t --rm -v /tmp/keycloak_docs/:/output dafero/get-keycloak-docs:v1.0
# the epub file will be created in /tmp/keycloak_docs/keycloak_docs.epub
```

Enjoy! 🎉
