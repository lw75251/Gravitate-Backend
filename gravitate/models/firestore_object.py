from google.cloud.firestore_v1beta1 import DocumentReference


class FirestoreObject(object):
    __firestoreRef: DocumentReference = None

    def __init__(self):
        pass

    def set_firestore_ref(self, firestore_ref: DocumentReference):
        self.__firestoreRef = firestore_ref

    def get_firestore_ref(self):
        return self.__firestoreRef
