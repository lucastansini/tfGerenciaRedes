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
