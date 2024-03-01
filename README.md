# Introduction
This python code will connect to the vcenter and fetch the RHEL hosts with their IPs and then export the result into the CSV.
## Running
Run this code ```python-vmware.py -O filename.csv -s hostname -u username -p password```

- In order to disable ssl check add ``-nossl`` at the end of the arguments.
### PS
Before running this code, add the "Tools" folder from 
https://github.com/vmware/pyvmomi-community-samples/tree/master/samples
