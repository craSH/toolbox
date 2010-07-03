#!/usr/bin/env python
# This is a really simple script that tests the hashstore.savedata method.
# It will just crawl all the files in /bin and store them to /tmp/hashstore/[blah]
# and print out their respective paths

import os
from hashstore import savedata

for root, dirs, files in os.walk('/bin'):
    for name in files:
        bindata = open(os.path.join(root, name)).read()
        hashpath = savedata('/tmp/hashstore', bindata)
        print hashpath
