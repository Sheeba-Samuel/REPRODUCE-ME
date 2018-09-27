#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import os


logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.SubExperiment")

class SubExperiment():
    
    def __init__(self):
        self.mapping = [
            ('Experiment Number', 'number', 'Literal', 'reproduce'),
            ('Comment\[IDR Experiment Name\]', 'name', 'Literal', 'reproduce'),
            ('Experiment Description', 'description', 'Literal', 'reproduce'),
            ('Experiment Size', 'size', 'Literal', 'Literal'),
            ('5D Images', 'Literal', 'Literal', 'reproduce'),
            ('Average Image Dimension (XYZCT)', 'Literal', 'Literal', 'reproduce'),
            ('Total Tb', 'Literal', 'Literal', 'reproduce'),
            ('Experiment Example Images', 'hasExample', 'Literal', 'reproduce'),
            ('Experiment Imaging Method', 'usedMethod', 'Literal', 'reproduce'),
            ('Experiment Imaging Method Term Accession', 'usedMethod', 'URIRef', 'other'),
            ('Experiment Comments', 'comment', 'Literal', 'reproduce'),
        ]