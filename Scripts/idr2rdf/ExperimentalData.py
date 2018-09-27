#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import os


logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.ExperimentalData")

class ExperimentalData():
    
    def __init__(self):
        self.mapping = [
            ('Feature Level Data File Name', 'name', 'Literal', 'reproduce'),
            ('Feature Level Data File Description', 'description', 'Literal', 'reproduce'),
            ('Feature Level Data File Format', 'fileformat', 'Literal', 'reproduce'),
            # ('Feature Level Data Column Name', 'columnname', 'Literal', 'reproduce'),
            # ('Feature Level Data Column Description', 'columndescription', 'Literal', 'reproduce'),
                      
        ]