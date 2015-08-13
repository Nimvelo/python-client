#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# nimvelo/stream/__init__.py
# Python 2.7 client library for the Nimvelo/Sipcentric API
# Copyright (c) 2015 Sipcentric Ltd. Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

import multiprocessing
import requests
import time
import logging

import simplejson as json

logger = logging.getLogger(__name__)


class Stream(object):
  '''Allows you to connect to the Nimvelo (Sipcentric) streaming API
     and register callbacks to your own functions.
  '''

  def __init__(self, parent):

    self.parent = parent

    self.process = multiprocessing.Process(target=self.__run)

    self.username = self.parent.username # Account username
    self.password = self.parent.password # Account password
    self.base = self.parent.base + '/stream' # Base streaming URL (default: https://pbx.sipcentric.com/api/v1/stream)

    self.heartbeat = None

    self.eventsCallback = None
    self.incomingcallCallback = None
    self.smsreceivedCallback = None

  def __proccess(self, event):

    event = json.loads(event)

    logger.info('Processing event')
    logger.debug(event)

    if event['event'] == 'heartbeat':

      self.heartbeat = time.time()
      return True

    elif event['event'] == 'incomingcall':

      if self.incomingcallCallback:
        self.incomingcallCallback(event['values'])
        return True

    elif event['event'] == 'smsreceived':

      if self.smsreceivedCallback:
        self.smsreceivedCallback(event['values'])
        return True

    if self.eventsCallback:

      self.eventsCallback(event)
      return True

  def __run(self):

    stream = ''  # Used as a buffer for the stream data
    data = False  # Data is not JSON until we detect it
    level = 0  # JSON object depth

    r = requests.get(self.base, verify=True, auth=(self.username, self.password), stream=True)

    for i in r.iter_content():
      if i == '{':
        stream += i
        level += 1
        data = True

      elif i == '}':
        stream += i
        data = False
        level -= 1

        if level <= 0:
          self.__proccess(stream)
          stream = ''

      elif data is True:
        stream += i

  def register(self, type, callback):

    # Register a function to a callback in the class
    if type == 'incomingcall':
      self.incomingcallCallback = callback
    elif type == 'smsreceived':
      self.smsreceivedCallback = callback
    elif type == 'events':
      self.eventsCallback = callback

    logger.info('Callback registered')

  def connect(self):

    # Start multiprocessing thread
    self.process.start()
    logger.info('Connected')

  def disconnect(self):

    # Terminate multiprocessing thread
    self.process.terminate()
    logger.info('Disconnected')
