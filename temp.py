input_string = "/folder1/folder2/file.txt"

# Kiểm tra số lượng ký tự '/'
count_slashes = input_string.count('/')
if count_slashes > 1:
    # Tìm vị trí của ký tự '/' cuối cùng
    last_slash_index = input_string.rfind('/')

    # Lưu giá trị từ đầu đến '/' cuối cùng
    result = input_string[0:last_slash_index]

    print(result)
else:
    print("Không có hơn 1 ký tự '/' trong chuỗi.")