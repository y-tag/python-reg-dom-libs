#
# Florian Sager, 06.08.2008, sager@agitos.de
#
# Python translation:
# TAGAMI Yukihiro, 2010-09-06, tagami.yukihiro@gmail.com
#

import urllib2
import sys

myprint = sys.stdout.write

url = 'http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1'

# Does $search start with $startstring?

def startsWith(search, startstring):
	return search.find(startstring) == 0

# Does $search end with $endstring?

def endsWith(search, endstring):
	return search.find(endstring) == len(search) - len(endstring)


def buildSubdomain(node, tldParts):

	dom = tldParts.pop().strip()

	isNotDomain = False
	if startsWith(dom, "!"):
		dom = dom[1:]
		isNotDomain = True

	if not dom in node:
		if isNotDomain:
			node[dom] = {"!" : ""}
		else:
			node[dom] = {}

	if not isNotDomain and len(tldParts) > 0:
		buildSubdomain(node[dom], tldParts)

def printNode(key, valueTree, isAssignment):

	if isAssignment:
		myprint(str(key) + " = {")
	else:
		if key == "!":
			myprint("u'!' : {}")
			return
		else:
			myprint("u'" + key + "' : {")

	keys = valueTree.keys()
	keys.sort()

	for i in range(len(keys)):

		key = keys[i]

		printNode(key, valueTree[key], False)

		if i+1 != len(valueTree):
			myprint(",\n")

	myprint("}")

tldTree = dict()
domain_list = urllib2.urlopen(url).read()
lines = domain_list.split("\n")
licence = True

myprint("# -*- coding: utf-8 -*-\n")

for line in lines:

	if licence and startsWith(line, "//"):

		myprint("# " + line[2:] + "\n")

		if startsWith(line, "// ***** END LICENSE BLOCK"):
			licence = False
			myprint("\n")
		continue;

	if startsWith(line, "//") or line == '':
		continue;

	# this must be a TLD
	tldParts = line.split('.')

	buildSubdomain(tldTree, tldParts)

printNode("tldTree", tldTree, True)
myprint("\n")

