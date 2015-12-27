#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unicodecsv as csv
import argparse
from py2neo import authenticate, Graph, Relationship


def read_rows(filename, delimiter=","):
    with open(filename, "rb") as f:
        datareader = csv.reader(f, encoding="utf-8", delimiter=str(delimiter))
        header = next(datareader)

        for line in datareader:
            yield dict(zip(header, line))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Load csv data into neo4j")
    parser.add_argument('--file', dest='file', required=True, help='CSV file with data')
    parser.add_argument('--delimiter', dest='delimiter', default=",", help='Delimiter used')
    parser.add_argument('--user', dest='user', default="neo4j", help='Neo4j user')
    parser.add_argument('--password', dest='password', default="neo4j", help='Neo4j password')
    args = parser.parse_args()

    # Authentication
    authenticate("localhost:7474", args.user, args.password)
    db = Graph()

    # Start with empty database
    db.delete_all()

    # Index your data
    db.cypher.execute("CREATE INDEX ON :Beer(name)")
    db.cypher.execute("CREATE INDEX ON :Brewery(name)")
    db.cypher.execute("CREATE INDEX ON :Alcohol(percentage)")
    db.cypher.execute("CREATE INDEX ON :Type(type)")

    # Add nodes + relations
    # `merge_one` will try to match an existing node
    for row in read_rows(args.file, args.delimiter):
        beer = db.merge_one("Beer", "name", row["Merk"])
        brewer = db.merge_one("Brewery", "name", row["Brouwerij"])
        alc = db.merge_one("Alcohol", "percentage", row["Percentage alcohol"])

        # Add node to db (this is kinda slow, you might want to do it in batches)
        db.create(Relationship(beer, "has_alcohol", alc))
        db.create(Relationship(brewer, "brews", beer))

        # Comma seperated
        for t in row["Soort"].split(","):
            btype = db.merge_one("Type", "type", t)
            db.create(Relationship(beer, "is_a", btype))

    print "Done."
