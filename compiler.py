import os 

data_directory = "data/"
compiled_file = "compiled.txt"
print("starting...")
for filename in os.listdir(data_directory):
    if filename.endswith(".txt"):
        addition = ""
        with open(data_directory+filename, "r") as f:
            for line in f:
                addition += line.strip() + "\r\n"
        with open(compiled_file, "a") as f: 
            f.write(addition)

print("Done.")