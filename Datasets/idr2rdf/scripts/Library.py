#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import os


logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.Study")

class Library():
    
    def __init__(self):
        self.mapping = [
            ('Library File Name', 'name', 'Literal', 'reproduce'),
            ('Library File Format', 'fileformat', 'Literal', 'reproduce'),
            ('Library Type Term Accession', 'type', 'URIRef', 'other'),
            # ('Library Manufacturer', 'wasAttributedTo', 'URIRef', 'prov'),
            ('Library Version', 'version', 'Literal', 'reproduce'),
            ('Quality Control Description', 'qualitycontrol', 'Literal', 'reproduce'),            
        ]
