
from .nextflow_file import Nextflow_File
from .ro_crate import RO_Crate
from . import constant

import os
import re
import json


class Workflow:
    def __init__(self, file, duplicate=False, display_info=True, 
                 name = None, datePublished=None, description=None,
                 license = None, creativeWorkStatus = None, authors = None, 
                 version = None, keywords = None, producer = None,
                 publisher = None):
        self.nextflow_file = Nextflow_File(file, duplicate = duplicate, display_info = display_info)
        self.rocrate = None
        self.name = name
        self.datePublished = datePublished
        self.description = description
        self.license = license
        self.creativeWorkStatus = creativeWorkStatus
        self.authors = authors
        self.version = version
        self.keywords = keywords
        self.producer = producer
        self.publisher = publisher
        self.log = ""
        self.fill_log()
        self.address = ""
        self.set_address()
        self.dico = {}
        self.get_dico()
    
    def fill_log(self):
        current_directory = os.getcwd()
        os.chdir("/".join(self.nextflow_file.get_file_address().split("/")[:-1]))
        try:
            os.system(f"git log --reverse > temp_{id(self)}.txt")
            with open(f'temp_{id(self)}.txt') as f:
                self.log = f.read()
            os.system(f"rm temp_{id(self)}.txt")
        except:
            None
        os.chdir(current_directory)

    def get_address(self):
        return self.address

    def set_address(self):
        current_directory = os.getcwd()
        os.chdir("/".join(self.nextflow_file.get_file_address().split("/")[:-1]))
        try:
            os.system(f"git ls-remote --get-url origin > temp_address_{id(self)}.txt")
            with open(f'temp_address_{id(self)}.txt') as f:
                self.address = f.read()
            os.system(f"rm temp_address_{id(self)}.txt")
        except:
            None
        os.chdir(current_directory)
        for match in re.finditer(r"https:\/\/github\.com\/([^\.]+)\.git", self.address):
            self.address = match.group(1)

    def get_dico(self):
        current_directory = os.getcwd()
        os.chdir("/".join(self.nextflow_file.get_file_address().split("/")[:-1]))
        try:
            _ = os.system(f"wget -qO - https://api.github.com/repos/{self.address} > temp_dico_{id(self)}.json")
            with open(f'temp_dico_{id(self)}.json') as json_file:
                self.dico = json.load(json_file)
            os.system(f"rm temp_dico_{id(self)}.json")
            
        except:
            _ = os.system(f"rm temp_dico_{id(self)}.json")
        os.chdir(current_directory)
    


    def get_name(self):
        if(self.name==None):
            return self.nextflow_file.get_file_address().split("/")[-2]
        else:
            return self.name

    #Format yyyy-mm-dd
    #Here i return the first commit date
    def get_datePublished(self):
        if(self.datePublished==None):
            for match in re.finditer(r"Date: +\w+ +(\w+) +(\d+) +\d+:\d+:\d+ +(\d+)",self.log):
                month = constant.month_mapping[match.group(1)]
                day = match.group(2)
                year = match.group(3)
                return f"{year}-{month}-{day}"
        else:
            return self.datePublished
        

    def get_description(self):
        if(self.description==None):
            try:
                res = self.dico["description"]
            except:
                res = None
            return res
        else:
            return self.description
        
    

    def get_main_file(self):
        return self.nextflow_file.get_file_address().split("/")[-1]


    def get_license(self):
        if(self.license==None):
            try:
                res = self.dico["license"]["key"]
            except:
                res = None
            return res
        else:
            return self.license
        
    
    #TODO
    def get_creativeWorkStatus(self):
        return "TODO"
    
    #TODO
    def get_version(self):
        return "TODO"


    def get_authors(self):
        if(self.authors==None):
            authors = {}
            for match in re.finditer(r"Author: ([^>]+)<([^>]+)>",self.log):
                authors[match.group(2)] = match.group(1).strip()
            tab = []
            for author in authors:
                #tab.append({"@id":author, "name":authors[author]})
                tab.append({"@id":authors[author], "email":author})
            return tab
        else:
            return self.authors
    

    #Need to follow this format : "rna-seq, nextflow, bioinformatics, reproducibility, workflow, reproducible-research, bioinformatics-pipeline"
    def get_keywords(self):
        if(self.keywords==None):
            try:
                res = ", ".join(self.dico["topics"])
            except:
                res = None
            return res
        else:
            return self.keywords

    

    def get_producer(self):
        if(self.producer==None):
            try:
                res = {"@id": self.dico["owner"]["login"]}
            except:
                res = None
            return res
        else:
            return self.producer
    

    def get_publisher(self):
        if(self.dico!={}):
            return "https://github.com/"
        else:
            return None
    
    def get_output_dir(self):
        return self.nextflow_file.get_output_dir()

    def get_file_address(self):
        return self.nextflow_file.get_file_address()

    def add_2_rocrate(self, dico):
        self.nextflow_file.add_2_rocrate(dico)

    def initialise_rocrate(self):
        self.rocrate = RO_Crate(self)
        self.rocrate.initialise()


    def initialise(self):
        self.nextflow_file.initialise()
        self.initialise_rocrate()

    def generate_all_graphs(self, render_graphs = True, processes_2_remove = []):
        self.nextflow_file.generate_all_graphs(render_graphs = render_graphs, processes_2_remove = processes_2_remove)
