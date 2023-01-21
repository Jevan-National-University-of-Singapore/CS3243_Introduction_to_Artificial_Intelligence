file_name = "1.txt"
lines = []
with open(file_name) as f:
    lines = f.readlines()
    lines = [line.strip('\n') for line in lines]