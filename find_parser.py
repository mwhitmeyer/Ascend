from copy import deepcopy
import os

def take_out_extra_slash(string):
	copy = deepcopy(string)
	doubles = []
	for i in range(1, len(string)):
		if string[i-1] == "\\" and string[i] == "\\":
			doubles.append(i)
	for index in reversed(doubles):
		copy = copy[:index] + copy[index+1:]


folders = ""
files = ""
examples = ""
main_path = r"C:\Users\mdw82\ascend\sasmacroCheckout"
length = len(main_path)
parameter = None

#print("working directory: ", os.getcwd())
file = open("input.txt", "r")
line = file.readline().strip()

index = line.find("&")
if index == -1:
	print("HUH???")
else:
	line = line[index:]
	index = line.find("\"")
	line = line[:index]
	parameter = line

line = file.readline().strip()

while line != "" and line[0] != 'S':
	if line[0] == 'C': # this is the beginning of a file location
		line = line[length:]
		i = -1
		while line[i] != '(':
			i -= 1
		line = line[:len(line) + i]
		line = line.strip()
		i = -1
		while line[i] != "\\":
			i-=1
		if files.find(line + ",") == -1:
			files += line + ", "
		folder = line[:len(line) + i]
		if folders.find(folder + ",") == -1:
			folders += folder + ", "
	elif line[0] == 'L':
		i = 0
		while line[i] != ':':
			i += 1
		line = line[i+1:]
		line = line.strip()
		examples += line + "\r\n"
	else:
		print("don't know how to process", line)
	line = file.readline().strip()


if folders != "":
	folders = folders[:len(folders) - 2]
if files != "":
	files = files[:len(files) - 2]
# if examples != "":
# 	examples = examples[:len(examples) - 2]

file.close()

file = open("output.txt", "w")
file.write("Parameter: " + parameter + "\r\n\r\n")
file.write("Folders: " + folders + "\r\n\r\n")
file.write("Files: " + files + "\r\n\r\n")
file.write("Examples: " + examples)
file.close()

# print("Parameter:", parameter)
# print("Folders:", folders)
# print("Files:", files)
# print("Examples:", examples)
