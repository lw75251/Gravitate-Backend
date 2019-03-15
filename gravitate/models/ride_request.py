"""Author: Zixuan Rao, Andrew Kim
"""

from gravitate.models.target import Target, ToEventTarget, FromEventTarget
from .firestore_object import FirestoreObject
from gravitate.domain.rides.models import Ride as RideRequest
from gravitate.domain.rides.models import SocialEventRide as SocialEventRideRequest
from gravitate.domain.rides.models import AirportRide as AirportRideRequest


#
# class RideRequest(FirestoreObject):
#     """ Description
#         This class represents a RideRequest object
#
#     """
#
#     @staticmethod
#     def from_dict_and_reference(ride_request_dict, ride_request_ref):
#         ride_request = RideRequest.from_dict(ride_request_dict)
#         ride_request.set_firestore_ref(ride_request_ref)
#         return ride_request
#
#     @staticmethod
#     def from_dict(d):
#         """ Description
#             This function creates AirportRideRequest or SocialEventRideRequest.
#                 (RideRequest Factory)
#
#             :param d:
#         """
#         ride_request_type = d['rideCategory']
#
#         driver_status = d['driverStatus']
#         pickup_address = d['pickupAddress']
#         has_checked_in = d['hasCheckedIn']
#         event_ref = d['eventRef']
#         orbit_ref = d['orbitRef']
#         user_id = d['userId']
#         target = Target.from_dict(d['target'])
#         pricing = d['pricing']
#         request_completion = d['requestCompletion']
#
#         if ride_request_type == 'airportRide':
#             flight_local_time = d['flightLocalTime']
#             flight_number = d['flightNumber']
#             airport_location = d['airportLocation']
#             baggages = d['baggages']
#             disabilities = d['disabilities']
#
#             return AirportRideRequest(driver_status, pickup_address, has_checked_in,
#                                       event_ref, orbit_ref, user_id, target, pricing, request_completion, flight_local_time,
#                                       flight_number, airport_location, baggages, disabilities)
#         elif ride_request_type == 'eventRide':
#             location_ref = d['locationRef']
#             return SocialEventRideRequest(driver_status, pickup_address, has_checked_in, event_ref, orbit_ref, user_id, target,
#                                           pricing, request_completion, location_ref)
#         else:
#             raise Exception(
#                 'Not supported rideRequestType: {}'.format(ride_request_type))
#
#     def to_dict(self):
#         ride_request_dict = {
#             'driverStatus': self.driver_status,
#             'pickupAddress': self.pickup_address,
#             'hasCheckedIn': self.has_checked_in,
#             'eventRef': self.event_ref,
#             'orbitRef': self.orbit_ref,
#             'userId': self.user_id,
#             'target': self.target.to_dict(),
#             'pricing': self.pricing,
#             'requestCompletion': self.request_completion
#         }
#         return ride_request_dict
#
#     def to_dict_view(self):
#         """
#         Dict for external presentation / returns for endpoint get
#         :return:
#         """
#         ride_request_dict = {
#             'driverStatus': self.driver_status,
#             'pickupAddress': self.pickup_address,
#             'hasCheckedIn': self.has_checked_in,
#             'eventId': self.event_ref.id,
#             'orbitId': self.orbit_ref.id if self.orbit_ref is not None else None,
#             'userId': self.user_id,
#             'target': self.target.to_dict(),
#             'pricing': self.pricing,
#             'requestCompletion': self.request_completion
#         }
#         return ride_request_dict
#
#     def __init__(self, driver_status, pickup_address, has_checked_in, event_ref, orbit_ref, user_id, target, pricing,
#                  request_completion):
#         """ Description
#             This function initializes a RideRequest Object.
#             Note that this function should not be called directly.
#
#             :param self:
#             :param driver_status:
#             :param pickup_address:
#             :param has_checked_in:
#             :param event_ref:
#             :param orbit_ref:
#             :param target:
#             :param pricing:
#             :param request_completion:
#         """
#
#         self.driver_status = driver_status
#         self.pickup_address = pickup_address
#         self.has_checked_in = has_checked_in
#         self.event_ref = event_ref
#         self.orbit_ref = orbit_ref
#         self.user_id = user_id
#         self.target = target
#         self.pricing = pricing
#         self.request_completion = request_completion
#
#
# class AirportRideRequest(RideRequest):
#
#     # TODO more arguments
#     def __init__(self, driver_status, pickup_address, has_checked_in, event_ref, orbit_ref, user_id, target, pricing,
#                  request_completion, flight_local_time, flight_number, airport_location, baggages, disabilities):
#         """ Description
#             Initializes an AirportRideRequest Object
#             Note that this class should not be initialzed directly.
#             Use RideRequest.from_dict to create an AirportRideRequest.
#
#             :param self:
#             :param driver_status:
#             :param pickup_address:
#             :param has_checked_in:
#             :param event_ref:
#             :param orbit_ref:
#             :param target:
#             :param pricing:
#             :param flight_local_time:
#             :param flight_number:
#             :param airport_location:
#             :param baggages:
#             :param disabilities:
#         """
#
#         super().__init__(driver_status, pickup_address,
#                          has_checked_in, event_ref, orbit_ref, user_id, target, pricing, request_completion)
#         self.ride_category = 'airportRide'
#         self.flight_local_time = flight_local_time
#         self.flight_number = flight_number
#         self.airport_location = airport_location
#         self.baggages = baggages
#         self.disabilities = disabilities
#
#     def to_dict(self):
#         """ Description
#             This function returns the dictionary representation of a RideRequest object
#                 so that it can be stored in the database.
#
#         :type self:
#         :param self:
#
#         :raises:
#
#         :rtype:
#         """
#
#         ride_request_dict = super().to_dict()
#
#         ride_request_dict['rideCategory'] = 'airportRide'
#         ride_request_dict['flightLocalTime'] = self.flight_local_time
#         ride_request_dict['flightNumber'] = self.flight_number
#         ride_request_dict['airportLocation'] = self.airport_location
#         ride_request_dict['baggages'] = self.baggages
#         ride_request_dict['disabilities'] = self.disabilities
#         return ride_request_dict
#
#     def to_dict_view(self):
#         ride_request_dict = super().to_dict_view()
#
#         ride_request_dict['rideCategory'] = 'airportRide'
#         ride_request_dict['flightLocalTime'] = self.flight_local_time
#         ride_request_dict['flightNumber'] = self.flight_number
#         ride_request_dict['locationId'] = self.airport_location.id
#         ride_request_dict['baggages'] = self.baggages
#         ride_request_dict['disabilities'] = self.disabilities
#         return ride_request_dict
#
#
# class SocialEventRideRequest(RideRequest):
#
#     # TODO more arguments
#     def __init__(self, driver_status, pickup_address, has_checked_in, event_ref, orbit_ref, user_id, target, pricing,
#                  request_completion, location_ref):
#         """ Description
#             Initializes a SocialEventRideRequest Object
#             Note that this class should not be initialized directly.
#             Use RideRequest.from_dict to create a SocialEventRideRequest.
#
#         :type self:
#         :param self:
#
#         :type dictionary:
#         :param dictionary:
#
#         :raises:
#
#         :rtype:
#         """
#
#         super().__init__(driver_status, pickup_address,
#                          has_checked_in, event_ref, orbit_ref, user_id, target, pricing, request_completion)
#         self.location_ref = location_ref
#         self.ride_category = 'eventRide'
#
#     def to_dict(self):
#         ride_request_dict = super().to_dict()
#         ride_request_dict['rideCategory'] = 'eventRide'
#         ride_request_dict['locationRef'] = self.location_ref
#
#         return ride_request_dict
#
#     def to_dict_view(self):
#         ride_request_dict = super().to_dict_view()
#
#         ride_request_dict['rideCategory'] = 'eventRide'
#         ride_request_dict['locationId'] = self.location_ref.id
#
#         return ride_request_dict
