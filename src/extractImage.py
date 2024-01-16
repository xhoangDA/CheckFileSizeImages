import re
import subprocess
import datetime

# def pull_image(image):
#     subprocess.getoutput(f"docker images -f reference={image}")
#     output = subprocess.getoutput(f"docker pull {image}")
#     return output
def log(message):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{formatted_time}] {message}"
    print(log_message)

def checkExistImage(imageName):
    try:
        checkExist = subprocess.run(["docker", "image", "inspect",imageName], check=True, capture_output=True, text=True)
        return checkExist.returncode
    except subprocess.CalledProcessError as e:
        error = e.stderr

def pullDockerImage(imageName):
    try:
        # Kiểm tra image đã tồn tại trên máy chưa
        checkExist = subprocess.run(["docker", "image", "inspect",imageName], check=True, capture_output=True, text=True)
        if checkExist.returncode != 0:
            # Sử dụng subprocess để chạy lệnh docker pull
            result = subprocess.run(['docker', 'pull', "-q", imageName], check=True, capture_output=True, text=True)
        
    except subprocess.CalledProcessError as e:
        # Nếu lệnh chạy không thành công, in thông báo lỗi và output của lệnh docker pull (nếu cần)
        log(f"\tError: {e.stderr}")

def pullImage(imageName):
    try:
        # Sử dụng subprocess để chạy lệnh docker pull
        result = subprocess.run(['docker', 'pull', "-q", imageName], check=True, capture_output=True, text=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        # Nếu lệnh chạy không thành công, in thông báo lỗi và output của lệnh docker pull (nếu cần)
        # print(f"Error: {e.stderr}")
        log(f"\tERROR: Kéo image {imageName} thất bại. ❌")
        print(f"==> Error detail: {e.stderr}")


# Hàm để lấy ra tên file/thư mục được đẩy vào trong image
def extractFolderFromAddOrCopySyntax(line):
    # Tìm kiếm chuỗi "COPY" hoặc "ADD"
    match = re.search(r'\b(COPY|ADD)\b', line)
    if match:
        # Tìm kiếm chuỗi " in "
        in_match = re.search(r'\sin\s', line)
        if in_match:
            # Lấy giá trị từ sau " in " cho tới dấu cách tiếp theo
            in_index = in_match.end()
            next_space_index = line.find(" ", in_index)
            if next_space_index != -1:
                value = line[in_index:next_space_index].strip()
                return value
        else:
            # Nếu không có "in", lấy giá trị từ "# buildkit" tới dấu cách thứ 2 trước nó
            buildkit_match = re.compile(r'(.*) # buildkit')
            buildkit_match = buildkit_match.search(line)
            if buildkit_match:
                value = buildkit_match.group(1).rstrip().rsplit(' ', 2)[-1]
                return value
    return None

# Hàm dùng để lấy ra tên đường dẫn tuyệt đối thay thế cho đường dẫn tương đối '.' hoặc './'
def extractValueOfDot(lines, i, value):
    breakPoint = False
    if value == "." or value == "./":
        while breakPoint == False:
            # Tìm kiếm chuỗi "WORKDIR"
            workdir_match = re.search(r'\bWORKDIR ', lines[i])
            if workdir_match:
                workdir_index = workdir_match.end()
                next_space_index = lines[i].find(" ", workdir_index)
                breakPoint = True
                return lines[i][workdir_index:next_space_index].strip()
            else: 
                i += 1
    else:
        return value

# Hàm lấy ra tất cả tên thư mục được thêm vào image
def getThingsAddToImage(docker_history_array):
    final_values = []
    # Lọc giá trị cho từng dòng và in ra kết quả
    for i in range(len(docker_history_array)):
        if i != len(docker_history_array) - 1:
            value = extractFolderFromAddOrCopySyntax(docker_history_array[i])
            if value is not None:
                final_values.append(extractValueOfDot(docker_history_array, i, value))
                final_values = list(set(final_values))
    return final_values

# Hàm để lấy ra những file/thư mục được add thêm vào thư mục / (ngoại trừ các folder OS mặc định)
def getNewThingsInRoot(lsFromRoot):
    root_folder_list = ['bin', 'boot', 'cdrom', 'dev', 'etc', 'home', 'lib', 'lib32', 'lib64', 'libx32', 'lost+found', 'media', 'mnt', 'opt', 'proc', 'root', 'run', 'sbin', 'snap', 'srv', 'sys', 'tmp', 'usr', 'var']

    s = set(root_folder_list)
    result = [x for x in lsFromRoot if x not in s]
    # Sử dụng vòng lặp để thêm ký tự '/' vào mỗi phần tử trong mảng result
    for i in range(len(result)):
        result[i] = '/' + result[i]
    return result

# Hàm để lấy ra danh sách các files/thư mục trong đường dẫn / (tương đương lệnh "ls -a /")
def lsFromRoot(input):
    lines = set()  # Sử dụng set để loại bỏ các chuỗi trùng lặp
    for line in input.split('\n'):
        if '/' in line:
            lines.add(line.split('/')[0])
        else:
            lines.add(line)

    return list(lines)

def copyFromContainerToHost(normalizeImage, list_folder, container_id):
    # Tạo thư mục lưu trữ file/thư mục từ image sang host
    # subprocess.getoutput(f"mkdir -p /tmp/checkfilesize/{normalizeImage}")
    subprocess.getoutput(f"[ -d /tmp/checkfilesize/{normalizeImage} ] && rm -rf /tmp/checkfilesize/{normalizeImage}")
    subprocess.getoutput(f"mkdir -p /tmp/checkfilesize/{normalizeImage}")
    for item in list_folder:
        if item.count("/") > 1:
            # Tìm vị trí của ký tự '/' cuối cùng (ví dụ /usr/share/bin/)
            last_slash_index = item.rfind('/')
            # Nếu có ký tự / cuối cùng thì loại bỏ
            if item[-1] == "/":
                new_item = item[:-1]
                last_slash_index = new_item.rfind('/')
                child_path = item[:last_slash_index]
            else:
                # Lưu giá trị từ đầu tới '/' cuối cùng
                child_path = item[:last_slash_index]
            subprocess.getoutput(f"mkdir -p /tmp/checkfilesize/{normalizeImage}{child_path}")
        else: 
            child_path = ''
        subprocess.getoutput(f"docker cp {container_id}:{item} /tmp/checkfilesize/{normalizeImage}{child_path}")
    # trả về  đường dẫn lưu trữ files
    return f"/tmp/checkfilesize/{normalizeImage}"

def processCopyFromContainerToHost(image_name):
    # Chuẩn hóa tên image thành format có thể đặt thành tên folder
    normalizeImage = re.sub('[\/\\-:\s]+', '_', image_name)

    # Lấy ra thông tin docker history của image
    docker_history_output = subprocess.getoutput(f"docker history {image_name} --no-trunc")
    docker_history_output_list = docker_history_output.split("\n")

    things_add_to_image = getThingsAddToImage(docker_history_output_list)

    # Tạo container mà không cần start
    container_id = subprocess.getoutput(f"docker create {image_name}")
    # Cần kiểm tra tạo container thành công không

    # Nếu có COPY/ADD vào đường dẫn /
    if "/" in things_add_to_image:
        # Xuất ra danh sách tất cả file trong image
        container_list_files = subprocess.getoutput(f"docker export {container_id} | tar t")

        # Lấy ra danh sách file/thư mục trong đường dẫn /
        root_ls = lsFromRoot(container_list_files)

        # Lấy ra các file/thư mục khác với các thư mục filesystem mặc định trong đường dẫn /
        new_things_in_root = getNewThingsInRoot(root_ls)

        # Loại bỏ / ra khỏi mảng things_add_to_image
        things_add_to_image.remove("/")

        # Gom 2 mảng new_things_in_root và things_add_to_image lại với nhau
        final_list_add_to_image = new_things_in_root + things_add_to_image
    else:
        final_list_add_to_image = things_add_to_image
        
    stored_path = copyFromContainerToHost(normalizeImage, final_list_add_to_image, container_id)
    # print(final_list_add_to_image)
    
    # Xóa các file symbolic links để  tránh xảy ra lỗi
    subprocess.getoutput("find " + stored_path + " -type l -ls -exec rm -f {} \;")
    output = [stored_path, container_id]
    return output

def clean(containerID1, containerID2, image1, image2, storedPath1, storedPath2):
    try:
        if containerID1 != None and image1 != None and storedPath1 != None:
            # Clean containers
            cleanContainer1 = subprocess.run(['docker', 'rm', containerID1], check=True, capture_output=True, text=True)
            cleanContainer2 = subprocess.run(['docker', 'rm', containerID2], check=True, capture_output=True, text=True)
            # Clean images
            cleanImage1 = subprocess.run(['docker', 'rmi', image1, '--force'], check=True, capture_output=True, text=True)
            cleanImage2 = subprocess.run(['docker', 'rmi', image2, '--force'], check=True, capture_output=True, text=True)        
            # Clean data in disk
            cleanDisk1 = subprocess.run(['rm', '-rf', storedPath1], check=True, capture_output=True, text=True)        
            cleanDisk2 = subprocess.run(['rm', '-rf', storedPath2], check=True, capture_output=True, text=True) 
            cleanReturnCode = [cleanContainer1.returncode, cleanContainer2.returncode, cleanImage1.returncode, cleanImage2.returncode, cleanDisk1.returncode, cleanDisk2.returncode]
            return cleanReturnCode
        else:
            # Clean container
            cleanContainer2 = subprocess.run(['docker', 'rm', containerID2], check=True, capture_output=True, text=True)
            # Clean images
            cleanImage2 = subprocess.run(['docker', 'rmi', image2, '--force'], check=True, capture_output=True, text=True)        
            # Clean data in disk
            cleanDisk2 = subprocess.run(['rm', '-rf', storedPath2], check=True, capture_output=True, text=True) 
            cleanReturnCode = [cleanContainer2.returncode,  cleanImage2.returncode, cleanDisk2.returncode]
            return cleanReturnCode
    except subprocess.CalledProcessError as e:
        log(f"\tERROR: Dọn dẹp thất bại. ❌")
        print(f"==> Error detail: {e.stderr}")

