#!/usr/bin/env python

"""
  Rehab Studio Gsheet parser
  Original Author: Daniel Porter
  Original Date: Nov 14, 2014
  Description:

  A Google Spreadsheet parser that will process data or shit

  cmdLine args are:
  (none)

  optionally:
  --format=json (otherwise "default")
"""

from __future__ import print_function

# import argparse
import json
import sys
# import urllib


def main():
    matrix = get_local_gsheet("data/matrix_export.json")

    phone_list = get_phones(matrix)

    with open('output.json', 'w') as outfile:
        json.dump(phone_list, outfile, sort_keys=True, indent=4, separators=(',', ': '))


# def get_gsheet(s=None):
#     """Returns a gsheet in json"""
#     key = "1YVnEXfOLMqa4Z37md-_ofXHp18eMF23wAsxx1O6Kcpw"
#     if s:
#         key = s
#
#     gsheet = urllib.urlopen("https://gsheets.google.com/feeds/list/%s/od6/public/values?alt=json"
#                             % key)
#
#     return json.loads(gsheet.read())["feed"]["entry"]


def get_local_gsheet(s=None):
    """Returns a gsheet already saved locally"""
    json_file = "sheet.json"
    if s:
        json_file = s

    gsheet = open(json_file)
    return json.loads(gsheet.read())["feed"]["entry"]


def get_phones(gsheet):
    """Maps and returns the useful data from the phone list"""
    blah = []
    for phone in gsheet:
        blah.append({'name': phone["gsx$phone"]["$t"],
                     'social_guru': {
                         'share': phone["gsx$share"]["$t"],
                         'chat': phone["gsx$chat"]["$t"],
                         'browse': phone["gsx$browse"]["$t"]},
                     'commuter': {
                         'play_music': phone["gsx$playmusic"]["$t"],
                         'read_books': phone["gsx$readbooks"]["$t"],
                         'games': phone["gsx$games"]["$t"]},
                     'professional': {
                         'multi_task': phone["gsx$multitask"]["$t"],
                         'navigate': phone["gsx$navigate"]["$t"],
                         'longevity': phone["gsx$longevity"]["$t"]},
                     'pic_buff': {
                         'photos': phone["gsx$photos"]["$t"],
                         'video': phone["gsx$video"]["$t"],
                         'hd_playback': phone["gsx$hdplayback"]["$t"]},
                     'g-fan': {
                         'gfan': phone["gsx$gfan"]["$t"]},
                     'outdoor': {
                         'play_outdoors': phone["gsx$playoutdoors"]["$t"],
                         'long_trips': phone["gsx$longtrips"]["$t"],
                         'exploring': phone["gsx$exploring"]["$t"]},
                     'simple': {
                         'calls': phone["gsx$calls"]["$t"],
                         'save_money': phone["gsx$savemoney"]["$t"],
                         'sms': phone["gsx$sms"]["$t"]},
                     'techie': {
                         'latest': phone["gsx$latest"]["$t"],
                         'customise': phone["gsx$customise"]["$t"],
                         'download': phone["gsx$download"]["$t"]}
                     })

    return blah


def log_error(*objs):
    print("ERROR:", *objs, file=sys.stderr)


def log_warning(*objs):
    print("WARNING:", *objs, file=sys.stderr)


def log(*objs):
    print(*objs, file=sys.stdout)


if __name__ == '__main__':
    main()
