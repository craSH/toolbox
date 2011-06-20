import sys, traceback, time, os


def sha1sum(string):
    """return the SHA1 sum of the param string"""
    import sha
    sha1 = sha.sha(string)
    return sha1.hexdigest()

def intArrayToString(intArray):
    """convert an array of integers to a space delimited string"""
    string = ""
    for num in intArray:
        string += str(num) + " "
    return string

def stringToIntArray(string):
    """convert a space delimited string of integers into an array of integers"""
    intArray = []
    for num in string.split():
        intArray.append(int(num))
    return intArray



def getFileNamesRecursive(directory):
    """crawl directory structure recursively and return list of all files"""
    filenames = [] 
    # walk email directory and create list of emails filenames to fuzz
    for root, dirs, files in os.walk(directory):
        for name in files:
            filenames.append(os.path.join(root, name))
    return filenames


def loadFile(filename):
    """open filename read only and return the contents as a string"""
    # todo: modify so it can optionally read/return binary
    f = open(filename, 'r')
    lines = f.readlines()
    text = "".join(lines)
    f.close()
    return text

def intFromString(string, default=None):
        """ get integer value from attribute dictionary or return default"""
        val = default
        if string:
                try:
                        val = int(string)
                except ValueError, TypeError:
                        print str(val), " is not a valid integer"
                        val = default
        return val

def escapeChars(text):
        """
        Escape any metacharacters in a string. 
        """
        t = text
        t = t.replace('\\r','\r')
        t = t.replace('\\n','\n')
        t = t.replace('\\t','\t')
        return t

def postBodyToDict(s):
        d = {}
        for x in s.split('&'):
                kv = x.split('=')
                d[kv[0]]=kv[1]
        return d

def listSplit(string, delimeters): 
    """
    split a string at any character in the delimiter list.
    returns a list containing the substring parts
    """ 
    substring = "" 
    parts = [] 
    i = 0 
    while (i < len(string)): 
        # does the string from this point start with a delim? 
        match = startsWithAny(string[i:len(string)-1], delimeters) 
        if match:
            # add substring then delim to the list
            if substring:
                parts.append(substring)
                substring = ''
            parts.append(match)
            i += len(match)
        else:
            substring += string[i]
            i += 1
    if substring:
        parts.append(substring)
    return parts

def slice(string, start, fin, startpos=0, endpos=-1):
    """
    Returns the contents between the substrings start and fin.
    Specify startpos/endpos to start/end at pos other than 0/-1 (slice notation) in string.
    Return None if substring does not exist or start/end positions are invalid
    """

    slice_start = None
    slice_end = None
    result = None

    try:
        slice_start = string.index(start, startpos, endpos) + len(start) if start else 0
        slice_end = string.index(fin, startpos + slice_start, endpos) if fin else len(string)
        result = string[slice_start:slice_end]
    except ValueError:
        pass

    return result

def startsWithAny(string, startStrings):
    """
    Check if string starts with any character sequence in the startStrings list.
    Return an element from startStrings or None if no match was found.
    """
    for x in startStrings:
        if string.startswith(x):
            return x

def printList(list):
    index = 0
    for item in list:
        print "%s\t%s" % (index, item)
        index +=1

def time():
    """return the local time as a string"""
    import time
    return time.strftime("%Y%b%d_%H%M%S")


def displit(x, acc=[]):
    return displit(x[2:], acc+[(x[:2])]) if x else acc
