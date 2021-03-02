#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import concurrent.futures
import salt.client
import salt.runner
import collections
import warnings


def gendata(grains, nthreads):

    warnings.simplefilter("ignore", DeprecationWarning)
    result = {}
    toreturn = {}
    if nthreads is None:
        nthreads = 8
    if grains is None:
        print("Error : Grains must be specified")
        sys.exit(2)

    def getgrainscontent(grains, server):
        result[server] = {}
        for grain in grains:
            c = salt.client.LocalClient()
            result[server][grain] = c.cmd(server, 'grains.items')[server][grain]
    opts = salt.config.master_config('/etc/salt/master')
    opts['quiet'] = True
    r = salt.runner.RunnerClient(opts)
    mup = r.cmd('manage.up')
    with concurrent.futures.ThreadPoolExecutor(nthreads) as executor:
        future_to_upd = dict((executor.submit(getgrainscontent, grains, server), server) for server in mup)
    toreturn['ncol'] = 1+len(grains)
    toreturn['headers'] = ['Hostname']
    toreturn['headers'].extend(grains)
    toreturn['data'] = collections.OrderedDict(sorted(result.items()))
    return toreturn
