#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# nimvelo/__init__.py
# Python 2.7 client library for the Nimvelo/Sipcentric API
# Copyright (c) 2015 Sipcentric Ltd. Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

import sys
import math
import requests
import time
import logging

import simplejson as json

from stream import Stream

logger = logging.getLogger(__name__)


class Nimvelo(object):

  def __init__(self, username, password, base='https://pbx.sipcentric.com/api/v1', customer='me'):

    self.username = username  # Account username
    self.password = password  # Account password
    self.base = base          # Base API URL (default: https://pbx.sipcentric.com/api/v1)
    self.customer = customer  # Customer (default: me)

    # Resources
    self.account = Account(self)
    self.callBundles = CallBundles(self)
    self.recordings = Recordings(self)
    self.phoneBook = PhoneBook(self)
    self.timeIntervals = TimeIntervals(self)
    self.endpoints = Endpoints(self)
    self.phoneNumbers = PhoneNumbers(self)
    self.sms = Sms(self)
    self.creditStatus = CreditStatus(self)
    self.calls = Calls(self)
    self.sounds = Sounds(self)
    self.outgoingCallerIds = OutgoingCallerIds(self)

    self.Stream = Stream(self)

  def _request(self, uri, method='GET', data=None, params=None):

    url = self.base + '/customers/' + self.customer + '/' + uri

    auth = requests.auth.HTTPBasicAuth(self.username, self.password)  # Basic auth

    if method == 'GET':

      if params:
        r = requests.get(url, auth=auth, params=params, verify=True, timeout=3.000)
      else:
        r = requests.get(url, auth=auth, verify=True, timeout=3.000)

    elif method == 'POST':

      headers = {'content-type': 'application/json'}

      if params:
        r = requests.post(url, auth=auth, headers=headers, data=json.dumps(data), params=params, verify=True, timeout=3.000)
      else:
        r = requests.post(url, auth=auth, headers=headers, data=json.dumps(data), verify=True, timeout=3.000)

    if (r.status_code == 200) or (r.status_code == 201):

      try:

        response = r.json()
        return response

      except:

        return True

    elif r.status_code == 401:

      raise AuthenticationException('We couldn\'t authenticate you with the API. Make sure you are using the correct credentials from the \'Web Users\' section of the control panel. If you dont have an account, sign up for one at https://my.nimvelo.com/signup')

      return False

    else:

      if r.json():

        raise Exception('HTTP Error ' + str(r.status_code), r.json())

      else:

        raise Exception('HTTP Error ' + str(r.status_code), 'Something went wrong with the request')

      return False


class Account(object):

  def __init__(self, parent):

    self.parent = parent
    self.uri = '' # Not needed for the base of the customer

  def get(self):

    return self.parent._request(self.uri)


class CallBundles(object):

  def __init__(self, parent):

    self.parent = parent
    self.uri = 'callbundles'

  def get(self):

    return self.parent._request(self.uri)


class Recordings(object):

  def __init__(self, parent):

    self.parent = parent
    self.uri = 'recordings'

  def get(self):

    return self.parent._request(self.uri)


class PhoneBook(object):

  def __init__(self, parent):

    self.parent = parent
    self.uri = 'phonebook'

  def get(self):

    return self.parent._request(self.uri)


class TimeIntervals(object):

  def __init__(self, parent):

    self.parent = parent
    self.uri = 'timeintervals'

  def get(self):

    return self.parent._request(self.uri)


class Endpoints(object):

  def __init__(self, parent):

    self.parent = parent
    self.uri = 'endpoints'

  def get(self):

    return self.parent._request(self.uri)


class PhoneNumbers(object):

  def __init__(self, parent):

    self.parent = parent
    self.uri = 'phonenumbers'

  def get(self):

    return self.parent._request(self.uri)


class Sms(object):

  def __init__(self, parent):

    self.parent = parent
    self.uri = 'sms'

  def get(self):

    return self.parent._request(self.uri)

  def post(self, to=None, _from=None, body=None):

    data = {
      'type': 'smsmessage',
      'to': to,
      'from': _from,
      'body': body
    }

    return self.parent._request(self.uri, method='POST', data=data)


class CreditStatus(object):

  def __init__(self, parent):

    self.parent = parent
    self.uri = 'creditstatus'

  def get(self):

    return self.parent._request(self.uri)


class Calls(object):

  def __init__(self, parent):

    self.parent = parent
    self.uri = 'calls'

  def get(self):

    return self.parent._request(self.uri)


class Sounds(object):

  def __init__(self, parent):

    self.parent = parent
    self.uri = 'sounds'

  def get(self):

    return self.parent._request(self.uri)


class OutgoingCallerIds(object):

  def __init__(self, parent):

    self.parent = parent
    self.uri = 'outgoingcallerids'

  def get(self):

    return self.parent._request(self.uri)


class AuthenticationException(Exception):

  pass


if __name__ == '__main__':
  logging.error('Do not run directly, import module first!')
  sys.exit()
