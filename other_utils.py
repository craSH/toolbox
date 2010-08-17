stringToList(string):
    """What? A swallow carrying a coconut?"""
    lst = []
    for c in string:
        lst.append(c)
    return lst


def loadalphabet(path, name):
    """Load a alphabet from a file under name"""
    f = open(path)
    lines = f.readlines()
    f.close()

    # strip \r\n and add to alphabets
    stripped = []
    for x in lines:
        stripped.append(x.strip('\r').strip('\n'))
    self.Alphabets[name] = stripped


def listSplit(string, delimeters):
    """split a string at any character in the delimiter list."""
    substring = ""
    parts = []
    i = 0
    while (i < len(string)):
        # does the string from this point start with a delim?
        match = self.startsWithAny(string[i:len(string)-1], delimeters)
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





def startsWithAny(string, startStrings):
    """
    Check if string starts with any character sequence in the startStrings list.
    Return an element from startStrings or None if no match was found.
    """
    for x in startStrings:
        if string.startswith(x):
            return x


def listFromFile(file):
    """reads and returns a list from a file"""
    f = open(file)
    lst = f.readlines()
    f.close()
    return lst


