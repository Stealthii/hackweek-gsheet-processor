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
    business = get_local_gsheet("data/business.json")
    entertainment = get_local_gsheet("data/entertainment.json")
    sport = get_local_gsheet("data/sport.json")

    person_list = []
    person_list.append(get_persons(business, "Business")[0])
    person_list.append(get_persons(entertainment, "Entertainment")[0])
    person_list.append(get_persons(sport, "Sport")[0])

    with open('output.json', 'w') as outfile:
        json.dump(person_list, outfile)
    # hmm = json.dumps([dict(mpn=pn) for pn in person_list])

    # log(hmm)

    # log(query_person("Bill Gates", business, fmt=None))
    # log(entertainment)
    # log(sport)


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


def get_persons(gsheet, sheet_type="Business"):
    """Maps and returns the useful data from a persons"""
    blah = []
    for person in gsheet:
        blah.append({'name': person["gsx$name"]["$t"],
                     'firstName': person["gsx$name"]["$t"].split()[0],
                     'jobTitle': "(unavailable)",
                     'income': person["gsx$earntin7mins"]["$t"],
                     'netWorth': person["gsx$networth"]["$t"],
                     'source': "Forbes",
                     'img': "img/" + person["gsx$name"]["$t"] + ".jpg",
                     'group': sheet_type,
                     'socialData': {'twitterHandler': person["gsx$twitterhandle"]["$t"]}
                     })

    return blah


def query_person(info, person_list, fmt):
    """Returns first person that matches info
    TODO: Vastly improve the logic here

    """
    try:
        return [show_person(person, fmt)
                for person in person_list
                if person["gsx$name"]["$t"] == info][0]
    except IndexError:
        return None


def show_person(person, fmt):
    """Returns a person"""
    if fmt == "json":
        return person  # Close enough
    else:
        return u"\n".join(map(unicode, ["Name: " + person["gsx$name"]["$t"],
                                        "First Name: " + person["gsx$name"]["$t"].split()[0],
                                        "Job Title: (unavailable)",
                                        "Income: " + person["gsx$earntin7mins"]["$t"],
                                        "Net Worth: " + person["gsx$networth"]["$t"],
                                        "Source: (unavailable)",
                                        "Img: img/" + person["gsx$name"]["$t"] + ".jpg",
                                        "Group: Business",
                                        "Twitter: " + person["gsx$twitterhandle"]["$t"]]))


def log_error(*objs):
    print("ERROR:", *objs, file=sys.stderr)


def log_warning(*objs):
    print("WARNING:", *objs, file=sys.stderr)


def log(*objs):
    print(*objs, file=sys.stdout)


if __name__ == '__main__':
    main()
