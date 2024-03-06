import zipfile


def unzip_file(zip_path, target_dir):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        # 设置解压时的编码为CP437（Windows默认），或者尝试UTF-8编码
        for name in zip_ref.namelist():
            try:
                zip_ref.extract(name, target_dir)
            except UnicodeDecodeError:
                # 如果CP437解码失败，则尝试使用UTF-8
                decoded_name = name.encode("cp437").decode("utf-8")
                zip_ref.extract(decoded_name, target_dir)
