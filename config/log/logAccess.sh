docker exec -it tfgerenciaredes_varnish_1 /bin/bash
varnishlog -i VCL_call,VCL_return,ReqURL | tee log.txt 
