import sys
import os
from web2png import trans2png

def main():
    if len(sys.argv) > 1:
        file_list = sys.argv[1:] 
        for fl in file_list:
            if os.path.exist(fl):
                if fl.endswith(".webp"):
                    trans2png(fl)
                else:
                    print("please pic format webp")
            else:
                print(f"does not exist {fl}")

    else:
         print("usage: webp2png file1.webp file2.webp")


if __name__ == "__main__":
    main()


