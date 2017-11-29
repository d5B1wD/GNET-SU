# GNET-SU
An TCP protocol build on UDP.

## NOTE:

* The first layer(proxy layer) controls how much data return to application,
  Other Layer just processes and returns whatever they've got(from lower
  layer).
* The last layer(udp layer) make sure all data send to peer, other layers
  just write as much as they received(from upper layer).


