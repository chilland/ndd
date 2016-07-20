### Near-duplicate detection

Module for near-duplicate detection, eg for images

 - Allows pluggable hash functions, which can be evaluated in a hierarchy from fast to slow.
 - Eventually would be good to drop CNN-feature cosine distance as a robust "hash".
 - Would also be good to implement backends that use something like `FALCONN` or `nmslib` for fast lookup.
 - Would also be good to implement out-of-core backends.


#### TO DO

 - Return distance for non-exact queries
 - Add Dockerized version
