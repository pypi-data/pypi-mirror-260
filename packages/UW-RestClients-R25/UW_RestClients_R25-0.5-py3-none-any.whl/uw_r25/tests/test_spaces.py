# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from commonconf import settings
from uw_r25.spaces import get_space_by_id, get_spaces
from restclients_core.exceptions import DataFailureException
from uw_r25.util import fdao_r25_override


@fdao_r25_override
class R25TestSpaces(TestCase):

    def test_space_by_id(self):
        space = get_space_by_id("1000")
        self.assertEqual(space.space_id, "1000", "space_id")
        self.assertEqual(space.name, "ACC 120", "name")
        self.assertEqual(space.formal_name, "Smith Hall", "formal_name")

    def test_all_spaces(self):
        spaces = get_spaces()
        self.assertEqual(len(spaces), 3, "space count")
