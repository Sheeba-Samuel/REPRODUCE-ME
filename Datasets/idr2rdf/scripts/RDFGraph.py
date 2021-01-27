#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import re
import os


from rdflib import URIRef, BNode, Literal, Namespace, Graph, plugin
from rdflib.serializer import Serializer
from rdflib.collection import Collection
from rdflib.namespace import RDF, XSD
from operator import itemgetter
import rdflib
import argparse

logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.RDFGraph")


class RDFGraph():
    def initialise_graph(self):
        self.g.bind('p-plan', self.pplan)
        self.g.bind('repr', self.reproduce)
        self.g.bind('prov', self.prov)
        self.g.bind('foaf', self.foaf)        
        self.g.bind('owl', self.owl)
    
    def initialise_source_mapping(self):
        self.source_mapping = {
            'EFO' : 'http://www.ebi.ac.uk/efo/',
            'NCBITaxon' : 'http://purl.obolibrary.org/obo/',
            'CMPO' : 'http://www.ebi.ac.uk/cmpo/',
            'FBbi' : 'http://purl.obolibrary.org/obo/',
            
        }
        self.source_mapping =  {k.lower(): v for k, v in self.source_mapping.items()}
    

    def __init__(self):
        self.g = Graph()
        self.pplan = Namespace("http://purl.org/net/p-plan#")
        self.reproduce = Namespace("https://w3id.org/reproduceme#")
        self.prov = Namespace("http://www.w3.org/ns/prov/#")
        self.foaf = Namespace("http://xmlns.com/foaf/0.1/#")
        self.owl = Namespace("http://www.w3.org/2002/07/owl#")
        self.initialise_graph()
