#!/usr/bin/env python

import urllib2
import re
from HTMLParser import HTMLParser
import sys

class GotovimDomaRecipesExtractor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recipe_links = set()
        self.recipe_link_regexp = re.compile("r=[0-9]+-recept-")
        self.inside_content = False
        self.div_tags_balance_inside_content = 0

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for attr in attrs:
                if attr[0] == "id" and attr[1] == "content":
                    self.inside_content = True

            if self.inside_content:
                self.div_tags_balance_inside_content += 1

        elif tag == "a" and self.inside_content:
            for attr in attrs:
                if attr[0] == "href" and self.recipe_link_regexp.search(attr[1]):
                    self.recipe_links.add(HOSTNAME + attr[1])

    def handle_endtag(self, tag):
        if tag == "div":
            if self.inside_content:
                self.div_tags_balance_inside_content -= 1
        if self.inside_content and self.div_tags_balance_inside_content == 0:
            self.inside_content = False

    def get_recipe_links(self):
        return self.recipe_links


HOSTNAME = "http://gotovim-doma.ru"
GROUP_PAGE_TEMPLATE = "http://gotovim-doma.ru/view.php?g={0}"

GROUP_LIST = [1, 2, 3, 4, 5, 6, 7, 42]

def main(dst_filename):
    dst_file = open(dst_filename, 'w')
    extractor = GotovimDomaRecipesExtractor()
    for group_index in GROUP_LIST:
        page = GROUP_PAGE_TEMPLATE.format(group_index)
        page_html = urllib2.urlopen(page).read().decode("windows-1251")
        extractor.feed(page_html)
    for link in extractor.get_recipe_links():
        print >>dst_file, link
    dst_file.close()

def process_options():
    import optparse
    opt = optparse.OptionParser("Usage: %prog <dst_file>\n" +
        "Save to file links to recipes from site 'gotovim-doma.ru'")
    opts, args = opt.parse_args()
    if len(args) != 1:
        opt.error("Incorrect number of arguments")
    return opts, args

if __name__ == "__main__":
    opts, args = process_options()
    main(args[0])
