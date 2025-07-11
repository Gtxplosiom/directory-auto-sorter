import sys

class Sorter:
    def __init__(self, argv):
        self.current_dir = argv[1]
        self.argv = argv

        self.accepted_args = ["createDir", "categorySort"]

    def main(self):
        active_mode = ""

        if len(self.argv) <= 2 or self.argv[2] == self.accepted_args[0]:
            active_mode = self.accepted_args[0]
        elif self.argv[2] == self.accepted_args[1]:
            active_mode = self.accepted_args[1]
        
        self.sort(active_mode)
        
    def sort(self, active_mode):
        if active_mode == self.accepted_args[0]:
            print(f"sorting while creating dir in {self.current_dir}")
        elif active_mode == self.accepted_args[1]:
            print(f"categorized sorting activated in {self.current_dir}")
        
if __name__ == '__main__':
    argv = sys.argv

    sorter = Sorter(argv)

    sorter.main()
