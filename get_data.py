#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import csv
import argparse
import urllib2
from bs4 import BeautifulSoup


# Remove stuff
def norm(s):
    s = re.sub(r"\(.*\)", "", s)
    s = re.sub(r"^.* voor ", "", s)

    s = re.sub(r"\bbij .*$", "", s)
    s = re.sub("\s\s+", " ", s)
    return s.strip()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download csv data from wikipedia")
    parser.add_argument('--out', dest='out', required=True, help='CSV file')
    parser.add_argument('--delimiter', dest='delimiter', default=",", help='Delimiter used')
    args = parser.parse_args()

    wiki_url = 'https://nl.wikipedia.org/wiki/Lijst_van_Belgische_bieren'
    html = urllib2.urlopen(wiki_url).read()
    soup = BeautifulSoup(html, "html.parser")

    with open(args.out + ".csv", "wb") as out:
        writer = csv.writer(out, delimiter=args.delimiter, quoting=csv.QUOTE_MINIMAL)

        # Hardcoded header
        writer.writerow(["Merk", "Soort", "Percentage alcohol", "Brouwerij"])

        for table in soup.findAll('table', {'class': 'wikitable'}):
            for row in table.findAll('tr')[1:]:
                data = []

                for cell in row.findAll('td'):
                    data.append(cell.text)

                try:
                    writer.writerow([norm(v.encode("utf-8")) for v in data])
                except Exception as err:
                    print err
                    print "Error with %s" % data

    print "Done."
