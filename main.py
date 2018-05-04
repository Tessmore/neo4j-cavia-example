#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import argparse
from py2neo import authenticate, Graph, Node, Relationship


def read_rows(filename, delimiter=","):
    datareader = csv.reader(open(filename, newline=""), delimiter=str(delimiter))
    header = next(datareader)

    for line in datareader:
        if not line:
            continue

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

    # Start with empty database
    graph = Graph()
    graph.delete_all()

    # Index your data
    graph.run("CREATE INDEX ON :Beer(name)")
    graph.run("CREATE INDEX ON :Brewery(name)")
    graph.run("CREATE INDEX ON :Alcohol(percentage)")
    graph.run("CREATE INDEX ON :Type(type)")

    # Add nodes + relations
    # `merge` will try to match an existing node
    for row in read_rows(args.file, args.delimiter):
        beer   = Node("Beer", name=row["Merk"])
        brewer = Node("Brewery", name=row["Brouwerij"])
        alc    = Node("Alcohol", percentage=row["Percentage alcohol"])

        graph.merge(beer)
        graph.merge(brewer)
        graph.merge(alc)

        # Add node to graph (this is kinda slow, you might want to do it in batches)
        graph.create(Relationship(beer, "has_alcohol", alc))
        graph.create(Relationship(brewer, "brews", beer))

        # # Comma seperated
        # for t in row["Soort"].split(","):
        #     btype = graph.merge("Type", "type", t)
        #     graph.create(Relationship(beer, "is_a", btype))

    print("Done.")
