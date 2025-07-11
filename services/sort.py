import sys

class Sorter:
    def __init__(self, argv):
        self.args = argv

        self.createDir = False
        self.categorySort = False

    def main(self):
        active_args = []
        accepted_args = ["createDir", "categorySort"]

        if len(self.args) <= 1:
            active_args.append("defaultSort")
        
        for i in range(len(self.args)):
            if i != 0 and self.args[i] in accepted_args:
                active_args.append(self.args[i])

        if len(active_args) <= 0:
            return print("no valid arguments")
        
        self.sort(active_args)
        
    def sort(self, active_args):
        if "createDir" in active_args:
            print("sorting while creating dir")
        if "categorySort" in active_args:
            print("categorized sorting activated")
        if "defaultSort" in active_args:
            print("default sorting")
        
if __name__ == '__main__':
    argv = sys.argv

    sorter = Sorter(argv)

    sorter.main()
