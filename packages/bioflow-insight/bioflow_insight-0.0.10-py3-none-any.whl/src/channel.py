from .nextflow_building_blocks import Nextflow_Building_Blocks
from .bioflowinsighterror import BioFlowInsightError

class Channel(Nextflow_Building_Blocks):
    def __init__(self, name, origin):
        self.name = name
        self.origin = origin
        to_call = self.get_name_processes_subworkflows()
        if(self.name in to_call):
            raise BioFlowInsightError(f"'{self.name}' is trying to be created as a channel{self.get_string_line(self.origin.get_code())}. It already exists as a process or a subworkflow in the nextflow file.", num = 4, origin=self)
        self.source = []
        self.sink = []


    def get_code(self):
        return self.name.strip()

    def add_source(self, source):
        self.source.append(source)

    def add_sink(self, sink):
        self.sink.append(sink)

    def set_sink_null(self):
        self.sink = []

    def get_type(self):
        return "Channel"

    def equal(self, channel):
        return (self.name==channel.name and self.origin==self.origin)
    
    def get_source(self):
        return self.source

    def remove_element_from_sink(self, ele):
        self.sink.remove(ele)

    def get_sink(self):
        return self.sink
    
    def get_name(self):
        return self.name
    
    def get_structure(self, dico, B):
        for source in self.get_source():
            dico["edges"].append({'A':str(source), 'B':str(B), "label":self.get_name()})



