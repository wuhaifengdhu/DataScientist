#!/usr/bin/python
# -*- coding: utf-8 -*-
import random


class ListHelper(object):
    @staticmethod
    def generate_list_sample(data_list):
        return random.choice(data_list)
