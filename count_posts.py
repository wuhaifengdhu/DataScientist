#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.store_helper import StoreHelper


def count_post_number():
    total_count = 0
    for i in range(8535):
        phrase_dict_file = "./data/result_dict/%04d.dat" % i
        if StoreHelper.is_file_exist(phrase_dict_file):
            total_count += 1
    print ("Total have %d post files" % total_count)


def show_data_structure_of_position_tag():
    position_tag = StoreHelper.load_data("./history/position_tag.dat", {})
    print (type(position_tag))
    print (position_tag)


show_data_structure_of_position_tag()
