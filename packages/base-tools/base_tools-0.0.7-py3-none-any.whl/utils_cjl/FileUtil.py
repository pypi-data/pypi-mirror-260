import os
import zipfile


def zip_files(paths: list[str], out_path: str, compression: int = zipfile.ZIP_STORED):
    """
    压缩指定文件
    :param paths: 文件路径组成的列表
    :param out_path: 输出的压缩文件的路径
    :param compression: 压缩方式
                ZIP_STORED = 0 # 不压缩
                ZIP_DEFLATED = 8
                ZIP_BZIP2 = 12
                ZIP_LZMA = 14
    :return:
    """
    zip_file = zipfile.ZipFile(out_path, "w", compression, allowZip64=True)

    for path in paths:
        pre_len = len(os.path.dirname(path))
        arc_name = path[pre_len:].strip(os.path.sep)
        zip_file.write(path, arc_name)
    zip_file.close()