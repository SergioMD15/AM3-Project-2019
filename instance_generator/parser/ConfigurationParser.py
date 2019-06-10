import os

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def openFile(filePath):
        if (not os.path.exists(filePath)):
            raise Exception('The file (%s) could not be found' % filePath)
        return (open(filePath, 'r'))


class AttrContainer(object):
    pass


class ConfigurationParser:

    attrs = AttrContainer();

    def parse(self, filePath):
        # Open file
        opened_file = openFile(filePath)

        # Try to parse all non-white lines
        try:
            for line in nonblank_lines(opened_file):
                self.attrs.__dict__[line.split('=')[0]] = self.parseAttribute(line.split('=')[1].replace(';',''))
        finally:
            opened_file.close()
            return self.attrs

    def parseAttribute(self, attr):
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
