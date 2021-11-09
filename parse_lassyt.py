import os

def writeTitles(lang, titles):
    titleYML = "\ntitles:\n    lassyt:\n" 
    for [ title, filename ] in titles:
        titleString = f"        {filename}: {title}\n"
        titleYML += titleString
    translationFilePath =  f"./_i18n/{lang}.yml"
    with open(translationFilePath, "a") as translationFile:
        translationFile.write(titleYML)

def getTitle(lines):
     for line in lines:
        try:
            if line[0] == "#":
                title = line.split("#")[1].strip().replace('"', '\\"')
                return f'"{title}"'
        except IndexError:
            continue
        
def writeTitle(lines, filenameWithoutType):
    splitByHeader =  "\n".join(lines).split("---")
    try:
        headerLines = splitByHeader[1].split("\n")
        headerLines = []
        for line in headerLines:
            [name, value] = line.split(":")
            if name == "title":
                newTitle = f"titles.{filenameWithoutType}"
                newLine = ":".join([name, newTitle])
                headerLines += [ newLine ]
            else:
                headerLines += [ line ]
        newHeader = "\n".join(headerLines)
                
        newData = "---".join([
            splitByHeader[0],
            newHeader,
            *splitByHeader[2:]
        ])
        return newData
    except IndexError:
        print("No header found")
        return "\n".join(lines)

def main():
    langs = ["fi", "en"]
    for lang in langs:
        directory = f"./_i18n/{lang}/_lassyt"
        titles = []

        for filename in os.listdir(directory):
            filePath = os.path.join(directory, filename)
            with open(filePath, "r+") as file:
                data = file.read()
                lines = data.split("\n")
                title = getTitle(lines)
                filenameWithoutType = filename.split(".")[0]
                titleObject = [ title , filenameWithoutType ]
                titles += [ titleObject ]
                newData = writeTitle(lines, filenameWithoutType)
                file.write(newData)

        writeTitles(lang, titles)

main()