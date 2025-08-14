import sys
import os
import shutil
import datetime

class Sorter:
    def __init__(self, argv):
        self.current_dir = argv[2] if len(argv) > 2 else os.getcwd()
        self.argv = argv
        self.accepted_args = ["createDir", "dateSort"]

    def main(self):
        active_mode = ""

        if len(self.argv) <= 1 or self.argv[1] == self.accepted_args[0]:
            active_mode = self.accepted_args[0]
        elif self.argv[1] == self.accepted_args[1]:
            active_mode = self.accepted_args[1]
        
        self.sort(active_mode)
        
    def sort(self, active_mode):
        match active_mode:
            case "createDir":
                print(f"Default sorting in {self.current_dir}...")
                sorted_dir = os.path.join(self.current_dir, 'directory_sorted')
                self.createDir(self.current_dir, sorted_dir)
            case "dateSort":
                print(f"Date sorting in {self.current_dir}...")
                sorted_dir = os.path.join(self.current_dir, 'date_sorted')
                self.dateSort(self.current_dir, sorted_dir)

    # checker kun an directory na exist na ba or diri
    def check_dir(self, sorted_dir):
        try:
            # an exists_ok na parameter para diri mag raise hin exception
            os.makedirs(sorted_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating sorted directory: {e}")
            return False
        return True

    def createDir(self, source_dir, sorted_dir):
        if not self.check_dir(sorted_dir):
            return
            
        items = os.listdir(source_dir)

        for item in items:
            filepath = os.path.join(source_dir, item)

            # key change para ma skip an mga directory ngan kun an ngaran an sorted folder name para fullproof la
            # though bangin magkaada issue ha sorted folder pero sunod nala iton
            if os.path.isdir(filepath) or item == 'directory_sorted':
                continue

            _, ext = os.path.splitext(item)
            
            # kun file ngan may extension
            if ext:
                # example .pdf, ig omit an dot tapos keep an rest, idk very weird syntax but amo iton
                ext = ext[1:]
                
                # check if an extension directory na exist na
                ext_dir = os.path.join(sorted_dir, ext)
                if not self.check_dir(ext_dir):
                    continue

                try:
                    # move an item ha iya proper directory
                    dest = os.path.join(ext_dir, item)
                    shutil.move(filepath, dest)
                    print(f"Moved {item} to {ext_dir}")
                except shutil.SameFileError:
                    print(f"File {item} already exists in destination")
                except Exception as e:
                    print(f"Error moving {item}: {e}")
            else:
                # kun file ngan waray extension
                no_ext_dir = os.path.join(sorted_dir, 'no_extension')
                try:
                    if not self.check_dir(no_ext_dir):
                        continue

                    dest = os.path.join(no_ext_dir, item)
                    shutil.move(filepath, dest)
                    print(f"Moved {item} to no_extension folder")
                except Exception as e:
                    print(f"Error moving {item}: {e}")
    
    def dateSort(self, source_dir, sorted_dir):
        if not self.check_dir(sorted_dir):
            return
            
        items = os.listdir(source_dir)

        for item in items:
            filepath = os.path.join(source_dir, item)

            # same with this pareho ha igbaw monitor if magkakaada issues ha sorted folder name
            if os.path.isdir(filepath) or item == 'date_sorted':
                continue

            try:
                last_mod = os.path.getmtime(filepath)
                last_mod_date = datetime.datetime.fromtimestamp(last_mod)

                date_str = last_mod_date.strftime('%Y-%m-%d')

                date_dir = os.path.join(sorted_dir, date_str)
                
                if not self.check_dir(date_dir):
                    continue

                dest = os.path.join(date_dir, item)
                shutil.move(filepath, dest)
                print(f"Moved {item} to {date_dir}")
                
            except shutil.SameFileError:
                print(f"File {item} already exists in destination")
            except Exception as e:
                print(f"Error processing {item}: {e}")
        
if __name__ == '__main__':
    argv = sys.argv
    sorter = Sorter(argv)
    sorter.main()
