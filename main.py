""" ============================================================================
Python version verification
Required Python version: 3.5
============================================================================ """
import sys

if __name__ != '__main__':
    exit(1)

if sys.version_info.major < 3 or (sys.version_info.major == 3
                                  and sys.version_info.minor < 5):
    print("Error: this application requires Python 3.5 or newer")
    exit(1)

""" ======================================================================== """

import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from subprocess import Popen, PIPE

full_file = ""

if len(sys.argv) != 2:
    print("Erro. Correct Usage: python3 main.py <docker_container>")
    exit(1)

varnish_hit  = 0
varnish_miss = 0
varnish_pass = 0
varnish_total_req = 0

first = True
def draw_graph(line):
    global full_file
    global first
    global varnish_hit
    global varnish_miss
    global varnish_pass
    global varnish_total_req

    n_varnish_hit  = varnish_hit + line.count("HIT")
    n_varnish_miss = varnish_miss + line.count("MISS")
    n_varnish_pass = varnish_pass + line.count("VCL_call       PASS")
    n_varnish_total_req = varnish_total_req + line.count("<< Request  >>")

    if first or ((varnish_hit != n_varnish_hit or varnish_miss != n_varnish_miss or varnish_pass != n_varnish_pass or varnish_total_req != n_varnish_total_req) and n_varnish_hit + n_varnish_miss + n_varnish_pass == n_varnish_total_req):
        fig, (ax1, ax2) = plt.subplots(1, 2, num="Varnish Requests")

        labels = 'HIT', 'MISS', 'PASS'
        sizes = [varnish_hit, varnish_miss, varnish_pass]
        explode = (0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        labels2 = 'Cached', 'Not Cached'
        sizes2 = [varnish_hit, varnish_miss + varnish_pass]
        explode2 = (0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')


        ax1.set_title("Request Result")
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        ax2.set_title("Requests")
        ax2.pie(sizes2, explode=explode2, labels=labels2, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        if first:
            print("Hits: {}".format(n_varnish_hit))
            print("Miss: {}".format(n_varnish_miss))
            print("Pass: {}".format(n_varnish_pass))
            print("Total Requests: {}".format(n_varnish_total_req))
            first = False
            plt.show(block=False)
        else:
            print("\033[F", "\033[F", "\033[F", "\033[F", end='', sep='')
            print("Hits: {}".format(n_varnish_hit))
            print("Miss: {}".format(n_varnish_miss))
            print("Pass: {}".format(n_varnish_pass))
            print("Total Requests: {}".format(n_varnish_total_req))
            plt.draw()
            plt.pause(0.001)
            plt.clf()

    varnish_hit  = n_varnish_hit
    varnish_miss = n_varnish_miss
    varnish_pass = n_varnish_pass
    varnish_total_req = n_varnish_total_req

def run():
    global full_file

    cmd = "docker exec -it {} ".format(sys.argv[1])

    proc = Popen(['docker', 'exec', sys.argv[1],
        'varnishlog', '-i', 'VCL_call,VCL_return,ReqURL,VCL_use,Timestamp,ReqStart,BereqURL'], stdout=PIPE, stderr=PIPE)

    while True:
        retcode = proc.poll()
        if retcode is not None: # Process finished.
            running_procs.remove(proc)
            break
        else: # No process is done, wait a bit and check again.
            print("Monitoring...\n")
            for line in iter(proc.stdout.readline,''):
                full_file += line.rstrip().decode('utf8') + '\n'
                draw_graph(line.rstrip().decode('utf8'))

            time.sleep(1)
            continue

run()
