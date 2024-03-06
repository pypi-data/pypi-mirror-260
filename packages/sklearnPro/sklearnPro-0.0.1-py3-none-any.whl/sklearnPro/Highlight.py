import os  
  
filename = 'hello.py'
if os.path.exists(filename):  
    with open(filename, 'r') as file:  
        print(file.read())  
else:  
    print(f"The file {filename} does not exist.")