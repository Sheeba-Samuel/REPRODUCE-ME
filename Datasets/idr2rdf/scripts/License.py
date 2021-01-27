#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import os


logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.Study")

class License():
    
    def __init__(self):
        self.mapping = [
            ('Study License', 'value', 'Literal', 'rdf'),
            ('Study License URL', 'licenseURL', 'Literal', 'reproduce'),
            ('Study Copyright', 'copyright', 'Literal', 'reproduce'),
        ]