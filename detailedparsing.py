#!/usr/bin/python3
"""
    IMPORTANT:
        Running this file assumes that you are in a similar directory structure
        that follows

        ../Visit
        |
        |-testingfolder/runtests.py [assuming that you have all other
        |-needed files in this directory as well]
        |
        |-testingfolder/TestResults/
        |
        |-src/
        |
        |-etc...

    This script parses through visit timing files in order to create a timing summary file which
    will be deposited in the directory this is ran in.

    DetailedParsing
        Authors: Garett Roberts, Amie Corso
""" 
from os import listdir, path
import re

class TimingsAnalyzer:
    
    def __init__(self,testdir="./TestResults"):
        """
            Just the initalizer. It checks to see if TestResults is populated(by checking top level
            directories and also checks to see if testdir is a valid path

            @param:
                testdir - (str) A string with the path to the TestResults file
        """
        self.testdir    = testdir
        self.filebuff   = []
        self.threaddirs = sorted([("./TestResults/" + i) for i in \
            listdir(self.testdir) if "thread" in i], \
            key = lambda x: int(re.search(r'\d+', x).group()))

        #checking path validity
        if(len(self.threaddirs) == 0 or not path.isdir(self.testdir)):
            print("./TestResults dosen't exist or it is empty")
            exit()

        #header
        self.filebuff.append("{0:7} {1:8} {2:4} {3:11} {4:11} {5:11} {6:12} {7:10} {8:10}\n"\
                            .format("Threads","Blocks","Dims","OverallTime",\
                            "NumContours","MinContour","MaxContour","Expected",\
                            "Deviation"))

    def scrubTimings(self,files,threadnum,blocks):
        """
            Finds the amount of contour filters used, the max times of the contours, and the overalltime
            it took to run the filters. Puts error in contours if paramters were not run.
            
            @param:
                files     - [str] All the timings files in the desired location"
                threadnum - (str) the number of threads
                blocks    - (str) number of blocks

            @returns:
                (str/int,str/int,int,str/int) - A tuple with the corresponding
                        number of contours, max number of contours,
                        min number of contours, and overalltime
        """ 
        totalcontours    = 0
        maxcontours      = 0
        mincontours      = 10000
        overalltime      = 0
        
        for f in files:
            contours = 0
            openfile = open(f,"r")
            for line in openfile:
                if "avtContourFilter::ExecuteDataTree_VTK" in line:
                    #Get individual contour times, convert to float, add to totaltime
                    time          = float(re.findall( r'\d+\.*\d*', line)[0])
                    contours      += 1
                    totalcontours += 1
    
                if "avtContourFilter took" in line:
                    overalltime = float(re.findall( r'\d+\.*\d*', line)[0]) 

            openfile.close()

            if contours > maxcontours:
                maxcontours = contours
            
            if contours < mincontours:
                mincontours = contours
            
        if overalltime == 0:
            totalcontours = "error"
            mincontours   = "N/A"
            maxcontours   = "N/A"

        return (totalcontours,maxcontours,overalltime,mincontours)

    def expectedTimes(self,threadnum,blocks,contours,mincontours,maxcontours):
        """
            This takes in information about the contours and the number of threads
            and returns a tuple withe strings correlating to the expected amount
            of contours preformed from a single thread and if it was within
            a reasonable threshold.
        
            @params:
                threadnum   - (int) number of threads
                blocks      - (int) number of blocks
                contours    - (int) number of contours we are working with
                mincontours - (int) the minimum amount of contours from a thread
                maxcontorus - (int) the maximum amount of contours from a thread
            
            @returns:
                (float,str) -  returns the expected amount of contours/thread and
                             if the max/min were in a reasonable threshold
        """
        #TEMPORARY? INSTEAD OF REASONABLE THREASHOLD RETURNING THREADNUM-MAXC

        expectation = float(blocks/threadnum)
        deviation   = abs(maxcontours-expectation)

        return (expectation,deviation)
        
        
    def grabTimings(self):
        """
            Walks through all of the sub-directories and then parses them and appends the useful
            information to the filebuff
        """
        for threaddir in self.threaddirs:
            threadnum = threaddir.split("_")[1]#current threadnum
            blocks = sorted([(threaddir + "/" + block) for block in listdir(threaddir)])
            for blockdir in blocks:
                blocknum = blockdir.split("_")[2]#current blocknum
                dims = sorted([(blockdir + "/" + dim) for dim in listdir(blockdir)])
                for dimdir in dims:
                    contour = 0 #total amount of contours
                    dimnum  = dimdir.split("_")[4]#current dimension
                    line    = "{0:^7} {1:^8} {2:^4}".format(threadnum,blocknum,dimnum) #this is our line we will output to filebuff
                    files   = sorted([(dimdir + "/" + f) for f in listdir(dimdir) if "engine_serThr" in f])
                    times   = self.scrubTimings(files,threadnum,blocknum)

                    if times[0] != "error" and threadnum != blocknum and blocknum != "nthreads":
                        expected = self.expectedTimes(int(threadnum),int(blocknum),\
                                times[0],times[3],times[1])
                    else:
                        expected = (0,0)

                    line    += " {0:^9.6f}     {1:^11} {2:^11} {3:^11} {4:^7.3f} {5:^7.3f}\n"\
                                .format(times[2],times[0],times[3],times[1],\
                                        expected[0],expected[1])
                    
                    self.filebuff.append(line)

    def outputTimings(self):
        """
            Outputs the filebuff to a file TimingSummary
        """
        f = open("TimingsSummary","w")
        for line in self.filebuff:
            f.write(line)    
        f.close()

    def default(self):
        """
            Runs the default configuration
        """
        self.grabTimings()
        self.outputTimings() 
         

if __name__ == '__main__':
    k = TimingsAnalyzer()
    k.grabTimings()
    k.outputTimings()
