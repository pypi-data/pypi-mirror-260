# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from commonconf import settings
from uw_r25.reservations import get_reservation_by_id, get_reservations
from restclients_core.exceptions import DataFailureException
from uw_r25.util import fdao_r25_override


@fdao_r25_override
class R25TestReservations(TestCase):

    def test_reservation_by_id(self):
        pass

    def test_get_reservations(self):
        pass
