# Copyright 2016 - Wipro Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module to start galaxia api service
"""

import eventlet
from eventlet import wsgi
import logging
import os
from oslo_config import cfg
import sys

from galaxia.common import service
from galaxia.gapi import api

log = logging.getLogger(__name__)


def main():
    eventlet.monkey_patch(socket=True, select=True, time=True)
    service.prepare_service("gapi", sys.argv)
    log.info('Completed configuration file parsing...')
    log.info('Completed logger initialization...')
    app = api.setup_app()
    log.info('Pecan app setup complete...')

    host, port = cfg.CONF.gapi.host, cfg.CONF.gapi.port

    log.info('Galaxia api server started in PID %s' % os.getpid())
    log.info('Galaxia API is now serving on http://%(host)s:%(port)s' % dict(
            host=host, port=port))
    print ('Galaxia API is now serving on http://%(host)s:%(port)s' % dict(
            host=host, port=port))

    wsgi.server(eventlet.listen((host, port)), app, log=log)
