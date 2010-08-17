import socket, toolbox, random, os, time

class Fuzzer:
    """
    Encapsulates the basic funtionality of a fuzzer. Overload the following methods:
      send()
      next()
      finish()
    """

    def __init__(self, baseLogDir="/tmp", verbose=False, delay=0):
        self.logs = []
        self.serialCount = 0 # number of times we have serialized
        self.baseLogDir = baseLogDir
        self.metaLogFileName = "fuzzResultsLog.txt"
        self.verbose = verbose
        self.delay = delay

    def send(self, data):
        """overload this: send data packet to host"""
   
    def next(self):
        """overload this: return the next fuzzed data packet"""

    def finish(self):
        """overload this: run after fuzzing completes"""

    def fuzz(self):
        """ given an itterable object, send each and log the result """
        self.logFileSetup(self.baseLogDir)
        packet = self.next()
        while packet:
            response = self.send(packet)
            self.log(packet, response)
            if len(self.logs) % 100 == 0:
                self.serializeAndRotateLogFiles()
            time.sleep(self.delay)
            packet = self.next()
        self.serializeAndRotateLogFiles()
        self.finish()

    def log(self, request, response=None):
        """add data to log along with time, sequence, hash, and other metadata"""
        reqSha = toolbox.sha1sum(request)
        respSha = toolbox.sha1sum(str(response))
        self.logs.append((len(self.logs), toolbox.time(), reqSha, respSha, request, response))
        if self.verbose:
            print "sha1(REQUEST): %s\tsha1(RESPONSE): %s" % (reqSha, respSha)

    def logSummary(self):
        """return string summary off fuzzing logs (index, date, hash)"""
        summary = "runIndex\tdate\tsha1sum(request)\tsha1sum(response)\n"
        for (index, date, shaData, shaResponse, data, response) in self.logs:
            summary += "%s\t%s\t%s\t%s\n" % (index, date, shaData, shaResponse)
        return summary


    def logFileSetup(self, baseLogDir):
        """ create file/directory structure for logs, do this once """
        self.logPath = os.path.join(baseLogDir, toolbox.time())
        os.makedirs(self.logPath)
        self.metaLogPath = os.path.join(self.logPath, self.metaLogFileName)
        # write header to metaLogFile
        metaLogFile = open(self.metaLogPath, "w")
        metaLogFile.write("%s\t%s\t\t%s\t\t%s\n" % ("Run", "Time", "sha1sum(Request)", "sha1sum(Response)"))
        metaLogFile.close()

    def serializeAndRotateLogFiles(self):
        """rotate the log files so no directory has more than 100 files in it
        write logs to disk with following structure:
        logBaseDir/date/metdata.txt
                        runNumGroup/runNum_request_hash
                        runNumGroup/runNum_response_hash
        """
        # create log file directory and names
        currentDirName = "%s-%s" % (self.serialCount*100, (self.serialCount+1)*100-1) # e.g. 0-99, 100-199, ...
        currentLogPath = os.path.join(self.logPath, currentDirName)
        os.makedirs(currentLogPath)
        
        # open metadata log file 
        metaLogFile = open(self.metaLogPath, "a")

        for (index, date, shaRequest, shaResponse, request, response) in self.logs:
            # save metadata to metaLogFile
            realIndex = index + self.serialCount*100
            metaLogFile.write("%s\t%s\t%s\t%s\n" % (realIndex, date, shaRequest, shaResponse))

            # save request
            requestFileName = "%s_%s_%s" % (realIndex, "request", shaRequest)
            requestFile = open(os.path.join(currentLogPath, requestFileName), "wb")
            requestFile.write(request)
            requestFile.close()

            # save response
            responseFileName = "%s_%s_%s" % (realIndex, "response", shaResponse)
            responseFile = open(os.path.join(currentLogPath, responseFileName), "wb")
            responseFile.write(str(response))
            responseFile.close()

        # cleanup, increment counter, and reset logs
        metaLogFile.close()
        self.serialCount = self.serialCount +1
        self.logs = []


