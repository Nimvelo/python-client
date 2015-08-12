# Nimvelo Python Client

Python 2.7 client library for the Nimvelo/Sipcentric API

```python
from nimvelo import Nimvelo
nimvelo = Nimvelo(username="myusername", password="mypassword")
print nimvelo.sms.post(_from="0123", to="03301201200", body="Hello World!")
```

## Install

### Best method

```
sudo pip install nimvelo
```

### Manual method

```
git clone git@github.com:Nimvelo/python-client.git && cd python-client
sudo python setup.py install
```

## Getting started

### Examples

**Get account details**

```python
from nimvelo import Nimvelo

nimvelo = Nimvelo(username="myusername", password="mypassword")

print nimvelo.account.get()
```

**Connect to the streaming api**

```python
from nimvelo import Nimvelo

nimvelo = Nimvelo(username="myusername", password="mypassword")
stream = nimvelo.Stream

def callHandler(call):
  print 'Incoming call from ' + call['callerIdName'] + ' (' + call['callerIdNumber'] + ')'

def smsHandler(sms):
  print sms['excerpt'] + ' from: ' + sms['from']

stream.register(type='incomingcall', callback=callHandler)
stream.register(type='smsreceived', callback=smsHandler)

stream.connect()
```

## Reference

- nimvelo.Nimvelo(username, password, base='https://pbx.sipcentric.com/api/v1', customer='me')
  - account
    - get()
  - callBundles
    - get()
  - recordings
    - get()
  - phoneBook
    - get()
  - timeIntervals
    - get()
  - endpoints
    - get()
  - phoneNumbers
    - get()
  - sms
    - get()
    - post(to, _from, body)
  - creditStatus
    - get()
  - calls
    - get()
  - sounds
    - get()
  - outgoingCallerIds
    - get()
  - Stream
    - register(type, callback)
    - connect()
    - disconnect()
