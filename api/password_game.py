#!/usr/bin/python27
#-*- coding: utf-8 -*-


from data.words import word_list_1, word_list_2
from random import randint

def get_random_word(used_words=[]):
  # Returns a random word
  word_lists = word_list_1 + word_list_2
  if used_words:
    word_lists = list(set(word_lists) - set(used_words))
  word = word_lists[randint(0,len(word_lists))]
  return word

def get_random_avatar():
  # Returns a random avatar url
  return 'http://th02.deviantart.net/fs70/200H/i/2012/112/1/c/random_avatar_by_luchozable-d4x9ccq.png'

