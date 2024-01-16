import sys
import time
import datetime
from src.args import arguments
from src import compareAlgorithms
from src import extractImage
# from src import terminalActions

argValues = arguments.argsFunc()
algorithms = compareAlgorithms
extractImageAlgs = extractImage
# TerminalActions = terminalActions

storedPath1 = ""
storedPath2 = ""
dirPath1 = ""
dirPath2 = ""
containerID1 = ""
containerID2 = ""
filesDir1 = []
filesDir2 = []
listFiles = []
result = []

def pullImages():
    try:
        print('*** Kiểm tra tồn tại images...')
        if not argValues[0]:
            extractImageAlgs.log('\t  INFO: Giá trị old image để trống.')
            extractImageAlgs.log('\t  INFO: Bỏ qua old image.')
            checkExistImage1 = 2
        else:
            checkExistImage1 = extractImageAlgs.checkExistImage(argValues[0])

        checkExistImage2 = extractImageAlgs.checkExistImage(argValues[1])

        if checkExistImage1 == 0:
            extractImageAlgs.log(f"\tINFO: Old image đã tồn tại. Bỏ qua pull image.")
        elif checkExistImage1 == 2:
            pass
        else:
            extractImageAlgs.log(f"\tINFO: Old image chưa tồn tại. Thực hiện kéo image {argValues[0]}...")
            exitCodePullImage1 = extractImageAlgs.pullImage(argValues[0])
            if exitCodePullImage1 == 0:
                extractImageAlgs.log(f'\tINFO: Kéo image {argValues[0]} hoàn tất.')
            else:
                extractImageAlgs.log(f'\tERROR: Kéo image {argValues[0]} thất bại. ❌')
                sys.exit(100)

        if checkExistImage2 == 0:
            extractImageAlgs.log(f"\tINFO: New image đã tồn tại. Bỏ qua pull image.")
        else:
            extractImageAlgs.log(f"\tINFO: New image chưa tồn tại. Thực hiện kéo image {argValues[1]}...")
            exitCodePullImage2 = extractImageAlgs.pullImage(argValues[1])
            if exitCodePullImage2 == 0:
                extractImageAlgs.log(f'\tINFO: Kéo image {argValues[1]} hoàn tất.')
            else:
                # extractImageAlgs.log(f'\tERROR: Kéo image {argValues[1]} thất bại. ❌')  
                sys.exit(100)

    except Exception as e:
        extractImageAlgs.log(f"\tERROR: {e}")
        sys.exit(100)

def extractFiles2Image():
    global listFiles
    global filesDir1
    global filesDir2
    global dirPath1
    global dirPath2
    global containerID1
    global containerID2
    global storedPath1
    global storedPath2
    try:
        print('*** Trích xuất image...')
        # if not algorithms.checkPath(argValues[1], argValues[2]):
        #     breakpoint = True
        #     pathError = True
        #     print('\n❌😨😨 ERROR: Đường dẫn 2 không đúng với mã phát hành mới. Vui lòng kiểm tra lại.')
        #     sys.exit()
        if not argValues[0]:
            extractImageAlgs.log('\tINFO: Bỏ qua trích xuất old image.')
        else:
            extractImageAlgs.log('\tINFO: Trích xuất old image...')
            extractOutput1 = extractImageAlgs.process_to_copy_from_container_to_host(argValues[0])
            storedPath1 = extractOutput1[0]
            containerID1 = extractOutput1[1]
            extractImageAlgs.log('\tINFO: Trích xuất old image hoàn tất. ✅')
        time.sleep(0.5)
        extractImageAlgs.log('\tINFO: Trích xuất new image...')
        extractOutput2 = extractImageAlgs.process_to_copy_from_container_to_host(argValues[1])
        storedPath2 = extractOutput2[0]
        containerID2 = extractOutput2[1]
        extractImageAlgs.log('\tINFO: Trích xuất new image hoàn tất. ✅')

    except Exception as e:
        extractImageAlgs.log(f"\tERROR: Trích xuất file thất bại. ❌")
        print(f"==> Error detail: {e}")
        sys.exit(100)

def getFiles2Folder():
    global listFiles
    global filesDir1
    global filesDir2
    global storedPath1
    global storedPath2
    try:
        print('*** Duyệt files...')
        # if not algorithms.checkPath(argValues[1], argValues[2]):
        #     breakpoint = True
        #     pathError = True
        #     print('\n❌😨😨 ERROR: Đường dẫn 2 không đúng với mã phát hành mới. Vui lòng kiểm tra lại.')
        #     sys.exit()
        if not argValues[0]:
            extractImageAlgs.log('\tINFO: Duyệt files trên thư mục 1')
            filesDir1 = [['', '', '', 0, '', '']]
            listFiles.append(filesDir1)
            extractImageAlgs.log('\tINFO: Duyệt thư mục 1 hoàn tất. ✅')
        else:
            extractImageAlgs.log('\tINFO: Duyệt files trên thư mục 1...')
            filesDir1 = algorithms.getFiles(storedPath1)
            listFiles.append(filesDir1)
            extractImageAlgs.log('\tINFO: Duyệt thư mục 1 hoàn tất. ✅')
        time.sleep(0.5)
        extractImageAlgs.log('\tINFO: Duyệt files trên thư mục 2...')
        filesDir2 = algorithms.getFiles(storedPath2)
        extractImageAlgs.log('\tINFO: Duyệt thư mục 2 hoàn tất. ✅')
        # extractImageAlgs.log(filesDir1)
        listFiles.append(filesDir2)
    
    except Exception as e:
        extractImageAlgs.log(f"\tERROR: Duyệt file thất bại. ❌")
        print(f"==> Error detail: {e}")
        sys.exit(100)

def compare():
    print('*** So sánh files...')
    global result
    global listFiles
    try:
        compareResult = algorithms.compareList(listFiles[0], listFiles[1])
        result.append(listFiles[0])
        result.append(listFiles[1])
        result.append(compareResult)
        extractImageAlgs.log(f"\tINFO: So sánh file hoàn tất. ✅")
    except Exception as e:
        extractImageAlgs.log(f"\tERROR: So sánh file thất bại. ❌")
        print(f"==> Error detail: {e}")
        sys.exit(100)

def output():
    global finishOutput
    global failOutput
    global result
    print('*** Xuất file kết quả...')
    try:
        fileOutput = algorithms.writeToExcelFile(result[0], result[1], result[2], argValues[0], argValues[1], argValues[2], argValues[3])
        extractImageAlgs.log(f"\tINFO: Xuất file kết quả hoàn tất ✅")
        extractImageAlgs.log(f"\tINFO: Đường dẫn file kết quả: {fileOutput}")
        # TerminalActions.createTable(result[2])
    except Exception as e:
        extractImageAlgs.log(f"\tERROR: {e}")
        sys.exit(100)

def clean():
    global storedPath1
    global storedPath2
    global containerID1
    global containerID2
    print('*** Dọn dẹp sau kiểm tra...')
    try:
        cleanReturnCode = extractImageAlgs.clean(containerID1, containerID2, argValues[0], argValues[1], storedPath1, storedPath2)
        if cleanReturnCode != None: 
            if all(element == 0 for element in cleanReturnCode):
                extractImageAlgs.log(f"\tINFO: Dọn dẹp hoàn tất ✅")
            else: 
                sys.exit(100)
        else: 
            sys.exit(100)
    except Exception as e:
        extractImageAlgs.log(f"\tERROR: {e}")
        sys.exit(100)

if __name__ == "__main__":
    print('''
       _               _            __ _ _                 _                     _              _ 
      | |             | |          / _(_) |               (_)                   | |            | |
   ___| |__   ___  ___| | ________| |_ _| | ___ ______ ___ _ _______  ___ ______| |_ ___   ___ | |
  / __| '_ \ / _ \/ __| |/ /______|  _| | |/ _ \______/ __| |_  / _ \/ __|______| __/ _ \ / _ \| |
 | (__| | | |  __/ (__|   <       | | | | |  __/      \__ \ |/ /  __/\__ \      | || (_) | (_) | |
  \___|_| |_|\___|\___|_|\_\      |_| |_|_|\___|      |___/_/___\___||___/       \__\___/ \___/|_|                                                                                                                                                         
    ''')
    print(f"""
INPUT:
[+] OLD IMAGE:      {argValues[0]}
[+] NEW IMAGE:      {argValues[1]}
[+] PRODUCT NAME:   {argValues[2]}
[+] VERSION:        {argValues[3]}
""")
    print("BẮT ĐẦU THỰC HIỆN CHECKFILESIZE\n")
    start = time.time()
    time.sleep(0.5)
    pullImages()
    time.sleep(0.5)
    extractFiles2Image()
    getFiles2Folder()
    end = time.time()
    compare()
    output()
    clean()
    print('CHECKFILESIZE THÀNH CÔNG !!!')
    print("Tổng thời gian chạy: " + str(end - start))
