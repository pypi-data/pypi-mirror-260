def read_as_str(path: str, limit: int = None) -> str:
    """
    以字符串格式读取指定文件的所有内容

    :param path: 文件路径
    :param limit: 字符长度限制
    :return: 读取出的字符串
    """
    with open(path) as file:
        if limit is None:
            details = file.read()
        else:
            details = file.read(limit)
    return details


if __name__ == '__main__':
    details = read_as_str('FileUtil.py', 10)
    print(details)
