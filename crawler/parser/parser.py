#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from HTMLParser import HTMLParser
import sys
import os
import json
import re

class GotovimDomaRecipesExtractor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inside_content = False
        self.off = False
        self.find_img = False
        self.data = u""
        self.image_index = 0

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'wall_post_text':
                    self.inside_content = True
                elif attr[0] == 'class' and attr[1] == 'page_post_queue_wide':
                    self.find_img = True
        elif tag == "img" and self.find_img:
            for attr in attrs:
                if attr[0] == 'src':
                    self.data += attr[1] + OUTSIDE_SEPARATOR
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
                        
    def handle_endtag(self, tag):
        if tag == "div":
            if self.inside_content:
                self.inside_content = False
                self.data += INSIDE_SEPARATOR
        elif tag == "a" and self.off:
            self.off = False
        elif tag == "img":
            self.find_img = False

    def handle_entityref(self, name):
        if name == "quot":
            self.data += '\"'
    
    def clean_recipes(self):
        self.data = re.sub("\n *\n* *\n*", "\n", self.data)
        self.data = re.sub(" *\n-? ?", "\n", self.data)
        self.data = re.sub("[0-9]\. ", "", self.data)
        self.data = self.data.replace("\nИнгредиенты:\n".decode("utf-8"), INSIDE_SEPARATOR)
        self.data = self.data.replace("\nПриготовление:\n".decode("utf-8"), INSIDE_SEPARATOR)

        temp_data = self.data.split(OUTSIDE_SEPARATOR)
        self.data = ""
        for recipe_index in temp_data:
            list = recipe_index.split(INSIDE_SEPARATOR)
            if len(list) == 4:
                list[0] = list[0].split("\n")[0]
                list[2] = re.sub("\n", " ", list[2])
                list[3] = self.download_image(list[3])
                self.data += (OUTSIDE_SEPARATOR + INSIDE_SEPARATOR.join(list))
        self.data = self.data[3:]
        # prints the data in a readable form
        #print >>FILE, self.data.encode("utf-8")
        
    def get_recipe_json(self):
        for recipe_index in self.data.split(OUTSIDE_SEPARATOR):
            recipe = {}
            list = recipe_index.split(INSIDE_SEPARATOR)
            recipe["title"] = list[0].encode("utf-8")
            recipe["ingredients"] = list[1].split("\n")
            for index in range(len(recipe["ingredients"])):
                recipe["ingredients"][index] = recipe["ingredients"][index].encode("utf-8")
            recipe["description"] = list[2].encode("utf-8")
            recipe["image"] = list[3].encode("utf-8")
            recipe["source"] = RECIPES.encode("utf-8")
            
            print >>FILE, json.dumps(recipe, ensure_ascii = False)

    def download_image(self, url):
        image_number = str(self.image_index).zfill(6)
        self.image_index += 1
        image_path = "/img/sc_img" + image_number + ".jpg"
        urllib.urlretrieve(url, os.getcwd() + image_path)
        return image_path

RECIPES = "http://vk.com/my_recept/"
FILE = open("out.txt", "w")
OUTSIDE_SEPARATOR = "\n#\n"
INSIDE_SEPARATOR = "\n$\n"

if __name__ == "__main__":
    extractor = GotovimDomaRecipesExtractor()
    extractor.feed(open("result2.txt", "r").read().decode("utf-8"))
    extractor.clean_recipes()
    extractor.get_recipe_json()
    #print >>FILE, extractor.data.encode("utf-8")