#!/usr/bin/env python3

'''
For primate euk project, parse multi genbank file, pull metadata for euk ref tree build, merge with mapping file with same accession ids (mapping file column to merge on must have header "TAXID") 
Use: python genbankparse.py myfile.gb map.txt
'''

import sys
import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

data = []

for record in SeqIO.parse(open(sys.argv[1], "r"), "genbank"):
    accession = record.id
    organism = record.annotations["organism"]
    source = None
    host = None
    country = None
    for feature in record.features:
        if "isolation_source" in feature.qualifiers:
            source = feature.qualifiers['isolation_source'][0]
        if "host" in feature.qualifiers:
            host = feature.qualifiers["host"][0]
        if "country" in feature.qualifiers:
            country = feature.qualifiers["country"][0]
    data.append([accession, organism, str(source), str(host), str(country)])
df = pd.DataFrame(data)
df.columns = ['accession', 'organism', 'isolation_source', 'host', 'country']
df.to_csv("metadata.txt", sep="\t", index=False)

meta = pd.read_csv("metadata.txt", sep="\t")
mapping = pd.read_csv(sys.argv[2], sep="\t")

merged = pd.DataFrame.merge(mapping, meta, how="right", left_on="TAXID", right_on="accession")

if merged.shape[0] != mapping.shape[0]:
	print("Warning! Some accession numbers from your mapping file were not in the supplied genbank. Merged mapping file includes %i of %i total accessions." % (merged.shape[0], mapping.shape[0]))

merged.to_csv("merged_mapping.txt", sep="\t", index=False)







