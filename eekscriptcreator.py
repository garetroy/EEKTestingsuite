""""
    IMPORTANT:
        Running this file assumes that you are in a similar directory structure
        that follows

        ../Visit
        |
        |-testingfolder/eekscriptcreator.py [assuming that you have all other
        |-needed files in this directory as well]
        |
        |-src/
        |
        |-etc...

    EEKScript creator
    Author: Garett Roberts

    This script will create an eek script. Run it in the same directory you want
    to run tests with eek
"""
from os import getcwd, path
class EEKScript:
    def __init__(self,database=getcwd() + "/eek.eek",debug=False):
        """
            Init assumes your database is where you are running
            the script, if not, specify the location on objects
            creation. If eek.eek is not existant/default/not a valit path, it will
            create the file in the default/given directory.

            @param:
                database [optional] - (str) the directory of your eek.eek file
                debug    [optional] - (bool) adds debug flag to engine
        """
        if not path.isfile(database):
            print("could not find eek.eek at location" + database + ".... creating at that directory")
            open(database,"a").close()

        self.database = database
        self.debug    = debug;

    def __str__(self):
        """
            Returns the string representation, showing the location of the database
            it is pointint to is
        """
        return "EEK database is pointed at " + str(self.database) + '\n'

    def removeExit(self):
        """
            Removes all exit() from the file, this way when we append, it's not
            for nothing.
        """
        runeekdir = getcwd() + "/runeek.py"
        if not path.isfile(runeekdir):
            f = open(getcwd() + "/runeek.py",'w')
            f.write('from subprocess import call\n')
            f.write('OpenDatabase("' + str(self.database) + '")\n')
            f.write('CloseComputeEngine()\n')
            f.close()
            return

        f = open(runeekdir, 'r')
        file_array = f.readlines()
        f.close()
        for i in file_array:
            if "exit()\n" == i:
                file_array.remove(i)

        f = open(runeekdir,'w')
        f.writelines(file_array)
        f.close()

    def appendToScript(self,weakscaling,blocks=1,cells=100,threads=1,loc=""):
        """
            Appends to runeek.py script with te corresponding options..

            @params:
                weakscaling        - (bool) if we want weakscaling
                blocks [optonal]   - (int) number of blocks we desire
                cells [optional]   - (int) number of cells wanted
                threads [optional] - (int) number of threads wanted
                loc [optional]     - (str) location we want to store timings
        """
        self.removeExit()
        f = open(getcwd() + "/runeek.py", 'a+')
        if(self.debug):
            f.write('OpenComputeEngine("localhost",("-thread","' + str(threads) +\
                    '","-withhold-timing-output","-debug","5"))\n')
        else:
            f.write('OpenComputeEngine("localhost",("-thread","' + str(threads) +\
                    '","-withhold-timing-output"))\n')
        f.write('opts = GetDefaultFileOpenOptions("EEK")\n')
        f.write('opts["cells"] = ' + str(cells) + '\n')
        if not weakscaling: #if weakscaling, this dosen't matter
            f.write('opts["blocks"] = ' + str(blocks) + '\n')
        f.write('opts["weakscaling"] = ' + str(weakscaling) + '\n')
        f.write('SetDefaultFileOpenOptions("EEK",opts)\n')
        f.write('ReOpenDatabase("' + str(self.database) + '")\n')
        f.write('AddPlot("Contour", "temperature")\n')
        f.write('try:\n')
        f.write('  DrawPlots()\n')
        f.write('  DeleteAllPlots()\n')
        f.write('  CloseComputeEngine()\n')
        f.write('except:\n')
        #start except block#
        f.write('  print("Test thread:{} '\
                        'block:{} dim:{} weakscale:{} not successful")\n'.format(threads,\
                        blocks,cells,weakscaling))
        if loc != "" and path.isdir(loc):
            f.write('  call("mv *.timings ' + str(loc) + '", shell=True)\n')
        if self.debug:
            f.write('  call("mv *.vlog ' + str(loc) + '", shell=True)\n')
        f.write('  exit(1)\n')
        #end except block#

        if loc != "" and path.isdir(loc):
            f.write('call("mv *.timings ' + str(loc) + '", shell=True)\n')
        if self.debug:
            f.write('call("mv *.vlog ' + str(loc) + '", shell=True)\n')
        f.write('exit()\n')

    def clearScript(self):
        """
            Clears the script totally
        """
        f = open(getcwd() + "/runeek.py",'w')
        f.write('from subprocess import call\n')
        f.write('OpenDatabase("' + str(self.database) + '")\n')
        f.write('CloseComputeEngine()\n')
        f.close()

if __name__ == "__main__":
    go = EEKScript()
    go.appendToScript(False)
