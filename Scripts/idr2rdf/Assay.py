#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import os


logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.Assay")

class Assay():
    
    def __init__(self):
        self.mapping = [
            ('Experiment Assay File', 'name', 'Literal', 'reproduce'),
            ('Quality Control Description', 'qualitycontrol', 'Literal', 'reproduce'),
        ]