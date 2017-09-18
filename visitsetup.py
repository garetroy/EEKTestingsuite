#!/usr/bin/python3
"""
    IMPORTANT:
        Running this file assumes that you are in a similar directory structure
        that follows (and you have all the ModifiedSrc files)

        ../Visit
        |
        |-testingfolder/setup.py [assuming that you have all other needed files
        |-in this directory as well]
        |
        |-src/ [optional]
        |
        |-etc...

    VisitSetup
        Author: Garett Roberts
        This program can build Visit and add additional options to the build.
        It can be run as a script, or be used as a class for modularity.

"""
from subprocess import call
from os import path, getcwd, chdir, listdir
from sys import argv

class Setup:
    def __init__(self,visitsrc,cmake,default=True,backup=False):
        """
            This function verifies that all the files we need are present
            and then runs through the default patch depending on default
            @params:
                visitsrc - (str) location of visit's src file
                cmake    - (str) location of the cmake file
                default  - (bool) [optional] will just add all patches manually
                backup   - (bool) [optional] sets the default for backing up files
                            before replacing them
        """
        self.visitsrc   = visitsrc
        self.modifypath = getcwd() + "/ModifiedSrc/"
        self.backup     = backup
        self.cmake      = cmake

        if not self.verifyModifiedFiles():
            print("--Above are missing files, please locate and move them to "\
                    + getcwd() + "/ModifiedSrc/ in order to run setup properly")
            exit()

        if default:
            self.default()

    def buildVisit(self,mesa=False,thirdpartypath=""):
        """
            This function builds visit. It will typically be called, then 
            the patch will be applied

            @params:
                mesa           - (bool) Adds mesa to the build if True
                thirdpartypath - (str) The path to the third party 
        """
        currdir = getcwd()
        chdir("../")
        buildvisiturl = "http://visit.ilight.com/svn/visit/trunk/src/svn_b"\
        +"in/build_visit"
        #nc means "no clobber" (dosen't download if file exists already 
        print("Grabbing build_visit script")
        call("wget -nc " + buildvisiturl, shell=True)
        try:
            print("Changing build_visit to executable")
            call("chmod +x build_visit", shell=True)
        except:
            print("Could not make build_visit executable")
            exit()

        flags = "--silo --netcdf --hdf5 --szip --boost --makeflags -j8"

        if mesa:
            flags += " --mesa "

        if thirdpartypath != "":
            flags += "--thirdparty-path " + thirdpartypath

        print("Building visit with flags: " + flags)
        if call("./build_visit " + flags, shell=True) < 0:
            print("BUILDING VISIT FAILED, Check logs")
            exit()
        chdir(currdir)


    def verifyModifiedFiles(self):
        """
            This function verifies that most of the files we want are there..
            it doesn't verify that all EEK files are in the EEK folder..
            so watch out!
        """
        desiredfiles = ["TimingsManager.h","TimingsManager.C","VisItInit.C",\
                        "main.C","VisItControlInterfaceRuntime.C","CMakeLists.txt"]
        filesexist   = True

        for i in desiredfiles:
            lookingat = self.modifypath + i
            if not path.isfile(lookingat):
                filesexist = False
                print(lookingat + " NOT FOUND")

        lookingat = self.modifypath + "EEK/"
        if not path.isdir(lookingat):
            filesexist = False
            print(lookingat)

        return filesexist

    def replaceLineWith(self,line,item,filepath):
        '''
            This function replaces the given item at the given line within
            the given filepath

            @param:
                line - (int) line number we want to replace
                item - (str) line we want to replace with
                filepath - (str) filepath
        '''
        file_arr  = [] #Puts each line in a position of the array

        f = open(filepath,'r')
        for i in f.readlines():
            file_arr.append(i) #appends each line to array

        f.close()

        file_arr[line] = item 
        f = open(filepath,'w')
        f.writelines(file_arr) #rewrite the modified file_arr to file
        f.close()

    def backupFile(self,filepath):
            '''
                This function takes a file path, and makes a backup of the 
                given file by appending a number to the end of it

                @param:
                    filepath - (string) A path that ends in a file..
            '''
            if(not self.backup):
                return

            extensions = "C cxx h e"

            if(not path.isfile(filepath)): #if non-existant... don't back up
                return

            condbreak = False
            number    = 1
            while(path.isfile(filepath)): #find non-existant file
                if(filepath[-1] in extensions):
                    filepath = filepath + str(number)
                    continue;

                if(number == 9):
                    number    = 1 #replaces 1
                    condbreak = True
                else:
                    number += 1;

                filepath = filepath[:-1]
                filepath += str(number)

                if(condbreak):
                    break;

            print("Backing up to " + filepath)
            call(["cp",filepath[:-1],filepath])

    def replaceTimingManagers(self):
        """
            Replaces the timings managers.
            This adds in a new TimingsManager to [dest to src]/common/misc/
            This is for multithreaded timing files
            You can grab them at
            http://visit.ilight.com/svn/visit/branches/hrchilds/Phi/src/
            common/misc/TimingsManager.[C/h]
            (Should be avaiable with tar)
        """
        print("Replacing TimingManagers at location src/common/misc/")
        timing_man  = self.modifypath + "TimingsManager.h"
        replace_tim = self.visitsrc + "/common/misc/TimingsManager.h"
        self.backupFile(replace_tim)
        call(["cp",timing_man,self.visitsrc+"/common/misc/"])

        timing_man  = timing_man[:-1] + "C"
        replace_tim = replace_tim[:-1] + "C"
        self.backupFile(replace_tim)
        call(["cp",timing_man,self.visitsrc+"/common/misc/"])

    def replaceVisItInit(self):
        """
            Replaces the VisItInit file to [dest to src]/common/misc
            This is for multithreaded timings managers and engine replacement
            You can grab this file at
            http://visit.ilight.com/svn/visit/branches/hrchilds/Phi/src/
            common/misc/VisItInit.C
            (Should be avaiable with tar)
        """
        print("Replacing VisItInit.C at location src/common/misc/") 
        visit       = self.modifypath + "VisItInit.C"
        replace_vis = self.visitsrc + "/common/misc/VisItInit.C"
        self.backupFile(replace_vis)
        call(["cp",visit,self.visitsrc+"/common/misc/"])

    def replaceMain(self):
        """
            Replace the engine's main, typically for the logtime feature.
            Logtime is a feature that allows us to specify the dest of the
            timings files 
            Replaces to [dest to src]/engine/main/
            This file was made by students and not avaiable online
            (Should be avaiable with tar)
        """
        print("Replacing main.C at location src/engine/main/")
        main_file    = self.modifypath + "main.C"
        replace_file = self.visitsrc  + "/engine/main/main.C"
        self.backupFile(replace_file)
        call(["cp",main_file,self.visitsrc + "/engine/main"])

    def replaceVControlIntf(self):
        """
            Replace the VisItControlInterfaceRuntime, typically for the logtime
            feature. (see replaceMain)
            Replaces to [dest to src]/sim/V2/runtime/
            Student made file, not available online
            (Should be avaiable with tar)
        """
        replace_control = self.visitsrc + "/sim/V2/runtime/"
        print("Replacing VisItControlInterfaceRuntime.C at location " + \
                replace_control[2:])
        control_init    = self.modifypath + "VisItControlInterfaceRuntime.C"
        replace_control += "VisItControlInterfaceRuntime.C"
        self.backupFile(replace_control)
        call(["cp",control_init,self.visitsrc + "/sim/V2/runtime/"])


    def addEEK(self):
        """
            Adds the EEK database to Visit
            EEK/ is placed in [dest to src]/databases/
            CMakeLists.txt is placed in the same location
            Both have student made files, not available online
            (Should be avaiable with tar)
        """
        print("Adding EEK")
        eek_path  = self.modifypath + "EEK/"
        cmake_eek = self.modifypath + "CMakeLists.txt"
        data_path = self.visitsrc + "/databases/"
        call(["cp","-r",eek_path,data_path])
        call(["cp",cmake_eek,data_path])

    def turningOnThreads(self):
        """
            Turns threading on for Visit (ONLY TURNS ON CMAKE and Contour)
            Location is at ../*.cmake, turning the THREADED option to ON
            Threaded for cmake is turned on at [dest to src]/avt/Filters/
            avtContourFilter.h
        """
        print("Turning CMake thread option ON and copying to config-site")
        self.backupFile(self.cmake)
        desiredlin = "VISIT_OPTION_DEFAULT(VISIT_THREAD ON TYPE BOOL)\n"
        copylocato = self.visitsrc + "/config-site/"
        self.replaceLineWith(25,desiredlin,self.cmake)
        call(["cp",self.cmake,copylocato])

        print("Adding ThreadSafe method to Contour") 
        filepath   = self.visitsrc + "/avt/Filters/avtContourFilter.h"
        desiredlin = "\tvirtual bool               ThreadSafe(void) { " \
                        + "return(true); };  \n"
        self.backupFile(filepath)
        self.replaceLineWith(118,desiredlin,filepath)
        call(["touch",filepath])

    def makeSrc(self):
        """
            Makes for Visit
        """
        currpath = getcwd()
        chdir(self.visitsrc)
        print("Make cleaning")
        call("make clean", shell=True)
        print("Making")
        makecall = call(("make -j8 1>>" + currpath + "/makelogs" + \
                        " 2>&1" ), shell=True)
        if makecall != 0:
            print("MAKE FAILED, check makelogs for more info")
            exit()
        chdir(currpath)

    def default(self):
        """
            Apply all patches available
        """
        self.replaceTimingManagers()
        self.replaceVisItInit()
        self.replaceMain()
        self.replaceVControlIntf()
        self.addEEK()
        self.turningOnThreads()
        self.makeSrc()

if __name__ == "__main__":
    if len(argv) == 1:
            print("a python script for setting up Visit")
            print("Usage: (visit src path) (cmakefilePath) [flags]")
            print("Use --help to get more info")
            exit()

    flag_setup = False

    if len(argv) > 1:
        if "--help" in argv or "-help" in argv or "-h" in argv: 
            print("a python script for setting up Visit")
            print("Usage: (visit src path) (cmakefilePath) [flags]")

            print("-h, --help")
            print("-t, --threads turns on threads, only turns on threading in"\
                 + "cmake and avtContourFilter currently")
            print("-e, --eek adds eeks to Visit")
            print("-m, --timingmanager adds multithreaded timings mangers")
            print("-b, --backup backs-up files being replaced")
            print("-d, --default runs all patches, by default already on, used"\
                    + " for -i")

            print()
            print("-i, --build from scratch will only build visit, will not apply any options by default")
            print("    --thirdparty-path allows you to use thirdparty with -i")
            print("    --mesa adds mesa to the -i build")
            exit()

        scratch        = False
        thirdpartypath = ""
        visitsrc       = ""
        cmakepath      = ""

        if "--build" in argv or "-build" in argv or "-i" in argv:
            scratch = True
            mesa    = False

            if "--mesa" in argv:
                mesa = True

            if "--thirdparty-path" in argv:
                i = argv.index("--thirdparty-path") + 1
                if path.isdir(argv[i]):
                    s = Setup("","",False)
                    s.buildVisit(mesa,thirdpartypath=argv[i])
                else:
                    print(argv[i] + " is not valid directory for thirdparty")
                    exit()
            else:
                s = Setup("","",False)
                s.buildVisit(mesa)

            visitsrc = "../src"
            #CAREFUL HERE, THIS GRABS THE FIRST CMAKE IT FINDS IN ../
            for i in listdir("../"):
                if ".cmake" in i:
                    cmakepath = "../" + str(i)
                    break;
        else:
            visitsrc = argv[1]
            try:
                cmakepath = argv[2]
            except:
                print("a python script for setting up Visit")
                print("Usage: (visit src path) (cmakefilePath) [flags]")
                print("Use --help to get more info")
                exit()

        if not path.isdir(visitsrc):
            print(str(visitsrc) + " is not a valid path to src")
            exit()

        if not path.isfile(cmakepath):
            print(str(cmakepath) + " is not a valid path to cmake")
            exit()

        if len(argv) == 3:
            print("Setting up Defualt Visit Enviroment")
            Setup(visitsrc,cmakepath)
            print("Setup Complete")
            exit()

        if "--backup" in argv or "-backup" in argv or "-b" in argv:
            s = Setup(visitsrc,cmakepath,default=False,backup=True)
        else:
            s = Setup(visitsrc,cmakepath,default=False)

        if "--default" in argv or "-default" in argv or "-d" in argv:
            s.default()
            exit()

        if "--threads" in argv or "-threads" in argv or "-t" in argv:
            s.turningOnThreads()
            flag_setup = True

        if "--eek" in argv or "-eek" in argv or "-e" in argv:
            s.addEEK()
            flag_setup = True

        if "--timingmanager" in argv or "-timingmanager" in argv or "-m" in argv:
            s.replaceTimingManagers()
            s.replaceVisItInit()
            s.replaceMain()
            s.replaceVControlIntf()
            flag_setup = True

        if flag_setup:
            s.makeSrc()

