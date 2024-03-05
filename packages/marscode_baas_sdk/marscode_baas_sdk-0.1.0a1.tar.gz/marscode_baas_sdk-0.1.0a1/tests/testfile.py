from io import BytesIO
import sys
import os
sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))] + sys.path
import marscode_baas_sdk.file as file

# upload file

# fd = file.upload("hel lo%@$!@#$%^&*()\.txt", b'hello world')
fd = file.upload("hello_new.txt", b'hello world1230900005')

print("[paas] ①  upload success")
print("          file id: ", fd.id)
print("          file url: ", fd.url)

# download file with file id
resp = file.download(fd.id)
print("[paas] ②  download success")
print("          file content: ", resp.decode("utf8"))
# # delete file
# file.delete(fd.id)
# print("[paas] ③  delete success")
# # try to dwonload deleted file, this option should failed with FileNotFound
# try:
#     file.download(fd.id)
# except file.FileNotFound:
#     print("[paas] ④  can not download deleted file!")




# resp = file.list_file(1, 10, "h")

# resp = file.list_file()
resp = file.list_file(1, 10, "hello")

print("[paas] ⑤  list success")
print("          resp paginate: ", resp.paginate.page_number, resp.paginate.page_size, resp.paginate.total_count)
for file_desc in resp.data:
    print("          resp data: ", file_desc.created_at, file_desc.id, file_desc.name, file_desc.size, file_desc.updated_at, file_desc.url)