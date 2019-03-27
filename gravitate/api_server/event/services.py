from flask import request
from flask_restful import Resource
from google.cloud.firestore import DocumentReference

import gravitate.api_server.utils as service_utils
import gravitate.domain.event.actions as event_actions
import gravitate.domain.event.builders_new as event_builders
import gravitate.domain.event.models as event_models
from gravitate.context import Context
from gravitate.data_access.user_dao import UserDao
from gravitate.domain.event.dao import EventDao
from . import parsers as event_parsers

db = Context.db


class UserEventService(Resource):
    """
    Handles user facebook event upload
    """

    @service_utils.authenticate
    def post(self, uid):
        json_data = request.get_json()
        b = event_builders.FbEventBuilder()
        b.build_with_fb_dict(json_data)
        e: event_models.SocialEvent = b.export_as_class(event_models.SocialEvent)

        # Note that e.firestore_ref will not be set by create()
        ref: DocumentReference = EventDao().create_fb_event(e)
        e.set_firestore_ref(ref)
        dict_view = e.to_dict_view()
        dict_view["eventId"] = ref.id

        # TODO: add error handling
        UserDao().add_user_event_dict(uid, dict_view["fbEventId"], dict_view)

        return {
            "id": e.get_firestore_ref().id
        }

    @service_utils.authenticate
    def put(self, uid):
        json_data = request.get_json()
        event_dicts = json_data["data"]
        ids = list()

        for event_dict in event_dicts:
            b = event_builders.FbEventBuilder()
            # print(event_dict)
            b.build_with_fb_dict(event_dict)
            e: event_models.SocialEvent = b.export_as_class(event_models.SocialEvent)

            # Note that e.firestore_ref will not be set by create()
            ref = EventDao().create_fb_event(e)
            e.set_firestore_ref(ref)
            dict_view = e.to_dict_view()
            dict_view["eventId"] = ref.id

            # TODO: add error handling
            UserDao().add_user_event_dict(uid, dict_view["fbEventId"], dict_view)
            ids.append(ref.id)

        return {
            "ids": ids
        }


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
        event_dict = event.to_dict_view()
        return event_dict
