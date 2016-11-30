#!/usr/bin/env python
# -*- coding:utf-8 -*-

import importlib
import sys
from datetime import datetime


def gendashboard(ident, output, nthreads=None, input=None):
    modulename = "pepperboard.dashboards."+ident
    mod = importlib.import_module(modulename, package=None)
    if "gendata" in dir(mod):
        gentable(mod.gendata(input, nthreads), output)
    elif "gendash" in dir(mod):
        mod.gendash(output, nthreads)
    else:
        print "Error : gendata() or gendash() methods not found in "+mod.__name__
        sys.exit(2)


def gentable(input, output):
    foutput = open(output, 'w')
    foutput.write('<html><head>')
    foutput.write(
        '<script type=\"text/javascript\">\nfunction toggle_hstlist() {\nvar e = document.querySelectorAll (\".hstlist\")\nfor (var i = 0; i < e.length; i++) {\nvar el = e[i];\nif(el.style.display == \'block\')\nel.style.display = \'none\';\nelse\nel.style.display = \'block\';\n}\n}\n</script>')
    foutput.write(
        '<script type=\"text/javascript\">\nfunction toggle_visibility(id) {\nvar e = document.getElementById(id);\nif(e.style.display == \'block\')\ne.style.display = \'none\';\nelse\ne.style.display = \'block\';\n}\n</script>')
    foutput.write('<script src=\"//www.kryogenix.org/code/browser/sorttable/sorttable.js\"></script>')
    foutput.write('<style>table.sortable th:not(.sorttable_sorted):not(.sorttable_sorted_reverse):not(.sorttable_nosort):after {content: \" \\25B4\\25BE\"}</style>')
    foutput.write('<link rel=\"stylesheet\" href=\"//yui-s.yahooapis.com/pure/0.6.0/pure-min.css\">')
    foutput.write('<title>Pepperboard</title>')
    foutput.write('</head>')
    foutput.write('<body><div>')
    foutput.write('<table class=\"pure-table pure-table-bordered sortable\"><thead><tr>')
    for header in input['headers']:
        foutput.write('<th>'+header+'</th>')
    foutput.write('</tr></thead><tbody>\n')
    for k, v in input['data'].iteritems():
        if input['ncol'] == 2:
            foutput.write('<tr><td valign=\"top\">'+str(k)+'</td><td>'+str(v)+'</td></tr>\n')
        else:
            foutput.write('<tr><td valign=\"top\">'+str(k)+'</td>')
            for header in input['headers'][1:]:
                if header in v:
                    foutput.write('<td>' + str(v[header]) + '</td>')
                else:
                    foutput.write('<td>grain '+header+' not available</td>')
            foutput.write('</tr>\n')
    foutput.write('</tbody></table>Last updated on ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '</body></html>')
    foutput.close()
