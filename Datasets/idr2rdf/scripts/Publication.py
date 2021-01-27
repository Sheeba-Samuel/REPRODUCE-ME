#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import os


logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.Study")

class Publication():
    
    def __init__(self):
        self.mapping = [
            ('Study DOI', 'doi', 'Literal', 'reproduce'),
            ('Study PubMed ID', 'pubmedid', 'Literal', 'reproduce'),
            ('Study Author List', 'wasAttributedTo', 'Literal', 'reproduce'),
            ('Study PMC ID', 'pmcid', 'Literal', 'reproduce'),
            ('Study Public Release Date', 'wasReleaseOn', 'Literal', 'reproduce'),
        ]
 