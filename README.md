Neo4j Cavia Example
===================

Demonstration of neo4j and relations in beer, for Cavia #43 of [via](https://svia.nl), inspired by ["Fun with beer and graphs"](http://blog.bruggen.com/2013/01/fun-with-beer-and-graphs.html).

```
// Get all info about Duvel
MATCH (b:Beer {name:"Duvel"})-[*]->(r) return b,r

// Check who brews Duvel
MATCH (b:Beer {name:"Duvel"})<-[*]-(r) return b,r

// List all beers that the brewer of Duvel also brews
MATCH (:Beer {name:"Duvel"})<-[:brews]-(b:Brewery)-[:brews]->(all:Beer) return b, all;

// Similar beer types
MATCH (b:Beer {name:"Duvel"})-[:is_a]->(t:Type)<-[:is_a]-(all:Beer) return t, all LIMIT 10

// Try to find any relations between two beers. The *0..5 is needed to limit searching
// or you will end up with all nodes in the graph (In a way, they are probably connected)
MATCH (:Beer {name:"Duvel"})-[r*0..5]-(:Beer {name:"Orval"}) return r;
```


## Obtaining data

I used wikipedia to get [lists of belgian beers](https://nl.wikipedia.org/w/index.php?title=Lijst_van_Belgische_bieren&printable=yes).

You can load it into a Google spreadsheet and then export it, but this is limited to a single table :(

```
=IMPORTHTML("https://nl.wikipedia.org/w/index.php?title=Lijst_van_Belgische_bieren&printable=yes", "table")
```

Since it's python, there are modules for this problem. With urllib/requests you can get webpages. Beautifulsoup parses the html and wraps xpath queries for you into usable searching features. You can install and download the example with:

```
pip install -r requirements.txt

python get_data.py --out data/belgian_beers
```


## Getting started

* [Download the Neo4j community edition](http://neo4j.com/download/)
* Fire it up and choose a location for your database
* Choose a password (default is neo4j, neo4j)


## Running the script

Given the example file:

```
python main.py --file data/belgian_beers.csv --user neo4j --password test
```

> For small datasets this is fine, it creates all nodes and relations. If you have GBs of data you might want to
> lookup batch imports and Cypher queries.

Now go to [http://localhost:7474/browser/](http://localhost:7474/browser/) and check out some queries.

