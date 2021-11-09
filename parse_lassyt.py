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
        newData = splitByHeader[2]
        return newData
    except IndexError:
        return "\n".join(lines)

def newRootFileData(lines, filenameWithoutType):
    splitByHeader =  "\n".join(lines).split("---")
    try:
        headerLines = splitByHeader[1].split("\n")
        newHeaderLines = []
        noPermaLink = True

        newValues = [
            ["title", f"titles.{filenameWithoutType}"],
            ["permalink", f"/{filenameWithoutType}/"],
            ["layout", "page"]
        ]
        for line in headerLines:
            if ":" in line:
                [name, *value] = line.split(":")
                if name in map(lambda newValue: newValue[0], newValues):
                    continue
                else:
                    newHeaderLines += [ line ]

        for newValue in newValues:
            [ name, value ] = newValue
            newLine = ": ".join([name, value])
            newHeaderLines += [ newLine ]

        newHeader = "\n".join(["", *newHeaderLines, ""])

        newBody = f"\n{{% translate_file _lassyt/{filenameWithoutType}/{filenameWithoutType}.md %}}"

        newData = "---".join([
            splitByHeader[0],
            newHeader,
            newBody,
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

        def updateFile(data):
            lines = data.split("\n")
            title = getTitle(lines)
            filenameWithoutType = filename.split(".")[0]
            titleObject = [ title , filenameWithoutType ]
            newData = newFileData(lines, filenameWithoutType)
            return [ newData, titleObject ]
            

        for filename in os.listdir(directory):
            folderExists = False
            fileNameWithType = filename if ".md" in filename else filename + ".md"
            folderPath = os.path.join(directory, filename.split(".")[0])
            newFilePath = os.path.join(folderPath, fileNameWithType)
            try:
                os.mkdir(folderPath)
            except FileExistsError:
                folderExists = True

            newData = ""
            filePath = os.path.join(directory, fileNameWithType) if not folderExists else newFilePath
            print(filePath)
            with open(filePath, "r+") as file:
                data = file.read()
                [ newData, titleObject ] = updateFile(data)
                titles += [ titleObject ]

            
            with open(newFilePath, "w") as file:
                file.write(newData)

            if not folderExists:
                os.remove(filePath) 

        # writeTitles(lang, titles)
    
    directory = f"./lassyt"
    for filename in filter(lambda x: ".md" in x, os.listdir(directory)):
            newData = ""
            filePath = os.path.join(directory, filename)

            def updateRootFile(data):
                lines = data.split("\n")
                filenameWithoutType = filename.split(".")[0]
                newData = newRootFileData(lines, filenameWithoutType)
                return [ newData ]

            with open(filePath, "r+") as file:
                data = file.read()
                [ newData ] = updateRootFile(data)

            with open(filePath, "w") as file:
                file.write(newData)


main()