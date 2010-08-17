"""
Copyright (C) 2008 Author
Author: 
Date: 

Description: 
    Overview of the project and the problem it solves

Usage:
    How to use the module 
"""

import urlparse, string
               

def textToDict(text, record='\n', assignment=':'):
    """
    text: a string, such as a config file or HTTP headers, which is a list of key value pairs.
    record: the delimiter between records in the list (such as newline or comma)
    assignement: the assignment delimiter between key value pairs (such as k=v or k:v)
    return: a dictionary represntation of the data

    Example:

        "Accept-Encoding: gzip,deflate 
         Keep-Alive: 300
         Accept: text/html"

    becomes:
        
        {'Accept-Encoding': 'gzip,deflate', 'Keep-Alive': '300', 'Accept': 'text/html'}
    """

    d = {}
    for section in text.split(record):
            kv = section.split(assignment)
            if len(kv)>1:
                d[kv[0]]=kv[1]
    return d

def dictToText(dictionary, record='\n', assignment=': '):
    """
    reverse the operation of textToDict
    """
    text = ""
    for (k,v) in dictionary.iteritems():
        text += assignment.join((str(k),str(v))) + record
    return text





def splitHTTPMessage(message):
    # split headers from body, try both possible line endings
    msgParts = message.split('\r\n\r\n')
    if not len(msgParts) > 1:
        msgParts = message.split('\n\n\n\n')
    body = ""
    headers = ""
    if len(msgParts) > 1:
        headers = msgParts[0]
        body = "".join(msgParts[1:])
    return (headers, body)



def urlToGet(url):
    """take the URL and return the host, port, and GET request"""
    scheme, host, path, params, query, fragment = urlparse.urlparse(url)
    try:
        host, port = string.split(host, ":", 1)
        port = int(port)
    except (TypeError, ValueError):
        port = 80 # default port
    if not path:
        path = "/"
    if params:
        path = path + ";" + params
    if query:
        path = path + "?" + query
    request = "GET %s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host)
    return (host, port, request)



class HttpParser:
    def __init__(self, httpText):
        # split http text headers/body and create dictionaries for headers
        self.raw = httpText
        (rawHeaders, rawBody) = splitHTTPMessage(httpText)
        self.headers = textToDict(rawHeaders, record='\n', assignment=': ')
        
        # separate first line (status or path)
        endline = self.raw.find('\n')
        firstLine = httpText[:endline].split()

        # determine verb (GET, POST, HEAD, ...) and status code if HTTP
        self.verb = firstLine[0].upper()
        if self.verb.startswith('HTTP'):
            self.status = firstLine[1]
            self.body = rawBody

        if self.verb.startswith('GET'): 
            self.path = firstLine[1]
        
        if self.verb.startswith('POST'):
            self.path = firstLine[1]
            self.body = textToDict(rawBody, record='&', assignment='=')
          

        # set verb, host, and path
        #endline = self.raw.find('\n')
        #head = self.raw[0:endline].split()
        #if len(head) > 1:
            # verb (GET, POST, etc)
            # self.verb = head[0]
            # path
            #protoSplit = head[1].split('://')
            #if len(protoSplit) > 1:
            #    pathSplit = protoSplit[1].split('/')
            #    self.host = pathSplit[0]
            #    self.path = '/'.join(pathSplit[1:len(pathSplit)])
            #else:
            #    if self.headers.has_key['Host']:
            #        self.host = self.headers['Host']
            #        self.path = protoSplit[0]




