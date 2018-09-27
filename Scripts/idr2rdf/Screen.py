#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import os


logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.Study")

class Screen():
    
    def __init__(self):
        self.mapping = [
            ('Screen Number', 'number', 'Literal', 'reproduce'),
            ('Comment\[IDR Screen Name\]', 'id', 'Literal', 'reproduce'),
            ('Screen Description', 'description', 'Literal', 'reproduce'),
            ('Screen Example Images', 'hasExample', 'Literal', 'reproduce'),
            ('Screen Imaging Method Term Accession Number', 'usedMethod', 'URIRef', 'other'),
            ('Screen Technology Type', 'usedTechnology', 'Literal', 'reproduce'),
            ('Screen Technology Term Accession', 'usedTechnology', 'URIRef', 'other'),
            ('Screen Type Term Accession', 'type', 'URIRef', 'other'),
            ('Screen Comments', 'comment', 'Literal', 'reproduce'),
        ]