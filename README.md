### Near-duplicate detection

Module for near-duplicate detection (esp for images)

Allows pluggable hash functions, which can be evaluated hierarchically.

#### TO DO

 - Bugs
     - Figure out centering/scaling issues with `convnetDB.py`
     - Remove repeated code from `imagehashDB.py` and `convnetDB.py`
     - Allow Docker images to access GPU -- otherwise, `convnetDB.py` is going to be too slow...
 
 - Features
     - Would also be good to implement backends that use something like `FALCONN` or `nmslib` for fast lookup.
     - Would also be good to implement out-of-core backends.
