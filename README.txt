This is a testing suite that tests (VisIt)[https://wci.llnl.gov/simulation/computer-codes/visit/]
using a dataset called EEK

Authors:
    Garett Roberts
    Amie Corso

Welcome to the EEK Testing suite!

First off, most of these scripts default assumptions are on a specific directory structure.. This is how it should look.

Visit/
    |
    |
    |--Testing/*
    |
    |--src/
    |
    |--etc..


Testing is where you should be reading this README right now. It's okay if you only have the Testing folder right now, as
there is a script that will set up visit for you. (Which you can jump down to the install portion if that's what you need)

If you have everything patched and ready to go. You can just go ahead and jump down to the testing portion.

More in-depth details of the programs and what they do will be in doc.txt

Lastly, make sure that all the .py files are chmod +x 'd (or alternativly you could just use "python3 <script>" to run the scripts

REQUIRED FILES:
    Testing/
        |
        |--visitsetup.py
        |
        |--eekscriptcreator.py
        |
        |--detailedparsing.py
        |
        |--runtests.py
        |
        |--ModifiedSrc/
                |
                |--TimingsManager.h/C
                |
                |--CMakeLists.txt
                |
                |--EEK/

INSTALL:
    Files used: visitsetup.py
    At any point, you can check your options to install/patch by typing in ./visitsetup.py -h

    To install visit, and to be safe, make sure that you don't have any .cmake files or src/ files in the parent directory 
    of the testing directory.

    The command to invoke an installation of visit is:
        ./visitsetup.py -i

    This will download the visit script and install most dependancies that you will need. There are other options
    as well such as --mesa which will install mesa (required for cori and non-windowed testing) and --thirdparty-path [path]
    which is reccommended so that you don't have to keep installing thirdparties over and over again. I typically put my
    third party path in my home directory. If you don't want to have to manually patch everything, and have it all do it
    at one time put a -d in the command line arguments.

    CORI:
        If you are installing this on cori, please make your Visit directory in the $SCRATCH directory
        You may need to setup some enviroment variables (such as tbb/python/knlswapping... etc)

    NOTE:
        Mesa sometimes has a hard time installing around the time of writing this (07/20/17). You may have to play around with it
        or keep attempting to install it.


PATCHING:
    Files used: visitsetup.py
    At any point, you can check your options to install/patch by typing in ./visitsetup.py -h

    To patch your current version of Visit (if you didn't install while using -d with the visitsetup script)
    you will need to provide the cmake file and the location of the src file.  

    There are other options, but to have it just patch to install for eek testing, go ahead and run the 
    following command.
        ./visitsetup.py (src path) (cmake file path)

    This will take some time, as it has to replace things (which will be explained in doc.txt), make clean, then make all over again.

    CORI:
        Make sure that you are using the right node's cmake file. (I usually just copy the one I have to the name of the cori node)

TESTING:
    Files used: runtests.py (requires all files)
    This is the actual script we will want to be using for the testing parameters. 

    To run testing:
        ./runtests.py

    At the bottom of the file is an example of how to setup the script. You will want to set up those parameters to what you desire to test.
    If at any point the visit script fails to run. It will move the error logs to the corresponding folder in TestResults, tell you it was unsuccessful
    and exit out (still parses the results). Any tests that were supposed to run after the errenous test will have to be re-scheduled. (Previous successful
    tests will be okay). You can check to see which were successful and what parameters caused an error by looking at the TimingSummary file.

    NOTES:
        Sometimes it fails initially.. Just re-run it and you should be okay.
        If on cori, as previously stated, please make sure your current Visit folder is in the $SCRATCH directory and then when creating the TestEEK object
        you can turn cori=True and it will run it for you on cori by creating a temporary bash script in the current directory

PARSING:
    Files used: detailedparsing.py
    To parse all the timings in TestResults

    To run parser:
        ./detailedparsing.py

    This will produce a file called TimingsSummary in the current directory which contains the summary of the test results
