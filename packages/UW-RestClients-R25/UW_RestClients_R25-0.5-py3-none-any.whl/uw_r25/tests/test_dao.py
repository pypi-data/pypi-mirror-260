# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from uw_r25.dao import R25_DAO
from commonconf import override_settings


class R25TestDao(TestCase):

    def test_custom_headers(self):
        self.assertFalse(R25_DAO()._custom_headers('GET', '/', {}, None))
        with override_settings(RESTCLIENTS_R25_BASIC_AUTH='b64here'):
            self.assertEqual(
                R25_DAO()._custom_headers('GET', '/', {}, None),
                {'Authorization': 'Basic b64here'}
            )
