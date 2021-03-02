#!/usr/bin/env python3
# -*- coding:utf-8 -*-


def gendata(apikey, nthreads):
    import sys
    import concurrent.futures
    import salt.client
    import salt.runner
    import collections
    import warnings
    import json
    import requests
    from datetime import datetime
    warnings.simplefilter("ignore", DeprecationWarning)
    result = {}
    toreturn = {}
    if nthreads is None:
        nthreads = 8

    def checkdellwarranty(apikey,serialnumber):
        baseurl = 'https://api.dell.com/support/assetinfo/v4/getassetwarranty/'
        httpresp = requests.get(baseurl+serialnumber+'?apikey='+apikey)
        enddates = []
        for entitlement in json.loads(httpresp.text)['AssetWarrantyResponse'][0]['AssetEntitlementData']:
            enddates.append(entitlement['EndDate'])
        return datetime.strptime(max(enddates),'%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')

    def getwarrantyenddate(server):
        c = salt.client.LocalClient()
        manufacturer = c.cmd(server, 'grains.items')[server]['manufacturer']
        if manufacturer == "Dell Inc.":
            serialnumber = c.cmd(server, 'grains.items')[server]['serialnumber']
            result[server] = checkdellwarranty(apikey,serialnumber)

    opts = salt.config.master_config('/etc/salt/master')
    opts['quiet'] = True
    r = salt.runner.RunnerClient(opts)
    mup = r.cmd('manage.up')
    with concurrent.futures.ThreadPoolExecutor(nthreads) as executor:
        future_to_upd = dict((executor.submit(getwarrantyenddate, server), server) for server in mup)
    toreturn['ncol'] = 2
    toreturn['headers'] = ['Hostname', 'Warranty Expiration']
    toreturn['data'] = collections.OrderedDict(sorted(result.items()))
    return toreturn
