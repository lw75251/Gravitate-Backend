"""
Author: Andrew Kim
Reviewer: Zixuan Rao
"""

from google.cloud.firestore import DocumentReference
from gravitate.domain.event.utils import local_time_from_timestamp
from .firestore_object import FirestoreObject


# event class
class Event(FirestoreObject):
    """ Description
    this class represents the event object
        Note that reference to the object eventRef is deprecated.
        Get and set firestoreRef instead.

    """

    @staticmethod
    def from_dict_and_reference(eventDict, eventRef):
        event = Event.from_dict(eventDict)
        event.set_firestore_ref(eventRef)
        return event

    @staticmethod
    def from_dict(eventDict):
        """ Description
            This function creates an event

            :param eventDict:
        """
        event_category = eventDict['eventCategory']
        participants = eventDict['participants']
        event_location = eventDict['eventLocation']
        start_timestamp = eventDict['startTimestamp']
        end_timestamp = eventDict['endTimestamp']
        pricing = eventDict['pricing']
        location_ref = eventDict['locationRef']
        is_closed = eventDict['isClosed']

        return Event(event_category, participants, event_location, start_timestamp, end_timestamp, pricing, location_ref,
                     is_closed)

    def to_dict(self):
        eventDict = {
            'eventCategory': self.event_category,
            'participants': self.participants,
            'eventLocation': self.event_location,
            'startTimestamp': self.start_timestamp,
            'endTimestamp': self.end_timestamp,
            'pricing': self.pricing,
            'locationRef': self.location_ref,
            'isClosed': self.is_closed
        }
        return eventDict

    def set_as_active(self):
        """ Definition
            Sets the boolean isClosed to False

            :param self:
        """
        self.is_closed = False

    def set_as_passed(self):
        """ Definition
            Sets the boolean isClosed to True

            :param self:
        """
        self.is_closed = True

    def __init__(self, event_category, participants, event_location, start_timestamp, end_timestamp, pricing, location_ref,
                 is_closed):
        """Description
           This function initializes an Event object

           :param self:
           :param event_category:
           :param participants:
           :param event_location:
           :param start_timestamp:
           :param end_timestamp:
           :param pricing:
           :param location_ref: a list of locationRef that corresponds to this event
           :param is_closed:
        """
        self.event_category = event_category
        self.participants = participants
        self.event_location = event_location
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.pricing = pricing
        self.location_ref = location_ref
        self.is_closed = is_closed

    def to_dict_view(self):
        d_view = {
            'eventCategory': self.event_category,
            'participants': self.participants,
            'eventLocation': self.event_location,
            'eventEarliestArrival': local_time_from_timestamp(self.start_timestamp),
            'eventLatestArrival': local_time_from_timestamp(self.end_timestamp),
            'pricing': self.pricing,
            'locationId': self.location_ref.id,
            'isClosed': self.is_closed
        }
        return d_view


class AirportEvent(Event):
    pass


class SocialEvent(Event):
    """ Description
        this class represents the event object
            Note that reference to the object eventRef is deprecated.
            Get and set firestoreRef instead.

        """

    @staticmethod
    def from_dict_and_reference(eventDict, eventRef):
        event = Event.from_dict(eventDict)
        event.set_firestore_ref(eventRef)
        return event

    @staticmethod
    def from_dict(eventDict):
        """ Description
            This function creates an event

            :param eventDict:
        """
        event_category = eventDict['eventCategory']
        participants = eventDict['participants']
        event_location = eventDict['eventLocation']
        start_timestamp = eventDict['startTimestamp']
        end_timestamp = eventDict['endTimestamp']
        pricing = eventDict['pricing']
        is_closed = eventDict['isClosed']
        parking_info = eventDict['parkingInfo']
        event_description = eventDict['description']
        event_name = eventDict['name']
        location_ref = eventDict['locationRef']

        return SocialEvent(event_category, participants, event_location, start_timestamp, end_timestamp, pricing,
                           is_closed, parking_info, event_description, event_name, location_ref)

    def to_dict(self):
        eventDict = {
            'eventCategory': self.event_category,
            'participants': self.participants,
            'eventLocation': self.event_location,
            'startTimestamp': self.start_timestamp,
            'endTimestamp': self.end_timestamp,
            'pricing': self.pricing,
            'isClosed': self.is_closed,
            'parkingInfo': self.parking_info,
            'description': self.event_description,
            'name': self.event_name,
            'locationRef': self.location_ref
        }
        return eventDict

    def set_as_active(self):
        """ Definition
            Sets the boolean isClosed to False

            :param self:
        """
        self.is_closed = False

    def set_as_passed(self):
        """ Definition
            Sets the boolean isClosed to True

            :param self:
        """
        self.is_closed = True

    def __init__(self, event_category, participants, event_location, start_timestamp, end_timestamp, pricing,
                 is_closed, parking_info, event_description, event_name, location_ref):
        """Description
           This function initializes an Event objects

           :param self:
           :param event_category:
           :param participants:
           :param event_location:
           :param start_timestamp:
           :param end_timestamp:
           :param pricing:
           :param location_ref: a list of locationRef that corresponds to this event
           :param is_closed:
           :param event_name:
           :param event_description:
           :param parking_info:
        """
        self.event_category = event_category
        self.participants = participants
        self.event_location = event_location
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.pricing = pricing
        self.is_closed = is_closed
        self.parking_info = parking_info
        self.event_description = event_description
        self.event_name = event_name
        self.location_ref = location_ref

    def to_dict_view(self):
        d_view = {
            'eventCategory': self.event_category,
            'participants': self.participants,
            'eventLocation': self.event_location,
            'eventEarliestArrival': local_time_from_timestamp(self.start_timestamp),
            'eventLatestArrival': local_time_from_timestamp(self.end_timestamp),
            'pricing': self.pricing,
            'locationId': self.location_ref.id,
            'isClosed': self.is_closed
        }
        return d_view
