#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import getopt
import os.path
import pepperboard.dashboards
import pkgutil
import sys

logos = dict(
    debian='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',
    centos='iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAIAAAAC64paAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAAB3RJTUUH4AgWCysI62xoGgAABARJREFUOMt1lH9M1HUYx5/Pj++X47jjx3nANzDHgAuloMjlzgSmc9XcWiOwH4uFaTFXq9Xa2ty05aZ/NrUtBJM1/5GRTieQC7Fc0CAUR8SPUwYKQnfc7+Pgjvt+v/f9fD79cZKr5vPv87y35/3s/bwAAAAAY0wppZRQSmVZBoB9+5uFYK1tZzAmCKH1JiWEwOMKYwwA7x/8SPPdjF7ZITxdLa3fAwBC6P/DCGPMOS8vL9/urDF0rmpxR9mWY4cP6oMfx5aG5WzFsrOt/bLrl74ek9mMEfYsuK/19oqUWJKkZDL55ZGvjhxrmPT1ZaYXKtatdxY6TcJatqYu3ilZHGWVe2tXlqL+KbfiKPQrcWeNkxkMIYQBBAAwQ4yFOvruHgpE53+a+nRo6ZvpeD9KkxaGQoMnbnY2nvbeXRz4+uqN412x8ArCDy3Q1AJCMLOcu23j52nEYjM/FUxMESDABZGByuiJZzcZqlH1QY3hV5luIIzXD4QwAGCCiqy7E8mAzldzTCXFOXsMriKC9VV94/YSpWoTTzItsla0q8yam8kNlhITxljV1ue+PdXmCp2b8J9LGvFsU4lMrPaMp3OiYZDKGcpChAenfVMXbq+GV1/6rA6I6O8fcDqdpOL5yh/OdkSuLoZLb2kmv4ETCRS0Z5dJyFqY7oi4zSIGmjfy16/TFpt5Q651ILD66t76SHiuunonct9fHDnU65/xbjtaqUMICYkjjRq2gspSpbTC7QoMDc+G55cJJYyxrA0ZP/7uck1729ubioqsVNN1JBNEwDuXFQxKEsWqxpT8DDk3QykFa14807ZsSXcjInFmZFiz6G2hqQYhFABQXkH+je6fpbH4iRFXX/80QeBwKLW1ZWaZ7nmXKcsBq+rjkUnD08+RZMorPvtHc9WLOzrOHy8sLMZ+j6+xuSm/wVGQb/M/CG/Kz6l1lq4EYjIl7tCfuhZIrKyp5grV+kIs4ouE+f7mV7q7W0+ebFlejhBJkjxuN6G0rr4hmVQrKp5ECAVCsVvDs7vqs2yeERJy4ZzNxKygdHv2ltfH5pNN+w4IwQcHB7EQAgAQQN+1CUqxLJNQKN51ZTQtjQIwkCwsOGp4BwBjkungviFt1QeYAgDnfD0rBIUjsZbT15NJNju7FI2qugYgMOYG4kwPTgoBCdcZ3TeCiCw4fxjP1K8hhBvfqbHb05X87Lferu7q+S0zGxDM6fZK+kyWbfObSI2YpE9wnkN6YANYFzPGAODixUte7xLnbHw8ce9e2eGjHw64v5hYGpoxKS9Xnrp0fqb3eo9sshA84/MsCG4AQMrvvyoFirrX3vBGxzsndt+PXfiutf1xMHgEkBRi/sHQgfeaheCtrW2PMETJfzD0N9NJ3yDwxM6sAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDE2LTA4LTIyVDEzOjQzOjA0KzAyOjAwd9gEzwAAACV0RVh0ZGF0ZTptb2RpZnkAMjAxNS0wNy0yMFQxNTo0ODoxNCswMjowMG9thioAAAAASUVORK5CYII=')


def usage():
    print("USAGE: " + sys.argv[0] + " [OPTIONS]")
    print("Pepperboard : neat and simple salt dashboards")
    print("--help|-h : Prints an awesome help message")
    print("--output=|-o : comma separated values of files to write dashboards given with the \"-d\" argument")
    print("--dashboards=|-d : comma separated values of dashboards")
    print("--threads=|-t : comma separated values of threads count to be used (must be greater than 0). Prefix the number by \"f\" if you want more threads than CPU core count")
    print("--grains=|-g : comma separated values of grains to be used with the mgrains dashboard. This argument implies \"-d 'mgrains'\"")
    print("--dellapikey=|-a : Dell API key used by the dellwarranty dashboard. This argument implies \"-d 'mgrains'\"")
    print("--list|-l : List available dashboards")


def getmasterstatus():
    import psutil
    for proc in psutil.process_iter():
        if proc.name() == 'salt-master':
            return 0
        if len(proc.cmdline()) > 0 and 'salt-master' in proc.cmdline()[0]:
            return 0
    return 1


def countminions():
    import salt.runner
    opts = salt.config.master_config("/etc/salt/master")
    opts['quiet'] = True
    r = salt.runner.RunnerClient(opts)
    return len(r.cmd('manage.present'))


def pepper_main():
    if getmasterstatus() == 1:
        print("Error : Your Salt Master isn't running. Exiting...")
        usage()
        sys.exit(2)

    if countminions() == 0:
        print("Error : You don't have any minions registered to the Salt Master. Exiting...")
        usage()
        sys.exit(2)

    if not sys.argv[1:]:
        print("Error : Pepperboard wrongly called")
        usage()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'o:d:t:g:a:lh',
                                   ['output=', 'dashboards=', 'threads=', 'grains=', 'dellapikey=', 'list', 'help'])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    available_dashboards = [name for _, name, _ in
                            pkgutil.iter_modules([os.path.dirname(pepperboard.dashboards.__file__)])]

    outputs = list()
    dashs = list()
    nthreads = list()
    raw_nthreads = list()
    grains = list()
    dellapikey = ''
    for o, a in opts:
        if o in ("-o", "--output"):
            if not a:
                print("Error : missing output file")
                usage()
                sys.exit(2)
            else:
                outputs = a.split(',')
        elif o in ("-t", "--threads"):
            if not a:
                print("Error : Missing thread number")
                usage()
                sys.exit(2)
            else:
                raw_nthreads = a.split(',')
                for th in raw_nthreads:
                    if th.startswith('f'):
                        nthreads.append(int(th[1:]))
                    else:
                        try:
                            from psutil import cpu_count
                        except ImportError:
                            raise ImportError("You need psutil python module")
                        if int(th) > cpu_count(logical=True):
                            print("Error : threads count cannot be greater than CPU core count unless you force it with \"f\" before the number")
                            sys.exit(2)
                        elif int(th) == 0:
                            print("Error : threads count must be greater than 0")
                            usage()
                            sys.exit(2)
                        else:
                            nthreads.append(int(th))
        elif o in ("-d", "--dashboards"):
            if not a:
                print("Error : Missing dashboards list")
                usage()
                sys.exit(2)
            else:
                dashs = a.split(',')
                for dash in dashs:
                    if dash not in available_dashboards:
                        print("Error : Dashboard " + dash + " not available.")
                        sys.exit(2)
        elif o in ("-g", "--grains"):
            if not a:
                print("Error : mgrains argument must be a CSV list")
                usage()
                sys.exit(2)
            else:
                if not "mgrains" in dashs:
                    dashs.append("mgrains")
                grains = a.split(',')
        elif o in ("-a", "--dellapikey"):
            if not a:
                print("Error : dellapikey argument can't be empty")
                usage()
                sys.exit(2)
            else:
                if not "dellwarranty" in dashs:
                    dashs.append("dellwarranty")
                dellapikey = a
        elif o in ("-l", "--list"):
            print("\n".join(available_dashboards))
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            print("Unhandled option")

    if 'mgrains' in dashs and len(grains) == 0:
        print("Error : You must the grains list when using the mgrains dashboard")
        sys.exit(2)

    if 'dellwarranty' in dashs and not dellapikey:
        print("Error : You must set the dellapikey when using the dellwarranty dashboard")
        sys.exit(2)

    if len(nthreads) == 0:
        if not len(outputs) == len(dashs):
            print("Error : All lists aren't the same size")
            sys.exit(2)
        else:
            for dash, out in zip(dashs, outputs):
                if dash == 'mgrains':
                    pepperboard.dashboards.gendashboard(dash, out, input=grains)
                elif dash == 'dellwarranty':
                    pepperboard.dashboards.gendashboard(dash, out, input=dellapikey)
                else:
                    pepperboard.dashboards.gendashboard(dash, out)
    else:
        if not len(outputs) == len(nthreads) == len(dashs):
            print("Error : All lists aren't the same size")
            sys.exit(2)
        else:
            for dash, out, nth in zip(dashs, outputs, nthreads):
                if dash == 'mgrains':
                    pepperboard.dashboards.gendashboard(dash, out, nth, grains)
                elif dash == 'dellwarranty':
                    pepperboard.dashboards.gendashboard(dash, out, nth, dellapikey)
                else:
                    pepperboard.dashboards.gendashboard(dash, out, nth)
