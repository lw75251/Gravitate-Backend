import unittest
from gravitate import context
from gravitate.domain.rides import RideRequest, RideRequestGenericDao
from test import store

db = context.Context.db


class RideRequestDaoTest(unittest.TestCase):

    def setUp(self):
        self.db = context.Context.db

        # JSON_FILENAME = 'rideRequest_1.json'
        self.rideRequestData1 = store.getMockRideRequest(returnDict=True)
        self.toDelete = list()

    def testCreate(self):
        rideRequestDict = self.rideRequestData1
        rideRequest = RideRequest.from_dict(rideRequestDict)
        RideRequestGenericDao().create(rideRequest)
        resultDict = rideRequest.to_dict()
        self.assertEqual(rideRequestDict, resultDict)

    def testSet(self):
        rideRequestDict = self.rideRequestData1
        rideRequest = RideRequest.from_dict(rideRequestDict)
        RideRequestGenericDao().create(rideRequest)
        RideRequestGenericDao().set(rideRequest)
        ref = rideRequest.get_firestore_ref()
        print(ref)
        self.toDelete.append(ref)
        d = RideRequestGenericDao().get(ref)
        self.assertEqual(rideRequestDict, d.to_dict())

    def tearDown(self):
        for ref in self.toDelete:
            ref.delete()

    # def testGet(self):
    #     rideRequestRef = self.db.collection('rideRequests').document('jhqdAdAhevewgMc7KLO1')
    #     rideRequest = RideRequestGenericDao().getRideRequest(rideRequestRef)
