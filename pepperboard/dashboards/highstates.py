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
    nostate = []
    processedserver = []
    if nthreads is None:
        nthreads = 4

    def simhighstate(server):
        tbc = []
        c = salt.client.LocalClient()
        hst = c.cmd(server, 'state.highstate', ['test', 'True'])
        if server in hst:
            minionos = c.cmd(server, 'grains.items')[server]['os'].lower()
            if isinstance(hst[server], dict):
                for k, v in hst[server].iteritems():
                    if not v['result']:
                        tbc.append("<li>" + v['name'] + "</li>")
                processedserver.append(server)
                if len(tbc) == 0:
                    nostate.append(server)
                else:
                    display = '<a style=\"color: #737373\" href=\"javascript:void(0);\" onclick=\"toggle_visibility(\'' + server + '\');\">' + str(
                        len(
                            tbc)) + ' states to be changed</a><div class=\"hstlist\" id=\"' + server + '\" style=\"display:none\"><ul>' + ''.join(
                        tbc) + '</ul></div>'
                    if minionos in core.logos:
                        displogo = '<div id=\"' + minionos + '\"></div> '
                    else:
                        displogo = ''
                    result[server] = '<tr><td valign=\"top\">' + displogo + server + '</td><td>' + display + '</td></tr>\n'
            else:
                processedserver.append(server)
                result[server] = '<tr><td><img src=\"data:image/png;base64,' + core.logos[minionos] + '\"/>' \
                                 + server + '</td><td>Error during states retrieveing (' + "".join(hst[server]) + ')</td></tr>\n'
    begin = datetime.now()
    foutput = open(output, 'w')
    opts = salt.config.master_config("/etc/salt/master")
    opts['quiet'] = True
    r = salt.runner.RunnerClient(opts)
    c = salt.client.LocalClient()
    foutput.write('<html><head>')
    foutput.write(
        '<script type=\"text/javascript\">\nfunction toggle_hstlist() {\nvar e = document.querySelectorAll (\".hstlist\")\nfor (var i = 0; i < e.length; i++) {\nvar el = e[i];\nif(el.style.display == \'block\')\nel.style.display = \'none\';\nelse\nel.style.display = \'block\';\n}\n}\n</script>')
    foutput.write(
        '<script type=\"text/javascript\">\nfunction toggle_visibility(id) {\nvar e = document.getElementById(id);\nif(e.style.display == \'block\')\ne.style.display = \'none\';\nelse\ne.style.display = \'block\';\n}\n</script>')
    foutput.write(
        '<script>\nfunction search() {\nvar input, filter, table, tr, td, i;\ninput = document.getElementById(\"searchfield\");\nfilter = input.value.toUpperCase();\ntable = document.getElementById(\"results\");\ntr = table.getElementsByTagName(\"tr\");\nfor (i = 0; i < tr.length; i++) {\ntd = tr[i].getElementsByTagName(\"td\")[0];\nif (td) {\nif (td.innerHTML.toUpperCase().indexOf(filter) > -1) {\ntr[i].style.display = \"\";\n} else {\ntr[i].style.display = \"none\";\n}\n}\n}\n}\n</script>'
    )
    foutput.write('<script src=\"//www.kryogenix.org/code/browser/sorttable/sorttable.js\"></script>')
    foutput.write('<style>table.sortable th:not(.sorttable_sorted):not(.sorttable_sorted_reverse):not(.sorttable_nosort):after {content: \" \\25B4\\25BE\"}')
    for os, logo in core.logos.iteritems():
        foutput.write('#'+os+'{background:url(data:image/png;base64,'+logo+') left no-repeat;height:20px;width:20px;float:left;padding-right:5px}')
    foutput.write('</style>')
    foutput.write('<link rel=\"stylesheet\" href=\"//yui-s.yahooapis.com/pure/0.6.0/pure-min.css\">')
    foutput.write('<title>Pepperboard - Out of sync Salt States</title>')
    foutput.write('</head>')
    foutput.write('<body><div>')
    mup = r.cmd('manage.up')
    mdown = r.cmd('manage.down')
    with concurrent.futures.ThreadPoolExecutor(nthreads) as executor:
        future_to_hst = dict((executor.submit(simhighstate, server), server) for server in mup)
    if len(processedserver) == len(nostate):
        foutput.write('All servers are in good state.<br/>')
    else:
        foutput.write(
            '<a href = \"javascript:void(0);\" onclick=\"toggle_hstlist();\" style=\"color: #737373\">Toogle all lists</a>'
        )
        foutput.write('</br><input type=\"text\" id=\"searchfield\" onkeyup=\"search()\" placeholder=\"Search for hostnames...\">')
        foutput.write('</div><table id=\"results\" class=\"pure-table pure-table-bordered sortable\"><thead><tr><th>Host</th><th class=\"sorttable_numeric\">States to be changed in a state.highstate</th></tr></thead><tbody>\n')
        resultod = collections.OrderedDict(sorted(result.items()))
        for s in resultod:
            foutput.write(resultod[s])
    end = datetime.now()
    d = end - begin
    foutput.write('</tbody></table>' + str(len(nostate)) + ' servers in good state.</br>')
    if len(mdown) > 0:
        foutput.write('Unreachable minions : ' + ",".join(mdown) + '.</br>')
    foutput.write('Last updated on ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.<br/>Generated in ' + str(
        d.seconds) + ' seconds.</body></html>')
    foutput.close()
