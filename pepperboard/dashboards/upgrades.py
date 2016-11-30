#!/usr/bin/env python
# -*- coding:utf-8 -*-


def gendash(output, nthreads):
    import concurrent.futures
    import salt.client
    import salt.runner
    import collections
    import warnings
    from datetime import datetime
    from pepperboard import core
    warnings.simplefilter("ignore", DeprecationWarning)
    result = {}
    noupg = []
    processedserver = []
    if nthreads is None:
        nthreads = 8

    def checkupdates(server):
        c = salt.client.LocalClient()
        upd = c.cmd(server, 'pkg.list_upgrades')
        if server in upd:
            if isinstance(upd[server], dict):
                processedserver.append(server)
                if len(upd[server]) == 0:
                    noupg.append(server)
                else:
                    displaypkgs = '<a style=\"color: #737373\" href=\"javascript:void(0);\" onclick=\"toggle_visibility(\'' + server + '\');\">' + str(
                        len(upd[
                                server])) + '</a><div class=\"pkglist\" id=\"' + server + '\" style=\"display:none\"><ul>' + ''.join(
                        ['<li>{} : {}</li>'.format(k, v) for k, v in
                         collections.OrderedDict(sorted(upd[server].items())).iteritems()]) + '</ul></div>'
                minionos = c.cmd(server, 'grains.items')[server]['os'].lower()
                if minionos in core.logos:
                    displogo = '<img src=\"data:image/png;base64,' + core.logos[minionos] + '\"/> '
                else:
                    displogo = ''
                result[server] = '<tr><td valign=\"top\">' + displogo + server + '</td><td>' + displaypkgs + '</td></tr>\n'
            else:
                result[server] = '<tr><td><img src=\"/' + c.cmd(server, 'grains.items')[server][
                    'os'].lower() + '.png\"/> ' + server + '</td><td>Error during upgrades retrieveing (' + upd[
                                     server] + ')</td></tr>\n'
    begin = datetime.now()
    foutput = open(output, 'w')
    opts = salt.config.master_config('/etc/salt/master')
    opts['quiet'] = True
    r = salt.runner.RunnerClient(opts)
    c = salt.client.LocalClient()
    foutput.write('<html><head>')
    foutput.write(
        '<script type=\"text/javascript\">\nfunction toggle_pkglist() {\nvar e = document.querySelectorAll (\".pkglist\")\nfor (var i = 0; i < e.length; i++) {\nvar el = e[i];\nif(el.style.display == \'block\')\nel.style.display = \'none\';\nelse\nel.style.display = \'block\';\n}\n}\n</script>')
    foutput.write(
        '<script type=\"text/javascript\">\nfunction toggle_visibility(id) {\nvar e = document.getElementById(id);\nif(e.style.display == \'block\')\ne.style.display = \'none\';\nelse\ne.style.display = \'block\';\n}\n</script>')
    foutput.write('<script src=\"//www.kryogenix.org/code/browser/sorttable/sorttable.js\"></script>')
    foutput.write('<link rel=\"stylesheet\" href=\"//yui-s.yahooapis.com/pure/0.6.0/pure-min.css\">')
    foutput.write('<title>Pepperboard - Upgrades</title>')
    foutput.write('</head>')
    foutput.write('<body><div>')
    mdown = r.cmd('manage.down')
    mup = r.cmd('manage.up')
    with concurrent.futures.ThreadPoolExecutor(nthreads) as executor:
        future_to_upd = dict((executor.submit(checkupdates, server), server) for server in mup)
    if len(processedserver) == len(noupg):
        foutput.write('All servers are up-to-date.<br/>')
    else:
        foutput.write(
            '<a href = \"javascript:void(0);\" onclick=\"toggle_pkglist();\" style=\"color: #737373\">Toogle all lists</a></div><table class=\"pure-table pure-table-bordered sortable\"><thead><tr><th>Host</th><th>Upgrades summary</th></tr></thead><tbody>\n')
        resultod = collections.OrderedDict(sorted(result.items()))
        for s in resultod:
            foutput.write(resultod[s])
    end = datetime.now()
    d = end - begin
    foutput.write('</tbody></table>' + str(len(noupg)) + ' up-to-date servers.</br>')
    if len(mdown) > 0:
        foutput.write('Unreachable minions : ' + ",".join(mdown) + '.</br>')
    foutput.write('Last updated on ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.<br/>Generated in ' + str(
        d.seconds) + ' seconds.</body></html>')
    foutput.close()
