from __future__ import print_function
import sys
import re
import math
import logging
import time
from collections import defaultdict

logging.basicConfig(stream = sys.stderr, level=logging.INFO, 
	format='%(levelname)s:%(message)s')
logging.info('Starting parsing')
start_time = time.time()

nodes = []
nodes_meta = defaultdict(dict)
edges = defaultdict(int)
max_indegree = 0

def debug(s):
	print 

for line in sys.stdin.readlines():
	m = re.match("^[^<]*<[ @]([^>]*)> ([^: \",&<>]+)[:,] ", line)
	if m:
		removechars = "<&>\"_^`"
		sender = m.group(1).translate(None, removechars)
		receiver = m.group(2).translate(None, removechars)

		logging.debug(line)
		logging.debug("%s -> %s" % (sender, receiver))

		assert(sender != "" and set("&<>").isdisjoint(set(sender)))
		assert(receiver != "" and set("&<>").isdisjoint(set(receiver)))

		if sender not in nodes:
			nodes.append(sender)
			nodes_meta[sender].setdefault("indegree", 0)
			nodes_meta[sender].setdefault("outdegree", 0)
		if receiver not in nodes:
			nodes.append(receiver)
			nodes_meta[receiver].setdefault("indegree", 0)
			nodes_meta[receiver].setdefault("outdegree", 0)

		edges[(sender, receiver)] += 1

		nodes_meta[receiver]["indegree"] += 1
		nodes_meta[sender]["outdegree"] += 1

		if nodes_meta[receiver]["indegree"] > max_indegree:
			max_indegree = nodes_meta[receiver]["indegree"]


logging.debug(max_indegree)
logging.debug(nodes)
logging.debug(nodes_meta)
logging.debug(edges)

print("""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gephi.org/gexf" xmlns:viz="http://www.gephi.org/gexf/viz">
    <graph mode="static" defaultedgetype="directed">
        <nodes>""")

for i, node in enumerate(nodes):
	if nodes_meta[node]["outdegree"] <= 2:
		logging.debug("skipping node %s" % node)
		continue
	if nodes_meta[node]["indegree"] <= 2:
		logging.debug("skipping node %s" % node)
		continue

	print("""            <node id="%d" label="%s">
              <viz:size value="%f"/>
              <viz:position x="%f" y="%f" z="0.0"/>
            </node>""" % (nodes.index(node), node, float(nodes_meta[node]["indegree"]) / max_indegree,
            			  math.cos(2 * i * math.pi / len(nodes)), math.sin(2 * i * math.pi / len(nodes))))

print("""        </nodes>
        <edges>""")

sum_weight = 0
max_weight = 0
for edge in edges.iteritems():
	sum_weight += edge[1]
	if edge[1] > max_weight:
		max_weight = edge[1]

logging.debug("s: %f" % sum_weight)
logging.debug("mw: %f" % max_weight)

i = 0
for edge in edges.iteritems():
	if nodes_meta[edge[0][0]]["indegree"] <= 2 or nodes_meta[edge[0][0]]["outdegree"] <= 2:
		logging.debug("skipping edge 0 %s -> %s" % (edge[0][0], edge[0][1]))
		continue
	if nodes_meta[edge[0][1]]["indegree"] <= 2 or nodes_meta[edge[0][1]]["outdegree"] <= 2:
		logging.debug("skipping edge 1 %s -> %s" % (edge[0][0], edge[0][1]))
		continue

	weight = float(edge[1]) / max_weight
	logging.debug("e: %f" % edge[1])
	logging.debug("w: %f" % (float(edge[1])/sum_weight) )
	print("""		<edge id="%d" source="%d" target="%d" weight="%f" />""" % (i, 
		nodes.index(edge[0][0]), nodes.index(edge[0][1]), weight))
	i += 1

print("""					</edges>
    </graph>
</gexf>""")

end_time = time.time()
logging.info("Elapsed time was %g seconds" % (end_time - start_time))



