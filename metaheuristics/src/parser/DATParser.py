import os
import re

class DATAttributes():
    pass

class DATParser():

    @staticmethod
    def _tryParse(attr):
        # Parse as a integer
        try:
            return (int(attr))
        except ValueError:
            pass

        # Parse as float
        try:
            return (float(attr))
        except ValueError:
            pass

        # Parse as boolean
        if (attr in ['True', 'true', 'TRUE', 'T', 't']): return (True)
        elif (attr in ['False', 'false', 'FALSE', 'F', 'f']): return (False)

        return (attr)

    @staticmethod
    def _openFile(filePath):
        if(not os.path.exists(filePath)):
            raise Exception('The file (%s) does not exist' % filePath)
        return(open(filePath, 'r'))

    @staticmethod
    def parse(filePath):
        
        ## We change 'pass' name to 'passengers' ##

        """
        file = open(filePath,'r')
        filedata = file.read()
        file.close()

        filedata = filedata.replace('pass=', 'passengers=')
        filedata = filedata.replace('_max=', 'maxi=')

        file = open(filePath, 'w')
        file.write(filedata)
        file.close()
        """

        fileHandler = DATParser._openFile(filePath)
        fileContent = fileHandler.read()
        fileHandler.close()

        datAttr = DATAttributes()

        # parse scalar attributes
        pattern = re.compile(
            r'^[\s]*([a-zA-Z][\w]*)[\s]*\=[\s]*([\w\/\.\-]+)[\s]*\;', re.M)
        entries = pattern.findall(fileContent)
        for entry in entries:
            datAttr.__dict__[entry[0]] = DATParser._tryParse(entry[1])

        # parse 1-dimension vector attributes
        pattern = re.compile(
            r'^[\s]*([a-zA-Z][\w]*)[\s]*\=[\s]*\[[\s]*(([\w\/\.\-]+[\s]*)+)\][\s]*\;', re.M)
        entries = pattern.findall(fileContent)
        for entry in entries:
            pattern2 = re.compile(r'([\w\/\.]+)[\s]*')
            values = pattern2.findall(entry[1])
            datAttr.__dict__[entry[0]] = map(DATParser._tryParse, values)

        return(datAttr)
