#!/usr/bin/env python
#
# Copywrite (C) 2010 Ian Gallagher <crash@neg9.org>
#

import os
import hashlib


def savedata(basedir, data, hash_override=None, hashalgo="sha256"):
    """
    Given a base directory and chunk of data, store that data in a path
    composed of it's SHA256 (default) hexdigest as split in to single-byte
    hex directories, with the file being the last byte of the digest.

    Paramater basedir: The base directory to store this data in
    Parameter data: The data to store and which the path is derived from
    Parameter hashalgo: The hashing algorithm to use (as supported by python's
    hashlib module)

    Returns a string which is the complete path to the newly written file.
    """

    # TODO: Support using a file-like object instead of a 'data' string later

    if not basedir:
        raise ValueError("basedir not provided")

    if not hash_override:
        # We were not provided a hash to use, generate based on the data

        hash = hashlib.new(hashalgo)
        hash.update(data)
        hex_digest = hash.hexdigest()
    else:
        # We were provided a "hash" to use
        hex_digest = hash_override

    fh = hashpath(basedir, hex_digest, 'w')
    if fh:
        fh.write(data)
        fh.close()
    else:
        raise Exception("Error obtaining filehandle from hashpath method")

    return fh.name

def hashpath(basedir, hash, *args):

    if not basedir:
        raise ValueError("basedir not provided")
    if not hash:
        raise ValueError("hash not provided")
    if not args:
        args = ('w',)

    # Split hash string into two character chunks
    displit = lambda x, acc=[]: displit(x[2:], acc+[(x[:2])]) if x else acc
    hash_chunks = displit(hash)

    # Ensure each digraph is alphanumeric only - prevent directory traversal etc.
    hash_chunks = filter(lambda x: x.isalnum(), hash_chunks)

    # Seperate out the directory parts and file part
    hash_dirs = hash_chunks[:-1]
    hash_file = hash_chunks[-1]

    hash_directory = os.path.join(basedir, os.path.sep.join(hash_dirs))
    if not os.path.exists(hash_directory):
        try:
            os.makedirs(hash_directory)
        except Exception as ex:
            raise(ex)

    complete_path = os.path.join(hash_directory, hash_file)

    fh =  open(complete_path, *args)

    if fh:
        return fh
    else:
        return None
