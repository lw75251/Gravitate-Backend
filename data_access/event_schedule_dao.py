"""Author: David Nong
"""

from google.cloud.firestore import Transaction, DocumentReference, DocumentSnapshot, CollectionReference, Client, transactional, Query
import google
from typing import Type
from models import EventSchedule
import warnings
import config

CTX = config.Context

db = CTX.db

class EventScheduleGenericDao:
    """ Description	
        Database access object for eventSchedules
    """

    def __init__(self, userId = None, userRef = None):
        """ Description
            Either userId or userRef must be specified

            :type self:
            :param self:

            :type userId:
            :param userId:

            :type userRef:
            :param userRef:

            :raises:

            :rtype:
        """

        assert (userId != None) or (userRef != None)
        assert (userId == None) or (userRef == None)

        if userId:
            self.eventScheduleCollectionRef = db.collection('users').document(userId).collection('eventSchedules')
        else:
            self.eventScheduleCollectionRef = userRef.collection('eventSchedules')

    
    
    def getWithTransaction(self, transaction: Transaction, eventScheduleRef: DocumentReference) -> Type[EventSchedule]:
        """ Description
            Note that this cannot take place if transaction already received write operations. 
            "If a transaction is used and it already has write operations added, this method cannot be used (i.e. read-after-write is not allowed)."

        :type self:
        :param self:

        :type transaction:Transaction:
        :param transaction:Transaction:

        :type eventScheduleRef:DocumentReference:
        :param eventScheduleRef:DocumentReference:

        :raises:

        :rtype:
        """

        try:
            snapshot: DocumentSnapshot = eventScheduleRef.get(
                transaction=transaction)
            snapshotDict: dict = snapshot.to_dict()
            eventSchedule = EventSchedule.fromDict(snapshotDict)
            return eventSchedule

        except google.cloud.exceptions.NotFound:
            raise Exception('No such document! ' + str(eventScheduleRef.id))

    def get(self, eventScheduleRef: DocumentReference):
        transaction = db.transaction()
        eventScheduleResult = self.getWithTransaction(
            transaction, eventScheduleRef)
        transaction.commit()
        return eventScheduleResult

    def create(self, eventSchedule: Type[EventSchedule])->DocumentReference:
        """ Description
        :type self:
        :param self:

        :type eventSchedule
        :Type[EventSchedule]:


        :raises:

        :rtype:
        """
        _, eventScheduleRef = self.eventScheduleCollectionRef.a(eventSchedule.toDict())
        return eventScheduleRef

    def delete(self, singleEventScheduleRef: DocumentReference):
        """ Description
            This function deletes a ride request from the database

        :type self:
        :param self:

        :type singleEventScheduleRef:DocumentReference:
        :param singleEventScheduleRef:DocumentReference:

        :raises:

        :rtype:
        """
        return singleEventScheduleRef.delete()

    
    @staticmethod
    def setWithTransaction(transaction: Transaction, newEventSchedule: Type[EventSchedule], eventScheduleRef: DocumentReference):
        """ Description
            Note that a read action must have taken place before anything is set with that transaction. 

        :type self:
        :param self:

        :type transaction:Transaction:
        :param transaction:Transaction:

        :type newEventSchedule:Type[EventSchedule]:
        :param newEventSchedule:Type[EventSchedule]:

        :type eventScheduleRef:DocumentReference:
        :param eventScheduleRef:DocumentReference:

        :raises:

        :rtype:
        """
        return transaction.set(eventScheduleRef, newEventSchedule)