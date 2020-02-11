🔐 Keycloak latest official documentation (ebook)
=================================================

This python code will download Keycloak's latest documentation guides from https://www.keycloak.org/documentation.html,
put all the content in a single file, and convert it to epub, markdown, [and any other format](https://pandoc.org/MANUAL.html#specifying-formats) supported by pandoc.

So you can read the Keycloak docs on your Kindle or other ebook devices.

## How to use this code

### 💻 Run it directly on your computer

```
pip install -r requirements.txt
python get_keycloak_docs.py -v --format epub --output /tmp/keycloak_docs.epub
```

### 🐋 Run it on a Container (recommended option)

```
sudo docker run -i -t --rm -v /tmp/keycloak_docs/:/output dafero/get-keycloak-docs:v1.0
```

> Note: the resulting file will be created in `/tmp/keycloak_docs/keycloak_docs.epub` on your local machine


Enjoy! 🎉
