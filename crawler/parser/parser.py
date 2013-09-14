#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from HTMLParser import HTMLParser
import sys
import json
import re

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
                        
    def handle_endtag(self, tag):
        if tag == "div":
            if self.inside_content:
                self.inside_content = False
                self.data += SEPARATOR
        elif tag == "a" and self.off:
            self.off = False

    def handle_entityref(self, name):
        if name == "quot":
            self.data += '\"'
    
    def clean_recipes(self):
        self.data = self.data.replace("\nИнгредиенты:\n".decode("utf-8"), "\n$\n")
        self.data = self.data.replace("\nПриготовление:\n".decode("utf-8"), "\n$\n")
        self.data = re.sub("\n *\n* *\n*", "\n", self.data)
        self.data = re.sub(" *\n-? ?", "\n", self.data)
        self.data = re.sub("[0-9]\. ", "", self.data)
        temp_data = self.data.split(SEPARATOR)
        self.data = ""
        for recipe_index in temp_data:
            list = recipe_index.split("\n$\n")
            if len(list) == 3:
                list[0] = list[0].split("\n")[0]
                list[2] = re.sub("\n", " ", list[2])
                self.data += (SEPARATOR + "\n$\n".join(list))
        self.data = self.data[3:]
        #print >>FILE2, self.data.encode("utf-8")
        
    def get_recipe_json(self):
        for recipe_index in self.data.split(SEPARATOR):
            recipe = {}
            list = recipe_index.split("\n$\n")
            recipe["title"] = list[0].encode("utf-8")
            recipe["ingredients"] = list[1].split("\n")
            for index in range(len(recipe["ingredients"])):
                recipe["ingredients"][index] = recipe["ingredients"][index].encode("utf-8")
            recipe["description"] = list[2].encode("utf-8")
            recipe["source"] = RECIPES.encode("utf-8")
            print >>FILE, json.dumps(recipe, ensure_ascii = False)

#NAMES = ["title", "ingregients", "description", "source", "image"]
RECIPES = "http://vk.com/my_recept/"
FILE = open("out.txt", "w")
#FILE2 = open("out2.txt", "w")
SEPARATOR = "\n#\n"

if __name__ == "__main__":
    extractor = GotovimDomaRecipesExtractor()
    extractor.feed(open("result2.txt", "r").read().decode("utf-8"))
    extractor.clean_recipes()
    extractor.get_recipe_json()
    #print >>FILE, extractor.data.encode("utf-8")