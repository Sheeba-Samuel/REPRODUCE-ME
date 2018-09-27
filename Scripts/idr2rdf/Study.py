#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import os


logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.Study")

class Study():
    
    def __init__(self):
        print("We are in Study")
        self.mapping = [
            ('Study Title', 'name', 'Literal', 'reproduce'),
            ('Study Description', 'desciption', 'Literal', 'reproduce'),
            ('Study Type', 'type', 'Literal', 'reproduce'),
            ('Study Type Term Accession', 'type', 'URIRef', 'other'),
            ('Study Public Release Date', 'isReleaseOn', 'Literal', 'reproduce'),
            ('Study External URL', 'isAvailableAt', 'Literal', 'reproduce'),
            ('Study Screens Number', 'hasScreen', 'Literal', 'reproduce'),
            ('Study Data DOI', 'doi', 'Literal', 'reproduce'), 
        ]
 