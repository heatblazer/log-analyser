import os


class Utils:

    @staticmethod
    def get_filesr(dirName, opt=None):
            listOfFile = os.listdir(dirName)
            allFiles = list()
            for entry in listOfFile:            
                fullPath = os.path.join(dirName, entry)                    
                if os.path.isdir(fullPath):
                    allFiles = allFiles + Utils.get_filesr(fullPath, opt)
                else:
                    if opt is not None and opt(fullPath) is False:
                        allFiles.append(fullPath)
                    elif opt is None:
                        allFiles.append(fullPath)
                    
            return allFiles

    @staticmethod
    def unix():
        return os.name == "posix"
