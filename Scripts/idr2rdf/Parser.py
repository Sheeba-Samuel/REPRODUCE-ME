#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Sheeba Samuel <sheeba.samuel@uni-jena.de>

from __future__ import absolute_import
import logging
import re
import os
import requests


from rdflib import URIRef, BNode, Literal, Namespace, Graph, plugin
from rdflib.serializer import Serializer
from rdflib.collection import Collection
from rdflib.namespace import RDF, XSD
from operator import itemgetter
import rdflib
import argparse
import Agent, Assay, ExperimentalData, Library, License, Organism, Phenotype, Protocol, Publication, Screen, Study, SubExperiment

logging.basicConfig(level=int(os.environ.get("DEBUG", logging.INFO)))
log = logging.getLogger("idr2rdf.Study")

TYPES = ["Experiment", "Screen"]

class Parser():
    
    def __init__(self, graph, study_file, study_number):
        self._study_file = study_file
        self.g = graph.g
        self.graph = graph
        self.study_number = study_number
        self.initialise_source_mapping()

        self.IDR_BASE_URL = "http://idr.openmicroscopy.org"
        self.INDEX_PAGE = "%s/webclient/?experimenter=-1" % self.IDR_BASE_URL
        self.create_idr_session()
        
        self.open_study_file()
        self.parse_study_file()

    def create_idr_session(self):
        # create http session
        with requests.Session() as self.session:
            request = requests.Request('GET', self.INDEX_PAGE)
            prepped = self.session.prepare_request(request)
            response = self.session.send(prepped)
            if response.status_code != 200:
                response.raise_for_status() 
    
    def initialise_source_mapping(self):
        self.source_mapping = {
            'EFO' : 'http://www.ebi.ac.uk/efo/',
            'NCBITaxon' : 'http://purl.obolibrary.org/obo/',
            'CMPO' : 'http://www.ebi.ac.uk/cmpo/',
            'FBbi' : 'http://purl.obolibrary.org/obo/',
            
        }
        self.source_mapping =  {k.lower(): v for k, v in self.source_mapping.items()}
        
    
    def parse_study_file(self):
        experiment = Study.Study()
        self.experiment = URIRef(self.graph.reproduce['Experiment' + '_' + self.study_number]) 
        self.g.add( (self.experiment, RDF.type, URIRef(self.graph.reproduce["Experiment"])) )
        self.parse(self.experiment, experiment.mapping)


        self.imaging_study = URIRef(self.graph.reproduce['ImagingStudy' + '_' + self.study_number])
        self.g.add( (self.imaging_study, RDF.type, URIRef(self.graph.reproduce["ImagingStudy"])) )

        agent = Agent.Agent()        
        self.parse_agent(agent.mapping)      
        

        license = License.License()
        self.license = URIRef(self.graph.reproduce['License' + '_' + self.study_number])  
        self.g.add( (self.license, RDF.type, URIRef(self.graph.reproduce["License"])) )
        self.parse(self.license, license.mapping)        

        publication = Publication.Publication()        
        self.publication = URIRef(self.graph.reproduce['Publication' + '_' + self.study_number])   
        self.g.add( (self.publication, RDF.type, URIRef(self.graph.reproduce["Publication"])) )
        self.parse(self.publication, publication.mapping) 

        organism = Organism.Organism()        
        self.organism = URIRef(self.graph.reproduce['Organism' + '_' + self.study_number])  
        self.g.add( (self.organism, RDF.type, URIRef(self.graph.reproduce["Organism"])) )
        self.parse(self.organism, organism.mapping) 

        self.parse_screen()
        self.parse_assay()

    def parse_screen(self):
        screen = Screen.Screen()    
        value = self.get_value('Study Screens Number')
        screen_ids = []
        

        if value:
            with open('./input', 'r') as f:  
                lines = f.readlines()
                for idx, val in enumerate(lines):
                    if self.study_number in val:    
                        screen_id =  val.split(":")[1].strip()
                        screen_ids.append(screen_id)
            for i in range(1, int(value) + 1):
                lines = self.get_lines(i, 'Screen')
                self.screen = URIRef(self.graph.reproduce['Screen' + '_' + self.study_number + '_' + str(i)])  
                self.g.add( (self.screen, RDF.type, URIRef(self.graph.reproduce["Screen"])) )
                self.g.add( (self.screen, self.graph.pplan.isOutputVarOf, self.imaging_study) )
                try:
                    self.g.add( (self.screen, self.graph.reproduce.id, Literal(screen_ids[i-1])) )
                    self.get_all_screen_images(screen_ids[i-1])
                except IndexError:
                    log.debug("Parsing %s %g" % ('Screen', i))
                self.parse(self.screen, screen.mapping, lines=lines)

                #ProcessedData
                self.processed_data = URIRef(self.graph.reproduce['ProcessedData' + '_' + self.study_number + '_' + str(i)])
                self.g.add( (self.processed_data, RDF.type, URIRef(self.graph.reproduce["ProcessedData"])) )
                self.g.add( (self.processed_data, self.graph.reproduce.name,  Literal(self.get_value('Processed Data File Name', lines=lines))))
                self.g.add( (self.processed_data, self.graph.pplan.isVariableOfPlan, self.experiment) )
                self.g.add( (self.processed_data, self.graph.pplan.isOutputVarOf, self.imaging_study) )

                experimentalData = ExperimentalData.ExperimentalData()
                self.experimentalData = URIRef(self.graph.reproduce['ExperimentalData' + '_' + self.study_number + '_' + str(i)]) 
                self.g.add( (self.experimentalData, RDF.type, URIRef(self.graph.reproduce["ExperimentalData"])) )
                self.parse(self.experimentalData, experimentalData.mapping, lines=lines)
                self.g.add( (self.experimentalData, self.graph.pplan.isVariableOfPlan, self.experiment) )

                library = Library.Library()  
                self.library = URIRef(self.graph.reproduce['Library' + '_' + self.study_number + '_' + str(i)])   
                self.g.add( (self.library, RDF.type, URIRef(self.graph.reproduce["Library"])) )      
                self.parse(self.library, library.mapping, lines=lines)
                self.g.add( (self.library, self.graph.pplan.isInputVarOf, self.imaging_study) )

                manufacturer_name = self.get_value('Library Manufacturer', lines=lines)
                if manufacturer_name:
                    self.library_agent = URIRef(self.graph.reproduce['Agent' + '_' + self.study_number + 'Library' + '_' + str(i)])  
                    self.g.add( (self.library_agent, RDF.type, URIRef(self.graph.prov["Agent"])) )
                    self.g.add( (self.library_agent, self.graph.reproduce.name,  Literal(manufacturer_name)))
                    self.g.add( (self.library_agent, self.graph.reproduce.hasRole, Literal('Manufacturer')) )
                    self.g.add( (self.library, self.graph.prov.wasAttributedTo, self.library_agent) )

                self.experimentcondition = URIRef(self.graph.reproduce['ExperimentalCondition' + '_' + self.study_number + '_' + str(i)])   
                self.g.add( (self.experimentcondition, RDF.type, URIRef(self.graph.reproduce["ExperimentalCondition"])) )      
                self.g.add( (self.experimentcondition, RDF.value,  Literal(self.get_value('Library Experimental Conditions', lines=lines))))
                self.g.add( (self.experimentcondition, self.graph.reproduce.type,  Literal(self.get_value('Library Experimental Conditions Term Accession', lines=lines))))
                self.g.add( (self.imaging_study, self.graph.reproduce.hasExperimentalCondition, self.experimentcondition))       

                exp_type = 'Screen'

                phenotype = Phenotype.Phenotype()
                self.parse_phenotype(phenotype.mapping, i, exp_type, lines=lines)

                protocol = Protocol.Protocol()  
                self.parse_protocol(protocol.mapping, i, exp_type, lines=lines)

            
    def parse_assay(self):
        subExperiment = SubExperiment.SubExperiment()    
        value = self.get_value('Study Experiments Number') 
        
        if value:
            project_ids = []
            with open('./input', 'r') as f:  
                lines = f.readlines()
                for idx, val in enumerate(lines):
                    if self.study_number in val: 
                        project_id =  val.split(":")[1].strip()
                        project_ids.append(project_id)
            for i in range(1, int(value) + 1):
                lines = self.get_lines(i, 'Experiment')
                self.subexperiment = URIRef(self.graph.reproduce['SubExperiment' + '_' + self.study_number + '_' + str(i)])   
                self.g.add( (self.subexperiment, RDF.type, URIRef(self.graph.pplan["Step"])) )
                self.parse(self.subexperiment, subExperiment.mapping, lines=lines)
                self.g.add( (self.subexperiment, self.graph.pplan.isStepOfPlan, self.experiment) )

                try:
                    self.g.add( (self.subexperiment, self.graph.reproduce.id, Literal(project_ids[i-1])) )
                    self.get_all_experiment_images(project_ids[i-1])
                except IndexError:
                    log.debug("Parsing %s %g" % ('Screen', i))

                assay = Assay.Assay()
                self.assay = URIRef(self.graph.reproduce['Assay' + '_' + self.study_number  + '_' + str(i)])  
                self.g.add( (self.assay, RDF.type, URIRef(self.graph.reproduce["Assay"])) )
                self.parse(self.assay, assay.mapping, lines=lines)
                self.g.add( (self.assay, self.graph.pplan.isOutputVarOf, self.subexperiment) )


                #ProcessedData
                self.processed_data = URIRef(self.graph.reproduce['ProcessedData' + '_' + self.study_number + '_' + str(i)])
                self.g.add( (self.processed_data, RDF.type, URIRef(self.graph.reproduce["ProcessedData"])) )
                self.g.add( (self.processed_data, RDF.value,  Literal(self.get_value('Processed Data File Name', lines=lines))))
                self.g.add( (self.processed_data, self.graph.pplan.isVariableOfPlan, self.experiment) )
                self.g.add( (self.processed_data, self.graph.pplan.isOutputVarOf, self.imaging_study) )

                experimentalData = ExperimentalData.ExperimentalData()
                self.experimentalData = URIRef(self.graph.reproduce['ExperimentalData' + '_' + self.study_number + '_' + str(i)]) 
                self.g.add( (self.experimentalData, RDF.type, URIRef(self.graph.reproduce["ExperimentalData"])) )
                self.parse(self.experimentalData, experimentalData.mapping, lines=lines)
                self.g.add( (self.experimentalData, self.graph.pplan.isVariableOfPlan, self.experiment) )                

                self.experimentcondition = URIRef(self.graph.reproduce['ExperimentalCondition' + '_' + self.study_number + '_' + str(i)])   
                self.g.add( (self.experimentcondition, RDF.type, URIRef(self.graph.reproduce["ExperimentalCondition"])) )      
                self.g.add( (self.experimentcondition, RDF.value,  Literal(self.get_value('Assay Experimental Conditions', lines=lines))))
                self.g.add( (self.experimentcondition, self.graph.reproduce.type,  Literal(self.get_value('Assay Experimental Conditions Term Accession', lines=lines))))
                self.g.add( (self.subexperiment, self.graph.reproduce.hasExperimentalCondition, self.experimentcondition))

                exp_type = 'Experiment'
                phenotype = Phenotype.Phenotype()
                self.parse_phenotype(phenotype.mapping, i, exp_type, lines=lines)

                protocol = Protocol.Protocol()  
                self.parse_protocol(protocol.mapping, i, exp_type, lines=lines)  
        
        self.initialise_relations()
        


    def initialise_relations(self):
        
        self.g.add( (self.imaging_study, self.graph.pplan.isStepOfPlan, self.experiment) )
        self.g.add( (self.publication, self.graph.pplan.isVariableOfPlan, self.experiment) )
        self.g.add( (self.publication, self.graph.pplan.isOutputVarOf, self.imaging_study) )
        self.g.add( (self.license, self.graph.pplan.isVariableOfPlan, self.experiment ))          
        self.g.add( (self.license, self.graph.pplan.isOutputVarOf, self.imaging_study) )                
        self.g.add( (self.organism, self.graph.pplan.isInputVarOf, self.imaging_study) )
        self.g.add( (self.organism, self.graph.pplan.isVariableOfPlan, self.experiment ))   
        self.g.add( (self.experiment, self.graph.prov.wasAttributedTo, self.agent ))   


    def open_study_file(self):
        with open(self._study_file, 'r') as f:
            log.info("Parsing %s" % self._study_file)
            self._study_lines = f.readlines()
            self._study_lines_used = [
                [] for x in range(len(self._study_lines))]

    def get_value(self, key, expr=".*", lines=None):
        pattern = re.compile("^%s\t(%s)" % (key, expr))
        if lines:
            # Fake space since we don't know what the caller is passing
            used = [[] for x in range(len(lines))]
        else:
            lines = self._study_lines
            used = self._study_lines_used
        for idx, line in enumerate(lines):
            m = pattern.match(line)
            if m:
                used[idx].append(("get_value", key, expr))
                return m.group(1).rstrip()

    def get_lines(self, index, component_type):
        PATTERN = re.compile("^%s Number\t(\d+)" % component_type)
        found = False
        lines = []
        for idx, line in enumerate(self._study_lines):
            m = PATTERN.match(line)
            if m:
                if int(m.group(1)) == index:
                    found = True
                elif int(m.group(1)) != index and found:
                    return lines
            if found:
                self._study_lines_used[idx].append(("get_lines", index))
                lines.append(line)
        if not lines:
            raise Exception("Could not find %s %g" % (component_type, index))
        return lines
    
    def get_array_value(self, value):
        if value:
            array_value = re.split(r'\t+', value)
            return array_value
        else:
            return
    

    def get_array_value_at_index(self, value, idx):
        if value:
            array_value = self.get_array_value(value)
            if array_value:
                try:
                    return array_value[idx]
                except IndexError:
                    return                
            else:
                return
        else:
            return

    def parse_agent(self, mapping, lines=None):        
        agent_names = self.get_value('Study Person First Name', lines=lines)
        agent_names = re.split(r'\t+', agent_names)
                
        for idx in range(1, len(agent_names) + 1):
            self.agent = URIRef(self.graph.reproduce['Agent' + '_' + self.study_number + '_' + str(idx)])  
            self.g.add( (self.agent, RDF.type, URIRef(self.graph.prov["Agent"])) )
            self.g.add( (self.experiment, self.graph.prov.wasAttributedTo, self.agent) )
            for key, ontology_term, ontology_type, ontology_name in mapping:
                if ontology_name == 'foaf':
                    self.g.add( (self.agent, self.graph.foaf[ontology_term], Literal(self.get_array_value_at_index(self.get_value(key, lines=lines), idx - 1) ))) 
                else:
                    self.g.add( (self.agent, self.graph.reproduce[ontology_term], Literal(self.get_array_value_at_index(self.get_value(key, lines=lines), idx - 1) ))) 
                
        
        publisher_name = self.get_value('Study Data Publisher', lines=lines)
        if publisher_name:
            self.agent = URIRef(self.graph.reproduce['Agent' + '_' + self.study_number])  
            self.g.add( (self.agent, RDF.type, URIRef(self.graph.prov["Agent"])) )
            self.g.add( (self.experiment, self.graph.prov.wasAttributedTo, self.agent) )
            self.g.add( (self.agent, self.graph.foaf.givenName, Literal(publisher_name)) )
            self.g.add( (self.agent, self.graph.reproduce.hasRole, Literal('Data Publisher')) )



    def parse_phenotype(self, mapping, i, exp_type, lines=None):        
        phenotype_names = self.get_value('Phenotype Name', lines=lines)
        phenotype_names = re.split(r'\t+', phenotype_names)
                
        for idx in range(1, len(phenotype_names) + 1):
            self.phenotype = URIRef(self.graph.reproduce['Phenotype' + '_' + self.study_number + '_' + str(i) + '_' + str(idx)])  
            self.g.add( (self.phenotype, RDF.type, URIRef(self.graph.reproduce["Phenotype"])) )
            self.g.add( (self.phenotype, self.graph.pplan.isOutputVarOf, self.imaging_study) )
            
            for key, ontology_term, ontology_type, ontology_name in mapping:
                self.g.add( (self.phenotype, self.graph.reproduce[ontology_term], Literal(self.get_array_value_at_index(self.get_value(key, lines=lines), idx - 1) ))) 

    def parse_protocol(self, mapping, i, exp_type, lines=None):        
        protocol_names = self.get_value('Protocol Name', lines=lines)
        protocol_names = re.split(r'\t+', protocol_names)

        for idx in range(1, len(protocol_names) + 1):
            self.protocol = URIRef(self.graph.reproduce['Protocol' + '_' + self.study_number + '_' + str(i) + '_' + str(idx)])  
            self.g.add( (self.protocol, RDF.type, URIRef(self.graph.reproduce["Protocol"])) )            
            
            if exp_type == 'Screen':
                self.g.add( (self.screen, self.graph.pplan.isVariableOfPlan, self.protocol) )
            elif exp_type == 'Experiment':
                self.g.add( (self.protocol, self.graph.pplan.isSubPlanOfPlan, self.experiment) )

            
            for key, ontology_term, ontology_type, ontology_name in mapping:
                self.g.add( (self.protocol, self.graph.reproduce[ontology_term], Literal(self.get_array_value_at_index(self.get_value(key, lines=lines), idx - 1) ))) 

    


    def parse(self, source_node, mapping, lines=None): 
        for key, ontology_term, ontology_type, ontology_name in mapping:
            value = self.get_value(key, lines=lines)
            
            if ontology_type == 'Literal':
                value = Literal(value)
            elif ontology_type == 'URIRef' and ontology_name == 'other': 
                if value:
                    ontology_source = value.rsplit('_', 1)[0]
                    if ontology_source.lower() in self.source_mapping:
                        value = self.source_mapping[ontology_source.lower()] + value
                        value = URIRef(value)
                        self.g.add( (source_node, self.graph.reproduce[ontology_term], value ))
            elif ontology_type == 'URIRef'  and ontology_name != 'other':
                value = URIRef(value)
            if ontology_name == 'reproduce':
                self.g.add( (source_node, self.graph.reproduce[ontology_term], value ))
            elif ontology_name == 'prov':
                self.g.add( (source_node, self.graph.prov[ontology_term], value ))
            elif ontology_name == 'pplan':
                self.g.add( (source_node, self.graph.reproduce[ontology_term], value ))
            elif ontology_name == 'foaf':
                self.g.add( (source_node, self.graph.foaf[ontology_term], value ))
            elif ontology_name == 'rdf':
                self.g.add( (source_node, RDF.value, value ))

    def get_all_screen_images(self, screen_id):

        PLATES_URL = "{base}/webclient/api/plates/?id={screen_id}"

        qs = {'base': self.IDR_BASE_URL, 'screen_id': screen_id}
        url = PLATES_URL.format(**qs)
        for p in self.session.get(url).json()['plates']:
            plate_id = p['id']

            WELLS_IMAGES_URL = "{base}/webgateway/plate/{plate_id}/{field}/"

            qs = {'base': self.IDR_BASE_URL, 'plate_id': plate_id, 'field': 0}
            url = WELLS_IMAGES_URL.format(**qs)
            grid = self.session.get(url).json()
            for row in grid['grid']:
                self.get_all_images(row)
                
                                

    def get_all_experiment_images(self, project_id):

        DATASET_URL = "{base}/webclient/api/datasets/?id={project_id}"

        IMAGE_URL = "{base}/webclient/api/images/?id={dataset_id}"
        qs = {'base': self.IDR_BASE_URL, 'project_id': project_id}
        url = DATASET_URL.format(**qs)
        for p in self.session.get(url).json()['datasets']:
            dataset_id = p['id']
            qs = {'base': self.IDR_BASE_URL, 'dataset_id': dataset_id}
            url = IMAGE_URL.format(**qs)
            self.get_all_images(self.session.get(url).json()['images'])
            
            

    def get_all_images(self, images):
        print("Count of all images:%s", len(images))
        for i in images:
            if i is not None:
                MAP_URL = "{base}/webclient/api/annotations/?type=map&{type}={image_id}"
                IMAGE_ID = i['id']
                self.image = URIRef(self.graph.reproduce['Image' + '_' + self.study_number + '_' + str(IMAGE_ID)])   
                self.g.add( (self.image, RDF.type, URIRef(self.graph.reproduce["Image"]) ))
                self.g.add( (self.image, self.graph.pplan.isOutputVarOf, self.imaging_study) )
                

                IMAGE_URL = "{base}/webclient/?show=image-{image_id}"
                image_url = IMAGE_URL.format(**{'base': self.IDR_BASE_URL, 'image_id': IMAGE_ID})
                self.g.add( (self.image, self.graph.reproduce.isAvailableAt, Literal(image_url)) )
                
                qs = {'base': self.IDR_BASE_URL, 'type': 'image', 'image_id': IMAGE_ID}
                url = MAP_URL.format(**qs)
                for a in self.session.get(url).json()['annotations']:
                    for v in a['values']:
                        key = re.sub('[^0-9a-zA-Z]+', '', v[0])
                        value = v[1]
                        ontology_term = key + '_' + str(IMAGE_ID)
                        self.g.add( (self.graph.reproduce[ontology_term], RDF.type, URIRef(self.graph.reproduce[key]) ))
                        self.g.add( (self.graph.reproduce[ontology_term], RDF.value, Literal(value)) )
                        self.g.add( (self.image, self.graph.reproduce.reference, self.graph.reproduce[ontology_term]) )
