import html2text



file = open(r"C:/Users/mdw82/python/PSEditorReleaseNotes.htm", "r")
file = file.read()

text = html2text.html2text(file)

print(text)
