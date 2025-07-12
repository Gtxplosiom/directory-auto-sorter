import sys
import os
import shutil

class Sorter:
    def __init__(self, argv):
        self.current_dir = argv[2]
        self.argv = argv

        self.accepted_args = ["createDir", "categorySort"]

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
            case "categorySort":
                print(f"Category sorting in {self.current_dir}...")

    def createDir(self, curr_dir:str):
        items:str = os.listdir(curr_dir)

        basePath = curr_dir + '\\'

        dirs = []

        for item in items:
            ext = item.split(os.extsep)
            filepath = basePath + item

            if len(ext) > 1: # if item has filename
                if ext[1] not in dirs: # if a new filetpe doesn't have a folder, create a folder
                    os.mkdir(basePath + ext[1])
                    dirs.append(ext[1])
                
                # move file to its rightful directory
                try:
                    dest = basePath + ext[1]
                    shutil.move(filepath, dest)
                except Exception as excep:
                    print(excep)
        
if __name__ == '__main__':
    argv = sys.argv

    sorter = Sorter(argv)

    sorter.main()
