#!/bin/python

from .task import MBIOTask
from .xmlconfig import XMLConfig

import requests


# https://www.sensorpush.com/gateway-cloud-api


class MBIOTaskSensorPush(MBIOTask):
    def initName(self):
        return 'spush'

    def onInit(self):
        self.config.set('refreshperiod', 60)
        self._token=None
        self._timeoutToken=0
        self._timeoutRefresh=0
        self._retry=3
        self.valueDigital('comerr', default=False)

    def onLoad(self, xml: XMLConfig):
        self.config.set('email', xml.get('email'))
        self.config.set('password', xml.get('password'))
        self.config.update('refreshperiod', xml.getInt('refresh'))

    def url(self, path='/'):
        url='https://api.sensorpush.com/api/v1'
        return '%s/%s' % (url, path)

    def post(self, path, data=None):
        try:
            url=self.url(path)
            self.logger.debug(url)

            headers={}
            if self._token:
                headers={'Authorization': self._token}

            r=requests.post(url,
                            headers=headers, payload=data,
                            verify=False, timeout=5.0)
            if r and r.ok:
                data=r.json
                self.logger.debug(data)
                return data
        except:
            self.logger.exception('post')

    def auth(self):
        if self._token and not self.isTimeout(self._timeoutToken):
            return self._token

        if not self.isTimeout(self._timeoutToken):
            return

        self._token=None
        self._timeoutToken=self.timeout(15)

        try:
            data={'email': self.config.email, 'passord': self.config.password}
            r=self.post('oauth/autorize', data)
            if r:
                key=r['autorization']
                if key:
                    data={'authorization': key}
                    r=self.post('oauth/accesstoken', data)
                    if r and r.ok:
                        self._token=r['accesstoken']
                        self._timeoutToken=self.timeout(60*45)
                        return self._token
        except:
            self.logger.exception('auth')

    def deauth(self):
        self._token=None

    def retrieveGateways(self):
        data={'active': True, 'format': 'string'}
        return self.post('device/gateways', data)

    def retrieveSensors(self):
        data={'active': True, 'format': 'string'}
        return self.post('device/sensors', data)

    def retrieveData(self, sensors):
        data={'active': True, 'bulk': True, 'format': 'string',
              'limit': 1, 'sensors': sensors}
        r=self.post('samples', data)
        try:
            # TODO:
            pass
        except:
            pass

    def poweron(self):
        self.auth()
        return True

    def poweroff(self):
        self.deauth()
        return True

    # TODO: adapt
    def decodeValueFloat(self, value, data, datakey, factor=1.0):
        if value is not None and data:
            try:
                v=data[datakey]
                if v and v!='-':
                    v=float(v)*factor
                    value.updateValue(v)
                    value.setError(False)
                    return
            except:
                pass
            value.setError(True)

    def run(self):
        if not self.auth():
            return 5.0

        if self.isTimeout(self._timeoutRefresh):
            self._timeoutRefresh=self.timeout(self.config.refreshperiod)
            error=False

            try:
                # TODO:
                pass
            except:
                # self.logger.exception('meteo')
                error=True

            if not error:
                self._timeoutRefresh=self.timeout(60*10)
                self._retry=3
                self.values.comerr.updateValue(False)
            else:
                self._timeoutRefresh=self.timeout(60)
                if self._retry>0:
                    self._retry-=1
                    if self._retry==0:
                        self.values.comerr.updateValue(True)
                        # TODO: set each error on each values

        return 5.0


if __name__ == "__main__":
    pass
