from flask_restful import Resource

from gravitate.context import Context
from gravitate.data_access import EventDao
import gravitate.api_server.utils as service_utils
import gravitate.domain.event.actions as event_actions
from . import parsers as event_parsers
from gravitate.api_server import errors as service_errors
import warnings

from flask_restful import Resource

from gravitate.context import Context
import gravitate.api_server.utils as service_utils

db = Context.db


class EventCreation(Resource):
    @service_utils.authenticate
    def post(self, uid):
        """
                TODO: implement

                This method allows the user to post an event.
                    Expect a JSON form in request.json
                For now, handle only local time in "America/Los_Angeles"

                Form fields required:
                    "eventCategory": "campus" | "social"
                    "eventLocation" (A user-defined text description such as "LAX")
                    "locationRef" (Should have been generated by earlier steps in workflow)
                    "startLocalTime"
                    "endLocalTime"
                    "pricing": 100

                Validation:
                    Reject if:
                        eventCategory is "airport", or is not one of "campus", "social"
                        locationRef is the same as any airport locationRef
                        ...
                    Allow pricing to be empty, and fill in default value



                :param uid:
                :return:
                """
        raise NotImplementedError
        # Verify Firebase auth.
        user_id = uid

        event_dict = None

        eventCategory = args["eventCategory"]

        if eventCategory == "social":
            args = event_parsers.social_event_parser.parse_args()
            event_dict = args.values()
        else:
            raise Exception("Unsupported eventCategory: {}".format(eventCategory))

        print(args)

        # Create RideRequest Object
        event = event_actions.create(args, user_id, event_category=eventCategory)

        # rideRequest Response
        response_dict = {
            "id": event.get_firestore_ref().id
        }

        return response_dict, 200


class EventService(Resource):

    def get(self, eventId):
        event = EventDao().get_by_id(event_id=eventId)
        return event.to_dict_view()
