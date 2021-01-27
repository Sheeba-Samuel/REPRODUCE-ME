#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import os


logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.Study")

class Protocol():
    
    def __init__(self):
        self.mapping = [
            ('Protocol Name', 'name', 'Literal', 'reproduce'),
            ('Protocol Description', 'desciption', 'Literal', 'reproduce'),
            ('Protocol Type Term Accession', 'type', 'URIRef', 'other'),
        ]

