from typing import Type

from google.cloud.firestore_v1beta1 import Transaction

from gravitate.controllers.grouping.grouping import db
from gravitate.data_access import EventDao, LocationGenericDao, OrbitDao, RideRequestGenericDao
from gravitate.models import Orbit, Location, Event, RideRequest
import gravitate.controllers.grouping.utils as utils


def _refresh_event_schedules_all(transaction: Transaction, in_orbit: dict, not_in_orbit: dict, orbit: Orbit, event,
                                 location):
    """ This function refreshes event schedules of each rideRequests in joined

    :param transaction:
    :param in_orbit:
    :param not_in_orbit:
    :param orbit:
    :param event:
    :param location:
    :return:
    """
    for rid, ride_request in in_orbit.items():
        # (from legacy code:) Note that profile photos may not be populated even after the change is committed
        utils.update_in_orbit_event_schedule(transaction, ride_request, orbit, event, location)

    for rid, ride_request in not_in_orbit.items():
        utils.update_not_in_orbit_event_schedule(transaction, ride_request, event, location)


def id_set_from_dict(d: dict) -> set:
    return {k for k, v in d.items()}


class OrbitGroup:

    """
    This class handles operations of grouping ride requests into orbits.
    Compared to Group, this new class has better atomicity.

    (Experimental)

    TODO: test

    """

    transaction: Transaction

    # To be set in setup
    orbit: Orbit = None
    ride_requests_to_add: dict = None
    ride_requests_existing: dict = None  # key: ride request document id; value: ride request object
    location: Type[Location] = None
    event: Event = None

    def __init__(self):
        # Start a transaction
        self.transaction = db.transaction()

    def setup(self, intended_orbit_id=None, ids_to_add: set = None, event_id=None, location_id=None):
        self.orbit = OrbitGroup._get_orbit(transaction=self.transaction, orbit_id=intended_orbit_id)
        self.ride_requests_existing = \
            OrbitGroup._get_existing_ride_requests(transaction=self.transaction, orbit=self.orbit)
        self.ride_requests_to_add = OrbitGroup._get_ride_requests_to_add(transaction=self.transaction, ids=ids_to_add)
        self.location = OrbitGroup._get_location(transaction=self.transaction, location_id=location_id)
        self.event = OrbitGroup._get_event(transaction=self.transaction, event_id=event_id)

        self._validate_setup()  # Validate fields

    @staticmethod
    def _get_event(transaction: Transaction = None, event_id: str = None) -> Type[Event]:
        event_ref = EventDao().get_ref(event_id)
        return EventDao().get_with_transaction(transaction, event_ref)

    @staticmethod
    def _get_location(transaction: Transaction = None, location_id: str = None) -> Type[Location]:
        location_ref = LocationGenericDao().get_ref_by_id(location_id)
        return LocationGenericDao.get_with_transaction(transaction, location_ref)

    @staticmethod
    def _get_orbit(transaction: Transaction = None, orbit_id: str = None) -> Orbit:
        orbit_ref = OrbitDao().ref_from_id(orbit_id)
        return OrbitDao.get_with_transaction(transaction, orbit_ref)

    @staticmethod
    def _get_existing_ride_requests(transaction: Transaction = None, orbit: Orbit = None) -> dict:
        refs = {ticket["rideRequestRef"] for user_id, ticket in orbit.user_ticket_pairs.items()}
        ride_requests = {ref.id: RideRequestGenericDao.get_with_transaction(transaction, ref) for ref in refs}
        return ride_requests

    def _validate_setup(self):

        def validate_ids(existing, to_add):

            """ Check that we are not adding ride request to one that already exists.

            :param existing:
            :param to_add:
            :return:
            """
            existing_ids: set = id_set_from_dict(existing)
            to_add_ids: set = id_set_from_dict(to_add)
            assert not existing_ids & to_add_ids

        validate_ids(self.ride_requests_existing, self.ride_requests_to_add)
        self._assert_elo_not_none()

    def _assert_elo_not_none(self):
        assert self.event is not None
        assert self.location is not None
        assert self.orbit is not None

    def execute(self) -> set:
        """
                This method puts rideRequests into orbit and update participants eventSchedule in atomic operations.
                :return: a list of rideRequests that are not joined
                """
        orbit = self.orbit

        # Create a transaction so that an exception is thrown when updating an object that is
        #   changed since last read from database
        transaction: Transaction = db.transaction()

        joined_ids = set()
        not_joined_ids = set()

        for rid, r in self.ride_requests_to_add.items():

            print(r.to_dict())

            # Join one rideRequest to the orbit
            is_joined = utils.join_orbit_to_ride_request(r, orbit)

            # when failing to join, record and move on to the next
            if is_joined:
                joined_ids.add(rid)
            else:
                not_joined_ids.add(r)

        # Update database copy of rideRequests
        for rid in joined_ids:
            r = self.ride_requests_to_add.get(rid)

            RideRequestGenericDao.set_with_transaction(
                transaction, r, r.get_firestore_ref())

        # Update database copy of orbit
        OrbitDao.set_with_transaction(
            transaction, orbit, orbit.get_firestore_ref())

        # refresh event schedule for each user

        in_orbit: dict = OrbitGroup._get_in_orbit(existing_ids=id_set_from_dict(self.ride_requests_existing),
                                                  just_joined_ids=joined_ids,
                                                  existing_r=self.ride_requests_existing,
                                                  to_add_r=self.ride_requests_to_add)

        not_in_orbit: dict = OrbitGroup._get_not_in_orbit(not_joined_ids=not_joined_ids,
                                                          existing_r=self.ride_requests_existing)

        _refresh_event_schedules_all(transaction=transaction, in_orbit=in_orbit, not_in_orbit=not_in_orbit,
                                     orbit=orbit, event=self.event, location=self.location)

        print("About to commit: just joined ids {}; not joined ids {}; all ids in orbit after operation: {}"
              .format(joined_ids, not_joined_ids, in_orbit.keys()))

        transaction.commit()

        return not_joined_ids

    @staticmethod
    def _get_not_in_orbit(not_joined_ids: set, existing_r: dict) -> dict:
        return {rid: r for rid, r in existing_r.items() if rid in not_joined_ids}

    @staticmethod
    def _get_in_orbit(existing_ids: set, just_joined_ids: set, existing_r: dict, to_add_r: dict) -> dict:
        """ Returns ride requests as a dict to refresh eventSchedule.

        :param existing_ids:
        :param just_joined_ids:
        :param existing_r:
        :param to_add_r:
        :return:
        """
        in_orbit_ids = existing_ids | just_joined_ids

        def get_ride_requests_all() -> dict:
            """
            Returns a union of ride requests
            :return:
            """
            d: dict = dict(existing_r)
            d.update(to_add_r)
            return d

        ride_requests_all: dict = get_ride_requests_all()

        return {rid: r for rid, r in ride_requests_all.items() if rid in in_orbit_ids}

    @staticmethod
    def _get_ride_requests_to_add(transaction: Transaction = None, ids: set = None) -> dict:
        refs = {RideRequestGenericDao().ref_from_id(rid) for rid in ids}
        ride_requests = {ref.id: RideRequestGenericDao.get_with_transaction(transaction, ref) for ref in refs}
        return ride_requests
