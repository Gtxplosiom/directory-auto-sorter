import sys
import os
import shutil
import datetime

class Sorter:
    def __init__(self, argv):
        self.current_dir = argv[2]
        self.argv = argv

        self.accepted_args = ["createDir", "dateSort"]

    def main(self):
        active_mode = ""

        if len(self.argv) <= 2 or self.argv[1] == self.accepted_args[0]:
            active_mode = self.accepted_args[0]
        elif self.argv[1] == self.accepted_args[1]:
            active_mode = self.accepted_args[1]
        
        self.sort(active_mode)
        
    def sort(self, active_mode):
        match active_mode:
            case "createDir":
                print(f"Default sorting in {self.current_dir}...")
                self.createDir(self.current_dir)
            case "dateSort":
                print(f"Date sorting in {self.current_dir}...")
                self.dateSort(self.current_dir)

    def createDir(self, curr_dir:str):
        items:str = os.listdir(curr_dir)

        basePath = curr_dir + '\\'

        for item in items:
            ext = item.split(os.extsep)

            filepath = basePath + item

            if os.path.isdir(filepath):
                continue

            print(ext)

            if len(ext) > 1: # if item has filename
                suffix = len(ext) - 1

                # create a folder for every file and its extension but skip is exists already
                try:
                    os.mkdir(basePath + ext[suffix])
                except FileExistsError as fileExistExcep:
                    pass
                except Exception as excep:
                    print(excep)
                
                # move file to its rightful directory
                try:
                    print("moving")
                    dest = basePath + ext[suffix]
                    shutil.move(filepath, dest)
                except shutil.SameFileError as sameFileExcep:
                    print(sameFileExcep)
                except Exception as excep:
                    print(excep)
    
    def dateSort(self, currDir:str):
        items:str = os.listdir(currDir)

        basePath = currDir + '\\'

        for item in items:
            filePath = basePath + item

            if (os.path.isdir(filePath)):
                continue

            # convert to more human redable format
            lastMod = os.path.getmtime(filePath)
            lastMod = datetime.datetime.fromtimestamp(lastMod)

            # convert datetime to string
            lastModStr = f"{lastMod}".split()
            lastModDate = lastModStr[0]

            # create dir for a file date
            try:
                os.mkdir(basePath + lastModDate)
            except FileExistsError as fileExistExcep:
                pass
            except Exception as excep:
                print(excep)

            # move file to the date specified folder
            try:
                dest = basePath + lastModDate
                shutil.move(filePath, dest)
            except shutil.SameFileError as sameFileExcep:
                print(sameFileExcep)
            except Exception as excep:
                print(excep)
        
if __name__ == '__main__':
    argv = sys.argv

    sorter = Sorter(argv)

    sorter.main()
