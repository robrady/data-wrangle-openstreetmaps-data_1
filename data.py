
__author__ = 'ronanbrady2'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import codecs
import json

# This file processes the OSM XML data file using a SAX parser and transforms into JSON format and appends the suffix .json
addrtype = set()

# adds a key to node if the key is present in element attributes
def addkey_cond(element, keyname, node):
    if (keyname in element.attrib):
        node[keyname] = element.attrib[keyname]

# returns a dictionary based on an input XML element.
# The dictionary will have a sub element 'address' and 'created'
# Only elements with tag name 'node' or 'way' are processed
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :

        created = {}
        created["uid"] = element.attrib["uid"]
        created["user"] = element.attrib["user"]
        created["timestamp"] = element.attrib["timestamp"]
        created["changeset"] = element.attrib["changeset"]
        created["version"] = element.attrib["version"]

        node["created"] = created
        node["id"] = element.attrib["id"]
        node["type"] = element.tag
        addkey_cond(element, "visible", node)

        pos = []

        if("lat" in element.attrib) :
            pos.append(float(element.attrib["lat"]))
        if("lon" in element.attrib) :
            pos.append(float(element.attrib["lon"]))

        node["pos"] = pos
        address = {}

        for tag in element.iter("tag"):
            key = tag.attrib['k']
            value = tag.attrib['v']
            # if the key begins with addr then add to the address dictionary.
            # Any other nesting using colon is handled by replacing colon with underscore
            if(key[0:4] == "addr"):
                code = key[5:].replace(":", "_")
                address[code] = value
            elif(key == "amenity"):
                node["amenity"] = value
            elif(key == "cuisine"):
                node["cuisine"] = value
            elif(key == "phone"):
                node["phone"] = value
            elif(key == "name"):
                node["name"] = value
            elif(key == "religion"):
                node["religion"] = value
            elif(key == "capacity"):
                node["capacity"] = value
            elif(key == "denomination"):
                node["denomination"] = value
            elif(key == "beer_garden"):
                node["beer_garden"] = value

        if(len(address) > 0):
            node["address"] = address

        noderefs = []
        for tag in element.iter("nd"):
            ref = tag.attrib['ref']
            noderefs.append(ref)
        if(len(noderefs) > 0):
            node["node_refs"] = noderefs

        return node
    else:
        return None

# This method outputs the dictionary as a json file
def process_map(file_in, pretty = False):

    file_out = "{0}.json".format(file_in)
    data = []
    count = 0
    with codecs.open(file_out, "w") as fo:
        fo.write("[")
        separator = ""
        for _, element in ET.iterparse(file_in):
            count = count + 1
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(separator + json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(separator + json.dumps(el) + "\n")
                separator = ","

        fo.write("]")
    return data



if __name__ == "__main__":
    process_map('dublin_ireland.osm', True)