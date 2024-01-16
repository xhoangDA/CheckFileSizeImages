from src.args import arguments
from src import compareAlgorithms
from src import extractImage
import time
# from src import terminalActions
import threading
import sys
import json

argValues = arguments.argsFunc()
algorithms = compareAlgorithms
extractImageAlgs = extractImage
# TerminalActions = terminalActions

breakpoint = False
finishExtractFiles = False
failExtractFiles = False
finishGetFiles = False
failGetFiles = False
finishCompareFiles = False
failCompareFiles = False
finishOutput = False
failOutput = False
pathError = False
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

def threadExtractFiles():
    time.sleep(0.5)
    def message():
        # Kết thúc animation
        global breakpoint
        while not extractImageCompleted.is_set() and breakpoint:
            time.sleep(2)
            if finishExtractFiles:  # Kiểm tra kết quả của hàm getfile
                time.sleep(1)
                print("\nTrích xuất image ra host thành công! ✅ ")
                breakpoint = False
                # return listFiles
            elif failExtractFiles: 
                print("\nTrích xuất image ra host thất bại! ❌😨😨")
                breakpoint = False

    def extractFiles2Image():
        global finishExtractFiles
        global failExtractFiles
        global listFiles
        global filesDir1
        global filesDir2
        global dirPath1
        global dirPath2
        global containerID1
        global containerID2
        global storedPath1
        global storedPath2
        global breakpoint
        try:
            print('\n[+] Đang trích xuất image...')
            # if not algorithms.checkPath(argValues[1], argValues[2]):
            #     breakpoint = True
            #     pathError = True
            #     print('\n❌😨😨 ERROR: Đường dẫn 2 không đúng với mã phát hành mới. Vui lòng kiểm tra lại!')
            #     sys.exit()
            if not argValues[0]:
                print('[+] INFO: Giá trị old image để trống.')
                print('\n--- Bỏ qua old image! ✅')
            else:
                print('[+] Trích xuất old image...')
                extractOutput1 = extractImageAlgs.process_to_copy_from_container_to_host(argValues[0])
                storedPath1 = extractOutput1[0]
                containerID1 = extractOutput1[1]
                print('\n--- Trích xuất old image thành công! ✅')
            time.sleep(0.5)
            print('\n[+] Trích xuất new image...')
            extractOutput2 = extractImageAlgs.process_to_copy_from_container_to_host(argValues[1])
            storedPath2 = extractOutput2[0]
            containerID2 = extractOutput2[1]
            print('\n--- Trích xuất new image thành công! ✅')
            finishExtractFiles = True

        except Exception as e3:
            failExtractFiles = True
            breakpoint = True
            print(f"\n❌😨😨 ERROR: {e3}")

    extractImageCompleted = threading.Event()
    extractImageThread = threading.Thread(target=extractFiles2Image)
    messageThread = threading.Thread(target=message)
    
    # Bắt đầu chạy cả hai luồng
    extractImageThread.start()
    messageThread.start()

    # Đợi cho đến khi hàm extractImage hoàn thành
    extractImageThread.join()
    time.sleep(0.5)
    # Đánh dấu rằng hàm extractImage đã hoàn thành
    extractImageCompleted.set()
    # Đợi cho đến khi luồng animation cũng hoàn thành
    messageThread.join()

def threadGetFiles():
    time.sleep(0.5)
    def message():
        # Kết thúc animation
        global breakpoint
        while not getfile_completed.is_set() and breakpoint:
            time.sleep(2)
            if finishGetFiles:  # Kiểm tra kết quả của hàm getfile
                time.sleep(1)
                print("\nDuyệt files thành công! ✅ ")
                breakpoint = False
                # return listFiles
            elif failGetFiles: 
                print("\nDuyệt files thất bại! ❌😨😨")
                breakpoint = False

    def getFiles2Folder():
        global finishGetFiles
        global failGetFiles
        global listFiles
        global filesDir1
        global filesDir2
        global storedPath1
        global storedPath2
        global breakpoint
        global pathError
        try:
            print('\n[+] Đang duyệt files...')
            # if not algorithms.checkPath(argValues[1], argValues[2]):
            #     breakpoint = True
            #     pathError = True
            #     print('\n❌😨😨 ERROR: Đường dẫn 2 không đúng với mã phát hành mới. Vui lòng kiểm tra lại!')
            #     sys.exit()
            if not argValues[0]:
                print('[+] Duyệt files trên thư mục 1')
                filesDir1 = [['', '', '', 0, '', '']]
                listFiles.append(filesDir1)
                print('\n--- Duyệt thư mục 1 thành công! ✅')
            else:
                print('\n[+] Duyệt files trên thư mục 1...')
                filesDir1 = algorithms.getFiles(storedPath1)
                listFiles.append(filesDir1)
                print('\n--- Duyệt thư mục 1 thành công! ✅')
            time.sleep(0.5)
            print('\n[+] Duyệt files trên thư mục 2...')
            filesDir2 = algorithms.getFiles(storedPath2)
            print('\n--- Duyệt thư mục 2 thành công! ✅')
            # print(filesDir1)
            listFiles.append(filesDir2)
            finishGetFiles = True
        
        except Exception as e3:
            failGetFiles = True
            breakpoint = True
            print(f"\n❌😨😨 ERROR: {e3}")
            # return False

    getfile_completed = threading.Event()
    getfile_thread = threading.Thread(target=getFiles2Folder)
    message_thread = threading.Thread(target=message)
    
    # Bắt đầu chạy cả hai luồng
    getfile_thread.start()
    message_thread.start()

    # Đợi cho đến khi hàm getfile hoàn thành
    getfile_thread.join()
    time.sleep(0.5)
    # Đánh dấu rằng hàm getfile đã hoàn thành
    getfile_completed.set()
    # Đợi cho đến khi luồng animation cũng hoàn thành
    message_thread.join()

def threadCompare():
    time.sleep(1)

    def message():
        # Kết thúc animation
        point = True
        while not compare_completed.is_set() and point == True:
            if finishCompareFiles == True:  # Kiểm tra kết quả của hàm getfile
                time.sleep(1)
                print("\n--- So sánh files thành công! ✅ ")
                point = False
                # return listFiles
            elif failCompareFiles == True: 
                print("\n--- So sánh files thất bại! ❌😨😨")
                point = False

    def compare():
        time.sleep(0.5)
        print('\n[+] Đang so sánh files...')
        global finishCompareFiles
        global failCompareFiles
        global result
        global listFiles
        try:
            compareResult = algorithms.compareList(listFiles[0], listFiles[1])
            result.append(listFiles[0])
            result.append(listFiles[1])
            result.append(compareResult)
            finishCompareFiles = True
        except Exception as e:
            failCompareFiles = True
            print(f"\nError: {e}")
            return False

    compare_completed = threading.Event()
    compare_thread = threading.Thread(target=compare)
    message_thread = threading.Thread(target=message)
    
    # Bắt đầu chạy cả hai luồng
    compare_thread.start()
    message_thread.start()

    # Đợi cho đến khi hàm compare hoàn thành
    compare_thread.join()
    time.sleep(0.5)

    # Đánh dấu rằng hàm compare đã hoàn thành
    compare_completed.set()

    # Đợi cho đến khi luồng animation cũng hoàn thành
    message_thread.join()

def threadFinal():
    global breakpoint

    time.sleep(1)
    def message():
        # Kết thúc animation
        point = True
        while not output_completed.is_set() and point == True:
            if finishOutput == True:  # Kiểm tra kết quả của hàm getfile
                time.sleep(1)
                print("\n--- Xuất file kết quả thành công! ✅ ")
                point = False
                # return listFiles
            elif failOutput == True: 
                print("\n--- Xuất file kết quả thất bại! ❌😨😨")
                point = False

    def output():
        time.sleep(0.5)
        print('\n[+] Đang xuất kết quả...')
        global finishOutput
        global failOutput
        global result
        try:
            algorithms.writeToExcelFile(result[0], result[1], result[2], argValues[0], argValues[1], argValues[2], argValues[3])
            finishOutput = True
            # TerminalActions.createTable(result[2])
        except Exception as e:
            failOutput = True
            print(f"\nError: {e}")
            return False
        
    output_completed = threading.Event()
    output_thread = threading.Thread(target=output)
    message_thread = threading.Thread(target=message)
    
    # Bắt đầu chạy cả hai luồng
    output_thread.start()
    message_thread.start()

    # Đợi cho đến khi hàm output hoàn thành
    output_thread.join()
    time.sleep(0.5)

    # Đánh dấu rằng hàm output đã hoàn thành
    output_completed.set()

    # Đợi cho đến khi luồng animation cũng hoàn thành
    message_thread.join()

if __name__ == "__main__":
    print('''
       _               _            __ _ _                 _                     _              _ 
      | |             | |          / _(_) |               (_)                   | |            | |
   ___| |__   ___  ___| | ________| |_ _| | ___ ______ ___ _ _______  ___ ______| |_ ___   ___ | |
  / __| '_ \ / _ \/ __| |/ /______|  _| | |/ _ \______/ __| |_  / _ \/ __|______| __/ _ \ / _ \| |
 | (__| | | |  __/ (__|   <       | | | | |  __/      \__ \ |/ /  __/\__ \      | || (_) | (_) | |
  \___|_| |_|\___|\___|_|\_\      |_| |_|_|\___|      |___/_/___\___||___/       \__\___/ \___/|_|                                                                                                                                                         
    ''')
    start = time.time()
    time.sleep(0.5)
    threadExtractFiles()
    threadGetFiles()
    end = time.time()
    if breakpoint == False:
        threadCompare()
        threadFinal()
        time.sleep(1)
        print('Kết thúc!!!')
        print("Tổng thời gian chạy: " + str(end - start))
    else:
        print("Tổng thời gian chạy: " + str(end - start))
