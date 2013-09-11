#!/usr/bin/env python

import json
import urllib2
from HTMLParser import HTMLParser
import sys

class GotovimDomaRecipesExtractor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inside_content = False
        self.off = False
        self.find_img = False
        self.data = u""

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'wall_post_text':
                    self.inside_content = True
        elif tag == "br":
            self.data += '\n'
        elif tag == "a" and self.inside_content:
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'wall_post_more':
                    self.off = True
                    self.data = self.data.strip()
                               
    def handle_data(self, data):
        if self.inside_content and not self.off:
            self.data += data
            print >> FILE, self.data.encode("utf-8"),
            self.data = ""
                        
    def handle_endtag(self, tag):
        if tag == "div":
            if self.inside_content:
                self.inside_content = False
                self.data += '\n---\n'
        elif tag == "a" and self.off:
            self.off = False

    def handle_entityref(self, name):
        if name == "quot":
            self.data += '\"'

RECIPES = "http://vk.com/my_recept"
FILE = open("out.txt", "w")
 
if __name__ == "__main__":
    extractor = GotovimDomaRecipesExtractor()
    extractor.feed(open("result2.txt", "r").read().decode("utf-8"))
    #print >>FILE, extractor.self.data