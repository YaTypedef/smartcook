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
        self.recipe = {}
        self.data = u""
        self.source = u""

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for attr in attrs:
                if attr[0] == 'class' and (attr[1] == 'wall_post_text' or attr[1] == 'pi_text'):
                    self.inside_content = True
                elif attr[0] == 'class' and (attr[1] == 'page_post_queue_wide' or attr[1] == 'medias_thumbs'):
                    self.find_img = True
        elif tag == "img" and self.find_img:
            for attr in attrs:
                if attr[0] == 'src':
                    self.data += attr[1] + SEPARATOR + self.source
        elif tag == "br":
            self.data += '\n'
        elif tag == "a" and self.inside_content:
            for attr in attrs:
                if attr[0] == 'class' and (attr[1] == 'wall_post_more' or attr[1] == 'pi_text_more'):
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
        elif tag == "img":
            self.find_img = False

    def handle_entityref(self, name):
        if name == "quot":
            self.data += '\"'
    
    def clean_recipes(self):
        self.data = re.sub("\n *\n* *\n*", "\n", self.data)
        self.data = re.sub(" *\n", "\n", self.data)
        self.data = re.sub("\nИнгредиенты:\n".decode("utf-8"), SEPARATOR, self.data)
        self.data = re.sub("\nПриготовление:\n".decode("utf-8"), SEPARATOR, self.data)

        list = self.data.split(SEPARATOR)
        if len(list) == 5:
            list[0] = list[0].split("\n")[0]
            list[3] = self.download_image(list[3])
            self.data = SEPARATOR.join(list)
        
    def get_recipe_json(self):
        list = self.data.split(SEPARATOR)
        if len(list) == 5:
            self.recipe["title"] = list[0].encode("utf-8")
            self.recipe["ingredients"] = list[1].split("\n")
            for index in range(len(self.recipe["ingredients"])):
                self.recipe["ingredients"][index] = self.recipe["ingredients"][index].encode("utf-8")
            self.recipe["description"] = list[2].encode("utf-8")
            self.recipe["image"] = list[3].encode("utf-8")
            self.recipe["source"] = list[4].encode("utf-8")

    def download_image(self, url):
        image_number = str(RECIPE_NUMBER).zfill(6)
        image_path = "/img/sc_img" + image_number + ".jpg"
        urllib.urlretrieve(url, os.getcwd() + image_path)
        return image_path
        
    def download_page(self):
        self.source = RECIPES + str(RECIPE_NUMBER)
        input_file = os.getcwd() + "/html/vk_recipes" + str(RECIPE_NUMBER) + ".txt"
        urllib.urlretrieve(self.source, input_file)
        return input_file
        
    def output_data(self):
        #print >>OUTPUT, (self.data + "\n###").encode("utf-8")
        print >>OUTPUT, json.dumps(self.recipe, ensure_ascii = False)

RECIPES = "http://vk.com/wall-30187757_"
RECIPE_NUMBER = 13851
OUTPUT = open("vk_recipes2.txt", "w")
SEPARATOR = "\n$$$\n"
PAGES_COUNT = 1

if __name__ == "__main__":
    for index in range(PAGES_COUNT):
        extractor = GotovimDomaRecipesExtractor()
        INPUT = extractor.download_page()
        extractor.feed(open(INPUT, "r").read().decode("utf-8"))
        extractor.clean_recipes()
        extractor.get_recipe_json()
        extractor.output_data()
        RECIPE_NUMBER -= 1