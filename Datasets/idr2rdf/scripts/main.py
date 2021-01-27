#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import argparse
import sys
import os
import logging
import re
import glob
import json
import requests
import RDFGraph
import Study
import Parser


from rdflib import URIRef, BNode, Literal, Namespace, Graph, plugin
from rdflib.serializer import Serializer
from rdflib.collection import Collection
from rdflib.namespace import RDF, XSD
from operator import itemgetter
import rdflib
import argparse

logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.main")

def command_line_parser():
    description = "Convert IDR Metadata to."
    example_use = """Example: python idr2rdf metadatafile
                  """
    parser = argparse.ArgumentParser(description=description,
                                     epilog=example_use)

    parser.add_argument("study_file", help="Study File to parse", nargs='+')
    # parser.add_argument("output_file", help="Output RDF", nargs='+')
    parser.add_argument("--strict", action="store_true",
                        help="Fail if unknown keys are detected")
    parser.add_argument("--inspect", action="store_true",
                        help="Inspect the internals of the study directory")
    parser.add_argument("--report", action="store_true",
                        help="Create a report of the generated objects")
    parser.add_argument("--check", action="store_true",
                        help="Check against IDR")
    args = parser.parse_args()

    return parser

def convert_idr_metadata_to_rdf(args, help=''):
    for s in args.study_file:
        for subfile in glob.glob(os.path.join(s + '/**/idr*study.txt'), recursive=True): 
            print(subfile)
            study_number = re.findall(r'\d+', subfile)
            
            graph = RDFGraph.RDFGraph()
            study_parser = Parser.Parser(graph, subfile, 'idr' + study_number[0])
            idr_experiment_rdf = graph.g.serialize(format="turtle").decode('utf-8')
            print("Count****%s", graph.g.__len__())   
            outputfile_name = 'idr' + study_number[0] + '.ttl' 
            open(outputfile_name, 'w+').write(str(idr_experiment_rdf)) 
                
    

def main():
    parser = command_line_parser()
    args = parser.parse_args()
    convert_idr_metadata_to_rdf(args, help=parser.format_help())


if __name__ == '__main__':
    main()
