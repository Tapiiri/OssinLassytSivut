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
        
def newFileData(lines, filenameWithoutType):
    splitByHeader =  "\n".join(lines).split("---")
    try:
        headerLines = splitByHeader[1].split("\n")
        newHeaderLines = []
        for line in headerLines:
            if ":" in line:
                [name, *value] = line.split(":")
                if name == "title":
                    newTitle = f"titles.{filenameWithoutType}"
                    newLine = ": ".join([name, newTitle])
                    newHeaderLines += [ newLine ]
                else:
                    newHeaderLines += [ line ]
            else:
                newHeaderLines += [ line ]
        newHeader = "\n".join(newHeaderLines)


        newData = "---".join([
            splitByHeader[0],
            newHeader,
            splitByHeader[2],
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

        def updateFile(file):
            lines = data.split("\n")
            title = getTitle(lines)
            filenameWithoutType = filename.split(".")[0]
            titleObject = [ title , filenameWithoutType ]
            newData = newFileData(lines, filenameWithoutType)
            return [ newData, titleObject ]

        for filename in filter(lambda x: ".md" in x, os.listdir(directory)):
            newData = ""
            filePath = os.path.join(directory, filename)
            print(filePath)
            with open(filePath, "r+") as file:
                data = file.read()
                [ newData, titleObject ] = updateFile(file)
                titles += [ titleObject ]
                
            folderPath = os.path.join(directory, filename.split(".")[0])
            try:
                os.mkdir(folderPath)
            except FileExistsError:
                pass

            
            newFilePath = os.path.join(folderPath, filename)
            with open(newFilePath, "w") as file:
                file.write(newData)

            os.remove(filePath) 

        # writeTitles(lang, titles)

main()