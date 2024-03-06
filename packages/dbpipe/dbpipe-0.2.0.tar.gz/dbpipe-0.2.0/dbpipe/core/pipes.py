from dataclasses import dataclass, field, asdict
from typing import List, Optional, Literal, Type, Union
import json
import os


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Schedule):
            return obj.__dict__
        if isinstance(obj, Pipe):
            return obj.__dict__
        if isinstance(obj, EndPoint):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

@dataclass
class EndPoint:
    """
    A data structure to track Endpoints

    Attributes:
    ----------
    name: str
        Name of Endpoint

    type: str
        The type of endpoint. API, Database, or file.

    location
        The URL, filepath, or server location.
    """
    name: str
    type: str
    location: Optional[str]

    def __repr__(self):
        return str(asdict(self))
    
    def to_dict(self):
        return asdict(self)
    
        
    def save(self):
        """
        Saves Pipe as a JSON File.
        """
        endpoint_dict = {
            "name": self.name,
            "type":self.type,
            "location":self.location
            
        }

        # Create the "pipes" directory if it doesn't exist
        if not os.path.exists("endpoints"):
            os.makedirs("endpoints")

        # Construct the file path within the "pipes" directory
        file_path = os.path.join("endpoints", self.name+'.json')

        # Write the JSON data to the file
        with open(file_path, 'w') as file:
            json.dump(endpoint_dict, file, indent=4, cls=Encoder)

@dataclass
class Pipe:
    """
    A data structure to document and track data pipelines

    Attributes:
    ----------
    name: str
        Name of the pipeline

    sources: List[str]
        The physical Location of the data. For APIs, this can be the endpoint. For databases, this can be the tables you are pulling from.

    destination: Optional[str]
        The endpoint or table where the data will be loaded.

    logfile: Optional[str]
        The location of the log. Used to troubleshoot the pipeline

    processfile: str
        The location of the pipeline process file
    """
    name: str
    sources: List[Type[EndPoint]]
    destination: Type[EndPoint]
    logfile: Optional[str] = None
    processfile: Optional[str] = None
    
    def __repr__(self):
        return str(asdict(self))
    
    def to_dict(self):
        return asdict(self)
    
    
        
    def save(self):
        """
        Saves Pipe as a JSON File.
        """
        pipe_dict = {
            "name": self.name,
            "sources": self.sources,
            "destination": self.destination,
            "logfile": self.logfile,
            "processfile": self.processfile,
            
        }

        # Create the "pipes" directory if it doesn't exist
        if not os.path.exists("pipes"):
            os.makedirs("pipes")

        # Construct the file path within the "pipes" directory
        file_path = os.path.join("pipes", self.name+'.json')

        # Write the JSON data to the file
        with open(file_path, 'w') as file:
            json.dump(pipe_dict, file, indent=4, cls=Encoder)





@dataclass
class Schedule:
    frequency: str
    start_time: str
    end_time: Optional[str] = None
    time_zone: str = 'UTC'

    def __repr__(self):
        return str(asdict(self))

    def to_dict(self):
        return asdict(self)





        # def __post_init__(self):
    #     valid_frequencies = {"hourly", "daily", "monthly"}
    #     if self.frequency is not None and self.frequency not in valid_frequencies:
    #         raise ValueError("Frequency must be one of 'hourly', 'daily', 'monthly'")



    
@dataclass
class Cluster:
    """
    A class that contains multiple Pipe Objects
    """

    cluster: List[Type[Pipe]]

    def __repr__(self):
        return str(self.cluster)
    
    # def to_list(self):
    #     return self.cluster

    def __iter__(self):
        return iter(self.cluster)
    
    def __str__(self):
        return str([str(item) for item in self.cluster])

    # # Implementing __len__ to make Cluster have a length
    # def __len__(self):
    #     return len(self.cluster)

    # # Implementing __getitem__ to allow indexing
    # def __getitem__(self, index):
    #     return self.cluster[index]


@dataclass
class Job:
    name: str
    schedule: Type[Schedule]
    jobs: List[Union[Type[Pipe], Type[Cluster]]]

    def __repr__(self):
        return str(asdict(self))

    def to_dict(self):
        return asdict(self)
    
    def __post_init__(self):
        if isinstance(self.jobs, Cluster):
            self.jobs = self.jobs.cluster



    def save(self):
        pipe_dict = {
        "name": self.name,
        "schedule":self.schedule,
        "jobs": self.jobs

        }

        # Create the "pipes" directory if it doesn't exist
        if not os.path.exists("jobs"):
            os.makedirs("jobs")

        # Construct the file path within the "pipes" directory
        file_path = os.path.join("jobs", self.name+'.json')

        # Write the JSON data to the file
        with open(file_path, 'w') as file:
            json.dump(pipe_dict, file, indent=4, cls=Encoder)





    