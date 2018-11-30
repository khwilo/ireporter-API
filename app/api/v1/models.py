"""This module represents an Incidence entity"""
from datetime import datetime

INCIDENCES = []

class IncidenceModel:
    """Entity representation for a Incidence"""
    def __init__(self, createdBy, _type, comment, location, status=None, images=None, videos=None):
        self.id = len(INCIDENCES) + 1
        self.createdOn = str(datetime.utcnow())
        self.createdBy = createdBy
        self.type = _type
        self.comment = comment
        self.location = location
        self.status = "DRAFT" if status is None else status
        self.images = [] if images is None else images
        self.videos = [] if videos is None else videos

    def get_id(self):
        """Return the id of the incidence"""
        return self.id

    def get_type(self):
        """Return the type of the incidence"""
        return self.type

    @staticmethod
    def insert_an_incidence(incidence):
        """Add an incidence record"""
        INCIDENCES.append(incidence)

    @staticmethod
    def get_incidence_by_id(id):
        """Return a particular incidence by its id"""
        incidence = {}
        for i in range(len(INCIDENCES)):
            if INCIDENCES[i].get("id") == id:
                incidence = INCIDENCES[i]
        return incidence

    @staticmethod
    def get_all_incidences():
        """Return all incidences"""
        return INCIDENCES

    @staticmethod
    def delete_by_id(id):
        global INCIDENCES
        INCIDENCES = list(filter(lambda i: i['id'] != id, INCIDENCES))

    def incidence_as_dict(self):
        """Convert an incidence object into a dictionary object"""
        return {
            'id': self.id,
            'createdOn': self.createdOn,
            'createdBy': self.createdBy,
            'type': self.type,
            'location': self.location,
            'status': self.status,
            'comment': self.comment
        }
        