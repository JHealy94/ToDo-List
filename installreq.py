import pip
read = open("requirments.txt", "r")

for r in read:
    pip.main(['install', r])
