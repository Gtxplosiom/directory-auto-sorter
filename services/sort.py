import sys
import os

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
                self.createDir()
            case "categorySort":
                print(f"Category sorting in {self.current_dir}...")

    def createDir(self):
        items = os.listdir(self.current_dir)
        print(items)
        
if __name__ == '__main__':
    argv = sys.argv

    sorter = Sorter(argv)

    sorter.main()
