#!/usr/bin/env python

import urllib2
import httplib
import urlparse
import time
import os, sys

def safe_urlread(url, timeout=60):
    try:
        result = urllib2.urlopen(url, timeout=int(timeout))
    except (IOError, httplib.BadStatusLine, urllib2.URLError) as err:
        print >>sys.stderr, 'error for', url, type(err).__name__, str(err)
        return None
    return result.read()

GOTOVIM_DOMA = "gotovim-doma.ru"

def choose_save_name(url):
    parsed_url = urlparse.urlparse(url)
    reqparams = urlparse.parse_qs(parsed_url.query)
    if parsed_url.hostname == GOTOVIM_DOMA:
        return "{0}_{1}".format(parsed_url.hostname[:parsed_url.hostname.index('.')], reqparams['r'][0])

    return None

def save_page(html, url, save_dir):
    save_name = choose_save_name(url)
    if save_name:
        save_path = os.path.join(save_dir, save_name)
        with open(save_path, 'w') as save_file:
            print >>save_file, html
    else:
        print >>sys.stderr, "Unable to choose savename for url {0}".format(url)
    pass

DOWNLOAD_TIMEOUT = 2

def main(links_filename, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    links_file = open(links_filename)
    for line in links_file:
        url = line.rstrip()
        print "Downloading", url
        html = safe_urlread(url)
        html = html.replace("\r", "")
        if html:
            save_page(html, url, dst_dir)
            print "Stored"
        time.sleep(DOWNLOAD_TIMEOUT)

    links_file.close()

def process_options():
    import optparse
    opt = optparse.OptionParser("Usage: %prog <links_file> <dst_dir>\n" +
        "Downloads pages from list given in file, saves in specified directory.\n" +
        "Page is saved with name based on url.")
    opts, args = opt.parse_args()
    if len(args) != 2:
        opt.error("Incorrect number of arguments")
    return opts, args

if __name__ == '__main__':
    opts, args = process_options()
    main(args[0], args[1])
