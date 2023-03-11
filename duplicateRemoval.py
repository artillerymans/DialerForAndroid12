"""
1.去除 msgid="2428457130578359186"等信息
对String.xml文件中的重复的name进行去重
"""
import os
from builtins import list
import re
import shutil
from enum import Enum


class FileUtils:
    class Mode(Enum):
        FILES = 1  # 文件类型
        DIRS = 2  # 目录类型
        ALL = 3  # 全部 包括目录文件

    @staticmethod
    def rm(src: str):
        """
        删除文件或目录
        :param src 表示文件路径 或者目录路径
        :return:
        """
        if os.path.isfile(src):
            os.remove(src)
        else:
            if len(os.listdir(src)) == 0:  # 空目录
                os.removedirs(src)
            else:
                shutil.rmtree(src)

    @staticmethod
    def copy(src: str, dst: str) -> bool:
        """
        复制文件 目标路径存在则直接覆盖
        :param src: 来源路径
        :param dst: 目标路径
        :return:
        """
        srcList = FileUtils.readFile2ListString(src)
        return FileUtils.write(dst, srcList)

    @staticmethod
    def readFile2ListString(path: str) -> list[str]:
        """
        把文件逐行读取到list里面
        :param path:
        :return:
        """
        with open(path, 'r') as file:
            contents = file.readlines()
        return contents

    @staticmethod
    def writeAppendListString2File(src: str, contents: list[str]) -> bool:
        """
        把list里面的数据写入到文件,文件存在直接追加写入,不存在就创建
        :param src: 文件路径
        :param contents:
        :return: false 表示写入失败
        """
        return FileUtils.write(src, contents, 'a')

    @staticmethod
    def write(src: str, contents: list[str], mode: str = 'w'):
        try:
            with open(src, mode) as file:
                file.writelines(contents)
            return True
        except Exception as e:
            # 异常返回 false
            return False

    @staticmethod
    def getFilePrefix(path: str) -> str:
        """
            获取文件名称不包括后缀
            :param path:  绝对路径
            :return: 返回 str
            """
        if len(path) == 0:
            return ""
        name, file_extension = os.path.splitext(path)
        name = os.path.basename(name)
        return name

    @staticmethod
    def getFileSuffix(path: str) -> str:
        """
        获取文件后缀
        :param path:
        :return:
        """
        if len(path) == 0:
            return ""
        name, file_extension = os.path.splitext(path)
        file_extension = file_extension[1:]
        return file_extension

    @staticmethod
    def loopDirs(path: str, filter=None) -> list[str]:
        """
        循环遍历目录下的子目录 不包括文件
        :param path:
        :param filter:
        :return:
        """
        return FileUtils.loop_files_and_dirs(path, FileUtils.Mode.DIRS, filter)

    @staticmethod
    def loop_files_and_dirs(path: str, mode: Mode = Mode.ALL, filter=None) -> list[str]:
        """
        循环遍历目录下的子目录以及文件
        :param path:
        :param filter:
        :param mode Mode.ALL 表示文件/目录 Mode.FILES表示只获取文件 Mode.DIRS表示只获取目录
        :return:
        """
        file_list = []
        for root, dirs, files in os.walk(path):
            if FileUtils.Mode.DIRS != mode:  # 不等于目录模式
                # 循环遍历文件
                for file in files:
                    absolutePath = os.path.join(root, file)
                    if filter is not None:
                        if filter(absolutePath):
                            file_list.append(absolutePath)
                    else:
                        file_list.append(absolutePath)
            if FileUtils.Mode.FILES != mode:  # 不等于 文件模式
                # 循环遍历目录
                for disStr in dirs:
                    absolutePath = os.path.join(root, disStr)
                    if filter is not None:
                        if filter(absolutePath):
                            file_list.append(absolutePath)
                    else:
                        file_list.append(absolutePath)
        return file_list

    @staticmethod
    def loopFiles(path: str, filter=None) -> list[str]:
        """
        循环遍历目录下的文件
        :param filter:过滤函数 返回bool类型的值
        :param path: 文件绝对路径
        :return:返回文件绝对路径列表
        """
        return FileUtils.loop_files_and_dirs(path, FileUtils.Mode.FILES, filter)

    @staticmethod
    def getDirName(path: str) -> str:
        if os.path.isfile(path):
            return FileUtils.getFilePrefix(path)
        else:
            return os.path.basename(os.path.normpath(path))

    @staticmethod
    def getFullName(path: str) -> str:
        """
        获取文件名称包括后缀
        :return:
        """
        return os.path.basename(path)


class LogoutUtils:
    """
    工具类日志打印
    """

    @staticmethod
    def d(*args):
        """
        日志打印的函数
        :param args:
        :return:
        """
        max_index = len(args) - 1
        for index, value in enumerate(args):
            if max_index == index:
                end_value = "\n"
            else:
                end_value = ""
            print(value, end=end_value)


class SystemUtils:
    @staticmethod
    def waitForInput(des: str) -> str:
        """
        等待用户输入
        :param des:
        :return:
        """
        inputValue = input(des)
        return str(inputValue)


class StringUtils:
    @staticmethod
    def isEmpty(value: str) -> bool:
        """
        判断字符是否是None或者长度为0
        :param value:
        :return:
        """
        return value is None or len(value) == 0

    @staticmethod
    def isTrimEmpty(s: str) -> bool:
        """
        判断字符是否为None 或者全部为空格
        :param s:
        :return:
        """
        return s is None or (len(s.strip()) == 0)


def isStartEndString(line: str) -> bool:
    """
    判断是否是 <string 开头 以及 </string>结尾
    :return: false 表示不是  true 表示是
    """
    startStr = "<string"
    endStr = "</string>"
    tempStr = line.strip()  # 清除头尾的空格
    if tempStr.startswith(startStr) and tempStr.endswith(endStr):
        return True
    else:
        LogoutUtils.d("不是是标准的String:", line)
        return False


def isStartEndDimen(line: str) -> bool:
    """
    判断是否是 <dimen 开头 以及 </dimen>结尾
    :return: false 表示不是  true 表示是
    """
    startStr = "<dimen"
    endStr = "</dimen>"
    tempStr = line.strip()  # 清除头尾的空格
    if tempStr.startswith(startStr) and tempStr.endswith(endStr):
        return True
    else:
        LogoutUtils.d("不是是标准的dimen:", line)
        return False


def replaceSpecificContent(src: str):
    """
    根据src 文件路径替换这个文件里面的特定内容
    当前是替换 msgid="xxxxxxx" 等内容  xxx是数字
    以及 stirng name="xxxx" 存在重复名称的资源 替换成一个 ""
    :param src:
    :return:
    """
    pattern = r"msgid=\"(\d+)\""  # 匹配 msgid开头的内容 替换调
    contents = FileUtils.readFile2ListString(src)
    for index, item in enumerate(contents):
        result = re.search(pattern, item)
        if result:
            LogoutUtils.d(result.group(0))
            contents[index] = str(item).replace(result.group(0), "")

    # 获取string name的名称
    repeatMap = {}  # 存放是否会有重复的字典
    patternStringName = r'name="(.+?)"'
    for index, item in enumerate(contents):
        result = re.search(patternStringName, item)
        if result:
            keyStr = result.group(0)
            mapValue = result.group(1)
            # LogoutUtils.d(f'key = {keyStr}, value = {mapValue}')
            if keyStr in repeatMap:  # 已经存在key
                if isStartEndString(item) or isStartEndDimen(item):  # 判断是string开头 string结尾进行下一步替换删除处理
                    LogoutUtils.d("正在替换:", item)
                    contents[index] = ""  # 替换成空的行
                else:
                    # 是重复的但是当前无法判断的 写到一个一个文件里面去
                    FileUtils.write(os.path.join(os.getcwd(), "out.txt"), [f'路径:{src}, 资源:{keyStr}\n'], 'a')
            else:  # 不存在key
                repeatMap[keyStr] = mapValue

    FileUtils.write(src, contents)


def loopDel(path: str, filter=None):
    """
    循环遍历删除特定文件
    :param path:
    :return:
    """
    LogoutUtils.d(f"遍历路径目录:{path}")
    # 忽略大小写的判断
    listFiles = FileUtils.loopFiles(path, filter)
    for item in listFiles:
        LogoutUtils.d(f"开始删除目录/文件 -> :{item}")
        FileUtils.rm(item)


def 去重数据(pathStr: str):
    LogoutUtils.d(f'{pathStr}')  # 换个行
    listFiles = FileUtils.loopFiles(pathStr,
                                    lambda path:
                                    FileUtils.getFilePrefix(str(path)) == "strings"
                                    or FileUtils.getFilePrefix(str(path)) == "dimens")
    for item in listFiles:
        replaceSpecificContent(item)


def 循环删除特定文件(filter=None):
    if filter is None:
        filter = lambda value: FileUtils.getFilePrefix(value).casefold() == "AndroidManifest".casefold()
    pathStr = SystemUtils.waitForInput("输入路径:")
    loopDel(pathStr, filter)


def 删除Res文件目录():
    src = SystemUtils.waitForInput("输入路径:")
    # srcList = FileUtils.loopDirs(src, lambda text: FileUtils.getDirName(text).casefold() == "res".casefold())

    srcList = FileUtils.loopFiles(src,
                                  lambda text: FileUtils.getFilePrefix(text).casefold() == "AndroidManifest".casefold())

    for item in srcList:
        FileUtils.rm(item)


def readCSVFile():
    import csv  # 导包

    """
    android supper 迁移到androidx 针对 java文件以及kt文件
    1.加载映射表
    2.遍历文件 过滤后缀为java或者kt的文件
    3.按行读取文件, 判断当前字符表是否包括 在字典中 在的话 获取Value进行替换
    4.写回文件中去
    :return: 
    """
    # androidx-class-mapping.csv 下载的映射文件
    androidxMap = {}  # 定义个字典类型
    workPath = SystemUtils.waitForInput("输入路径:")
    with open('androidx-class-mapping.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            androidxMap[row[0]] = row[1]
    srcList = FileUtils.loopFiles(workPath, lambda itemPath: FileUtils.getFileSuffix(
        itemPath).casefold() == "java".casefold() or FileUtils.getFileSuffix(itemPath).casefold() == "kt".casefold())
    for item in srcList:
        codeFileList = FileUtils.readFile2ListString(item)
        LogoutUtils.d(f"正在检索文件:${FileUtils.getFilePrefix(item)}")
        for indexValue, strValue in enumerate(codeFileList):
            tempValue = str(strValue).strip()
            if tempValue.startswith("import "):
                for keys, value in androidxMap.items():
                    if keys in tempValue:  # 包含在里面
                        codeFileList[indexValue] = tempValue.replace(keys, value) + "\n"
                    else:  # 不包含在里面
                        pass
            else:
                pass
        FileUtils.write(item, codeFileList)


def loopFilesCopyCustomOutDis():
    """
    过滤特定文件然后复制到特定的目录下
    :return:
    """
    inputDir = SystemUtils.waitForInput("过滤的目录:")
    outDir = SystemUtils.waitForInput("输出目录:")
    protoList = FileUtils.loopFiles(inputDir,
                                    lambda filePath: FileUtils.getFileSuffix(filePath).casefold() == "proto".casefold())
    for item in protoList:
        fileFullName = FileUtils.getFullName(item)
        status = FileUtils.copy(item, os.path.join(outDir, fileFullName))
        LogoutUtils.d(f"${item}", f"文件名称:${fileFullName}", f", 拷贝状态:${status}")


# 循环删除特定文件()
# 删除Res文件目录()
# readCSVFile()
# loopFilesCopyCustomOutDis()
循环删除特定文件(lambda value: FileUtils.getFileSuffix(value).casefold() == "proto".casefold())

