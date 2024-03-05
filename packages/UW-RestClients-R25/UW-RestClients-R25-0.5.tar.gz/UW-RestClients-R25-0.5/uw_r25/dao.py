# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import re
from os.path import abspath, dirname
from restclients_core.dao import DAO


class R25_DAO(DAO):
    def service_name(self):
        return 'r25'

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]

    def _custom_headers(self, method, url, headers, body):
        basic_auth = self.get_service_setting('BASIC_AUTH')
        if basic_auth is not None:
            return {"Authorization": "Basic {}".format(basic_auth)}
