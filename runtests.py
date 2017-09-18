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
        |-src/
        |
        |-etc...

        If you are here to change the paramaters of the script such as thread
        count, block dims, or block sizes... Go to the bottom of the script!

    EEKTests
        Author:Garett Roberts, Amie Corso

        This program is expected to be used as a script, but made modular
        in-case
"""
from os import mkdir, chdir, path, getcwd
from sys import argv
from subprocess import call
import eekscriptcreator
import detailedparsing

class TestEEK:
    def __init__(self,visitsrc="../src",backup=False,cori=False):
        """
        @params:
            visitsrc - (str) The location of Visit's src
            backup   - (bool) [optional] Will backup files before overwriting them
            cori     - (bool) [optional] Let's the script know it's running on cori
                        'use slurm/batch'
        """
        if not path.isdir(visitsrc):
            print(str(visitsrc) + " is not a valid path")
            exit()

        self.visitsrc  = visitsrc
        self.backup    = backup
        self.cori      = cori
        self.blocks    = []
        self.blockdims = []
        self.threads   = []

    def loadLists(self,blocks,blockdims,threads):
        """
            Loads the given lists into the object.

            @params:
                blocks    - list(int/str) the blocks we want to add to our object
                blockdims - list(int) the size of block dims we want to add
                threads   - list(int) the amount of threads we want to run every run
        """
        for i in blocks:
            self.blocks.append(i)

        for i in blockdims:
            self.blockdims.append(i)

        for i in threads:
            self.threads.append(i)

    def checkExistanceOfItems(self):
        """
            Makes sure there are items loaded up into blocks,blockdims,threads
        """
        if not ((len(self.blocks) > 0) and (len(self.blockdims) > 0) and \
                (len(self.threads) > 0)):
            print("You did not load up blocks, blockdims, or threads")
            exit()
        print("Found paramaters to test.")
        print("Threads: ", end="")
        print(','.join(map(str, self.threads)))
        print("Blocks: ", end="")
        print(','.join(map(str, self.blocks)))
        print("Block dimensions: ", end="")
        print(','.join(map(str, self.blockdims)))
        return

    def createStructure(self):
        """
            This function creates the testing directory structure, rooted at 
            "TestResults", then  organized first  by #blocks (static vs. dynamic),
            then by nCells, then by numThreads.  It checks to see if the directory
            is present, if not it creates it.

            Note: does NOT put an eek.eek (or parser) file in each directory -
            all tests can use a single eek.eek and single parser file located at same
            location as this testing script.
        """
        dir_name = getcwd() + "/TestResults"
        if not path.exists(dir_name):
            mkdir(dir_name) 
            chdir(dir_name)
            # initialize summary file and write header
            summary_file = open("timingSummary", "a")
            summary_file.write("Blocks  Load   Threads  Time\n")
            summary_file.close()

        for k in self.threads:
            thread_dir_name = dir_name + "/" + "thread_"+\
                str(k)
            if not path.isdir(thread_dir_name):
                mkdir(thread_dir_name)

            for i in self.blocks:
                blocks_dir_name = thread_dir_name + "/" + "blocks_" + str(i)
                if not path.isdir(blocks_dir_name):
                    mkdir(blocks_dir_name)

                for j  in self.blockdims:
                    block_dim_dir_name = blocks_dir_name + "/" + "block_dim_" + str(j)
                    if not path.isdir(block_dim_dir_name):
                        mkdir(block_dim_dir_name)


        print("Created directory structure.")

    def createScript(self):
        """
            Creates the runeek.py script for us using the 
            blocks and blockdims we have
        """
        esc = eekscriptcreator.EEKScript(debug=True)
        esc.clearScript()
        for k in self.threads:
            for i in self.blocks:
                for j in self.blockdims:
                    if i == "nthreads":
                        loc = getcwd() + "/TestResults/thread_" + str(k) + \
                            "/blocks_nthreads/block_dim_" + str(j) + "/"
                        esc.appendToScript(True,i,j,k,loc)
                    else:
                        loc = getcwd() + "/TestResults/thread_" + str(k) \
                            + "/blocks_" + str(i) + "/block_dim_" + str(j) + "/"
                        esc.appendToScript(False,i,j,k,loc)

        print("Created script.")

    def parseAll(self):
        """
            This will start the parsing of all the files generated from the
            threads,blocks,blockdims
        """
        print("Beginning parsing.")
        a = detailedparsing.TimingsAnalyzer()
        a.default()
        print("Finished Parsing.")

    def runAllTests(self):
        """
            Runs all test configurations from our generated script per thread
        """
        print("IMPORTANT: Ignore the first parameters given by the program," \
                + "(threads,blocks,...etc) they will be changed (as you will" \
                + " see on the second paramaters) by the script")
        self.checkExistanceOfItems()
        self.createStructure()
        self.createScript()
        print("Running all tests...")
        dir_name = getcwd() + "/TestResults"
        # run visit using correct number of
        # also adds all stderr and stdio to testing_visit_log
        visit_path = self.visitsrc + "/bin/visit"
        called = 0;
        if self.cori:
            bash_command = "srun -C knl -p debug -t 00:30:00 -J VISITKNLTEST -L SCRATCH -n 1 {} -nowin -cli -s {}/runeek.py -timings".format(visit_path,getcwd())
            f = open("./runvisit.sh","w")
            f.write("#!/bin/bash\n")
            f.write(bash_command)
            f.close()
            called = call("chmod +x ./runvisit.sh",shell=True)
            if called > 0:
                print("Could not chmod +x runvisit")
                exit()
            called = call("./runvisit.sh; rm ./runvisit.sh",shell=True)
        else:
            bash_command = visit_path + " -timings -nowin -nosplash" \
            +" -cli -s " + getcwd()  + "/runeek.py"
            called = call(bash_command, shell=True)

        if called > 0:
            print("ERROR RUNNING TESTS, (try running again)")
            exit()
        print("Finished running all tests.")

    def run(self,blocks,blockdims,threads):
        """
            This runs the tests
            
            @params:
                blocks    - [int/str] the blocks we want to test
                blockdims - [int] the dims we want to test
                threads   - [int] the threads we want to test
        """
        self.loadLists(blocks,blockdims,threads)
        self.runAllTests()
        self.parseAll() 
            

if __name__ == "__main__":
    """
        This is the main part of the script... There is an example below
        "nthreads" must be in double quotes.. check to see if runeek.py script
        is setting weakscaling to True
    """
    a = TestEEK(cori=True)
    #blocks    = ["nthreads"]
    blocks    = [240]
    blockdims = [100]
    #threads   = [100]
    #threads   = [120,140,160,180,200]
    #blockdims = [46,57]
    #threads   = [102,136,137,170,204,238,272]
    #threads   = [1,16,30,32,60,64,69,69,80,90,100,110,120,130,150,170,190,200,220,225,250]
    #threads   = [220,225,250]
    #threads   = [1]
    a.run(blocks,blockdims,threads)
