#!/usr/bin/python

# Daniel Fernandez Rodriguez <gmail.com daferoes>
# https://github.com/danifr/get-keycloak-docs
#
# Download Keycloak latest docs all in one file and convert them to epub markdown
#
#
# Usage: python get_keycloak_docs.py -v --output keycloak_latest.epub
#

import logging
import os
import sys
import urllib.request
import pypandoc

from argparse import ArgumentParser
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from readability.readability import Document


def load_url(url):
    """
    Load content of a remote URL

    :param url URL where the content is located
    """
    with urllib.request.urlopen(url) as response:
       if response.getcode() == 200:
           return response.read().decode('utf-8')
       raise Exception("URL '%s' NOT found" % url)


def get_guide_urls(guides_url):
    """
    Get the URLs of the guides listed in a guides page section

    :param guides_url URL of the guides page, optionally with a #section fragment
    """
    page_url, _, section = guides_url.partition('#')
    soup = BeautifulSoup(load_url(page_url), 'html.parser')
    categories = soup.find_all('div', attrs={'class': 'guide-category'})
    if section:
        categories = [c for c in categories if c.get('id') == section]
    hrefs = [a['href'] for c in categories for a in c.find_all('a', attrs={'class': 'stretched-link'})]
    return [h for h in hrefs if urlparse(h).netloc == urlparse(page_url).netloc]


def get_docs_urls(base_url):
    """
    Get the URLs of every chapter of the Keycloak docs

    :param base_url URL where the docs index is located
    """
    soup = BeautifulSoup(load_url(base_url), 'html.parser')
    table = soup.find('table', attrs={'class': 'kc-table-docs'})
    if table is None:
        raise Exception("Docs table not found in %s, the page layout may have changed" % base_url)

    urls = []
    for row in table.find('tbody').find_all('tr'):
        url = row.find_all('td')[0].find('a')['href']
        if "docs-api" in url:
            continue
        if urlparse(url).path.rstrip('/') == '/guides':
            urls.extend(get_guide_urls(url))
        else:
            urls.append(url)
    return list(dict.fromkeys(urls))


def absolutize_urls(html, page_url):
    """
    Make relative image sources and links absolute so pandoc can fetch the images

    :param html HTML of the page
    :param page_url URL the page was downloaded from
    """
    soup = BeautifulSoup(html, 'html.parser')
    for tag, attr in (('img', 'src'), ('a', 'href')):
        for element in soup.find_all(tag, attrs={attr: True}):
            if not element[attr].startswith('#'):
                element[attr] = urljoin(page_url, element[attr])
    return str(soup)


def get_docs_content(base_url):
    """
    Get the content of every chapter of the Keycloak docs

    :param base_url URL where the docs index is located
    """
    docs_content = ""
    for url in get_docs_urls(base_url):
        logging.info("Downloading content from %s..." % url)
        content = absolutize_urls(load_url(url), url)
        readable_title = Document(content).short_title()
        docs_content += '<h2>' + readable_title + '</h2><br/>' + content
        logging.info("Content parsed successfully")
    return docs_content


def main():
    parser = ArgumentParser(description="Download Keycloak latest docs all in one file and convert them to epub markdown")
    parser.add_argument("-u", "--url", default="https://www.keycloak.org/documentation.html", help="Keycloak documentation URL")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    parser.add_argument('-f', '--format', default="epub", help="Check https://pandoc.org/MANUAL.html#specifying-formats for all available formats")
    parser.add_argument('-o', '--output', default="keycloak_docs.epub", help="Output")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    logging.info("Getting content index from %s..." % args.url)
    docs_content = get_docs_content(args.url)
    logging.info("Saving redeable content as: %s" % args.output)
    pypandoc.convert_text(docs_content, args.format, format='html', outputfile=args.output)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)
        sys.exit(-1)
