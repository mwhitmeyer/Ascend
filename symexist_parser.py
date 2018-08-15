file = open("input.txt", "r")
line = file.readline().strip()
potential_parameters = []

while line != "":
    if line[0] == 'C':
        line = file.readline().strip()
        continue
    elif line[0] == 'L':
        line = line.lower()
        index = line.find('%symexist')
        if index == -1:
            print("FAT ERROR")
            print(line)
        line = line[index:]
        index = line.find('(')
        line = line[index + 1:]
        index = line.find(')')
        line = line[:index]
        line = "&" + line
        if line not in potential_parameters:
            potential_parameters.append(line)

        line = file.readline().strip()
    else:
        print("error")
        line = file.readline().strip()


file.close()

print(potential_parameters)

file = open("output.txt", "w")
for parameter in potential_parameters:
    file.write(parameter + "\r\n")
file.close()
