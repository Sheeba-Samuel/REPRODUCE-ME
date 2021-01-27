#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import os


logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.Agent")

class Agent():
    
    def __init__(self):
        self.mapping = [
            ('Study Person First Name', 'givenName', 'Literal', 'foaf'),
            ('Study Person ORCID', 'ORCID', 'Literal', 'reproduce'),
            ('Study Person Last Name', 'familyName', 'Literal', 'foaf'),
            ('Study Person Email', 'mbox', 'Literal', 'foaf'),
            ('Study Person Address', 'address', 'Literal', 'reproduce'),
            ('Study Person Roles', 'hasRole', 'Literal', 'reproduce')
        ]
 