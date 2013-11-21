#!/usr/bin/env python

import os, sys, requests
from lxml import etree
from Feedback import Feedback

def main(argv=None):
  if argv is None:
    argv = sys.argv

  items = Feedback()

  if len(argv) <= 1:
    print "{} <city> <state>".format(argv[0])
    return items

  if ', ' in argv[1]:
    argv[1] = argv[1].replace(', ', ' ')

  if len(argv) == 3:
    find_city = argv[1]
    find_state = argv[2]
  else:
    if ' ' not in argv[1]:
      return items

    find_city, find_state = argv[1].split(' ', 2)
    if len(find_state) != 2:
      return items

  s = requests.Session()
  #s.get("https://tools.usps.com/go/ZipLookupAction!input.action")
  r = s.post("https://tools.usps.com/go/ZipLookupAction.action", data={
    'mode': 0,
    'tCompany': '',
    'tZip': '',
    'tAddress': '',
    'tApt': '',
    'tCity': find_city,
    'sState': find_state,
    'tUrbanCode': '',
    'zip': ''}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'})
  tree = etree.HTML(r.text)

  results = []
  for branch in tree.xpath("//div[@class='data']/p[@class='std-address']"):
    city = branch.xpath("./span[@class='city range']")[0].text
    state = branch.xpath("./span[@class='state range']")[0].text
    zipcode = branch.xpath("./span[@class='zip']")[0].text
    items.add_item(title=zipcode, subtitle="{}, {}".format(city.rstrip(), state), valid='no')

  print items

  return 0

if __name__ == '__main__':
  sys.exit(main())
