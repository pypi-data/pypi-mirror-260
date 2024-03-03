import os, sys


class Danielley(): 
    def DDD(folder_name):
        current_directory=os.getcwd()
        folder_opened_in_vs = folder_name
        symbol = "\\" if sys.platform == "win32" else "/"

        index = current_directory.find(folder_opened_in_vs + symbol)

        if index != -1:
            new_path = current_directory[index + len(folder_opened_in_vs + symbol):]
        else:
            print("From Dot-Dot-Dee: We couldn't find iDDD") 

        return sys.path.append(current_directory.replace(new_path, ""))
