import json

from flask import request
from flask_restful import Resource

from gravitate.controllers.grouping import grouping
from gravitate.data_access import RideRequestGenericDao


class OrbitForceMatchService(Resource):
    """
    This class provides service layer functionality for force matching rideRequests.
        This service should be used in development environment to force a match for testing purposes.
    """
    def post(self):
        requestJson = request.get_json()
        requestForm = json.loads(requestJson) if (
                type(requestJson) != dict) else requestJson

        operationMode = requestForm.get("operationMode", None)
        rideRequestIds = requestForm.get("rideRequestIds", None)
        responseDict = None

        if operationMode == "two" and rideRequestIds != None:
            responseDict = grouping.group_two(rideRequestIds)
        elif operationMode == "many" and rideRequestIds != None:
            grouping.group_many(rideRequestIds)
            responseDict = {"success": True, "operationMode": "many"}
        elif operationMode == "all":
            allRideRequestIds = RideRequestGenericDao().get_ids(incomplete=True)
            grouping.group_many(allRideRequestIds)
            responseDict = {"success": True, "operationMode": "all"}
        else:
            responseDict = {"error": "Not specified operation mode."}
            return responseDict, 400

        # return rideRequest.get_firestore_ref().id, 200
        return responseDict, 200


def refreshGroupAll():
    """ Description
    This function corresponds to use case "grouping ride requests".

    :return:
    """
    allRideRequestIds = RideRequestGenericDao().get_ids(incomplete=True)
    grouping.group_many(allRideRequestIds)
