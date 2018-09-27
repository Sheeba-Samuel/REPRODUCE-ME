#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import os


logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.Study")

class Phenotype():
    
    def __init__(self):
        self.mapping = [
            ('Phenotype Name', 'name', 'Literal', 'reproduce'),
            ('Phenotype Description', 'desciption', 'Literal', 'reproduce'),
            ('Phenotype Term Accession', 'type', 'URIRef', 'other'),
            ('Phenotype Score Type', 'scoretype', 'Literal', 'reproduce'),
        ]