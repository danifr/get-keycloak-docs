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


def get_docs_content(base_url):
    """
    Get the content of every chapter of the Keycloak docs

    :param base_url URL where the docs index is located
    """
    html_doc = load_url(base_url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    docs_content = ""

    data = []
    table = soup.find('table', attrs={'class':'table table-bordered table-striped'})
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        url = cols[0].find_all('a')[0]['href']
        if "docs-api" not in url:
            logging.info("Downloading content from %s..." % url)
            content = load_url(url)
            readable_article = content
            readable_title = Document(content).short_title()
            readable_article = '<h2>'+readable_title+'</h2><br/>'+readable_article
            docs_content += readable_article
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
