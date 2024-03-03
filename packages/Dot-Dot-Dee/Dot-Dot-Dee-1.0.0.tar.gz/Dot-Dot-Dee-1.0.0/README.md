# DOT-DOT-DEE

### What is DotDotDee?
 DotDotDee is a simple python "library" (let's say it's one) that allows you to import your Python files in a simple way, no matter your folder configuration.
 
 If you ever faced some errors like: 
 ```ModuleNotFoundError: No module named <folder_name>```
 
 ... while trying to import a function from other directory.
 
 
 Here you a have a solution proposal, just follow the steps below 👇


### Steps guide:
 1. Install Dot-Dot-Dee:  ```pip install DotDotDeee==1.1.0```. (I know it has an extra 'e'... I have dislexia)
 


 2. Type in the file where you are trying to do the importation: 
 
        from DotDotDeee import DotDotDee


 3. Continue typing: 
 
        DotDotDee.Danielley.DDD("Random-garbage")

    expl: Random-garbage is the name of your VS Code project. (The folder you opened)


 4. Do your importation below. ex: 
 
        from api.models.configuration import Configuration
        

 Pd: If a ```None``` appears in the terminal... It's just a gift for you!!
 
 
 xoxo
