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

import matplotlib.pyplot as plt
import numpy as np

varnish_miss = 0
varnish_hit = 0

full_file = ""

with open('log.txt') as f:
    full_file = f.read()

varnish_hit = full_file.count("HIT")
varnish_miss = full_file.count("MISS")
varnish_pass = full_file.count("-   VCL_call       PASS\n-   VCL_return     fetch")
varnish_total_req = full_file.count("<< Request  >>")

print("Hits: {}".format(varnish_hit))
print("Miss: {}".format(varnish_miss))
print("Pass: {}".format(varnish_pass))
print("Total Requests: {}".format(varnish_total_req))

labels = 'HIT', 'MISS', 'PASS'
sizes = [varnish_hit, varnish_miss, varnish_pass]
explode = (0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

labels2 = 'Chached', 'Not Cached'
sizes2 = [varnish_hit, varnish_miss + varnish_pass]
explode2 = (0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig, (ax1, ax2) = plt.subplots(1, 2, num="Varnish Requests")

ax1.set_title("Request Result")
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

ax2.set_title("Requests")
ax2.pie(sizes2, explode=explode2, labels=labels2, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
