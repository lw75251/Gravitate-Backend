import json

from flask import request
from flask_restful import Resource

from controllers import grouping
from data_access import RideRequestGenericDao


class OrbitForceMatchService(Resource):
    def post(self):
        requestJson = request.get_json()
        requestForm = json.loads(requestJson) if (
            type(requestJson) != dict) else requestJson

        operationMode = requestForm.get("operationMode", None)
        rideRequestIds = requestForm.get("rideRequestIds", None)
        responseDict = None

        if operationMode == "two" and rideRequestIds != None:
            responseDict = grouping.forceMatchTwoRideRequests(rideRequestIds)
        elif operationMode == "many" and rideRequestIds != None:
            grouping.groupManyRideRequests(rideRequestIds)
            responseDict = {"success": True, "operationMode": "many"}
        elif operationMode == "all":
            allRideRequestIds = RideRequestGenericDao().getIds(incomplete=True)
            grouping.groupManyRideRequests(allRideRequestIds)
            responseDict = {"success": True, "opeartionMode": "all"}
        else:
            responseDict = {"error": "Not specified operation mode."}
            return responseDict, 400

        # return rideRequest.getFirestoreRef().id, 200
        return responseDict, 200


def refreshGroupAll():
    allRideRequestIds = RideRequestGenericDao().getIds(incomplete=True)
    grouping.groupManyRideRequests(allRideRequestIds)