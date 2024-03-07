import os

def delete_dot_underscore_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith("._"):
                file_path = os.path.join(root, file)
                os.remove(file_path)


if __name__ == "__main__":
    # 指定要删除文件的目录
    directory_to_clean = "/data/datadata/#datasets/VAD-datasets/"

    delete_dot_underscore_files(directory_to_clean)
