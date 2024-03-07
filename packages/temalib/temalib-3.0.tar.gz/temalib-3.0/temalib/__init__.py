"""
temalib
i do not faking know what to say here!!!!!!!!!
"""

__author__ = "tema5002 <tema5002@gmail.com>"
__version__ = "3.0"
__license__ = "MIT"
__copyright__ = "2024, tema5002"
__short_description__ = "a library that works with files i guess"

from typing import Any
import _io

def is_online(guild, user_id: int) -> bool:
    """
    guild: [disnake.Guild, nextcord.Guild]
    returns True if member is not offline (online, idle, etc.)
    else returns False

    also returns False if member was not found on guild
    """
    try:
        import disnake
        memberOnline = False

        if member := guild.get_member(user_id):
            memberOnline = (member.status != disnake.Status.offline)
        return memberOnline
    except ModuleNotFoundError:
        try:
            import nextcord
            memberOnline = False

            if member := guild.get_member(user_id):
                memberOnline = (member.status != nextcord.Status.offline)
            return memberOnline
        except ModuleNotFoundError as err:
            raise "Neither disnake or nextcord modules was found" from err

def smthfile(fp, readingmode) -> _io.TextIOWrapper:
    import codecs
    """
    returns file with utf-8 encoding and uses write mode you want to use
    """
    return codecs.open(fp, readingmode, encoding="utf-8")

def openfile(fp) -> _io.TextIOWrapper:
    """
    returns file with utf-8 encoding
    """
    return smthfile(fp, "r")

def editfile(fp) -> _io.TextIOWrapper:
    """
    returns file with utf-8 encoding and uses write mode
    """
    return smthfile(fp, "w")

def get_folder_path(caller: str, *args: list[Any], **kwargs) -> str:
    import os
    """
    PLEASE USE __file__ FOR caller FOR FRICKS SAKE 🍶🤧
    you can use anything for args but i highly recommend using str and int
    returns [folder where caller is]/args"
    for example if caller is "D:/kreisi program/main.py"
    get_folder_path(__file__, "folder 1", "folder 2") will return
    "D:/kreisi program/folder 1/folder 2"
    if any folder doesn't exist it will be created
    do get_folder_path(..., create_folders=False) if you won't
    """
    create_folders = kwargs.get("create_folders")
    if create_folders is None:
        create_folders = True

    args = map(str, args)
    folder_dir = os.path.dirname(caller)

    for f in args:
        folder_dir = os.path.join(folder_dir, f)
        if create_folders and not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
    return folder_dir

def get_file_path(caller: str, *args: list[Any], **kwargs) -> str:
    import os
    """
    PLEASE ALSO USE __file__ FOR caller FOR FUCKS CAKE 🍰🍰🍰🍰🍰🍰🍰
    yes you also can use anything for args but i highly recommend using str and int
    returns [folder where caller is]/args"
    for example if caller is "D:/kreisi program/main.py"
    get_file_path(__file__, "folder", "opinion on mars.txt") will return
    "D:/kreisi program/folder/opinion on mars.txt"

    if file or folder doesn't exist it will be created

    set create_folders to False if you won't it to be created

    set create_file to False if you won't it to be created
    you can set it to any str value if you want it to be
    wrote when file created (useful in json files so you
    can write {})
    """
    create_folders = kwargs.get("create_folders")
    create_file = kwargs.get("create_file")
    if create_folders is None:
        create_folders = True
    if create_file is None:
        create_file = ""
    args = map(str, args)
    folder_dir = get_folder_path(caller, *args[:-1], create_folders=create_folders)

    filepath = os.path.join(folder_dir, args[-1])
    if create_file != False and not os.path.exists(filepath):
        with editfile(filepath) as f:
            f.write(create_file)

    return filepath

def add_line(fp: str, line: str) -> None:
    """
    adds line to the of the file
    for example if file already has 2 strings
    add_line("opinion on mars.txt", "MARS IS A STUPID PLANET!!!!!!")
    will do

    already existsing string in file 1
    already existsing string in file 2
    MARS IS A STUPID PLANET!!!!!!
    """
    with smthfile(fp, "a+") as file:
        file.seek(0)
        if file.read():
            file.seek(0, 2)
            file.write("\n")
        file.write(line)

def remove_line(fp: str, line: str) -> None:
    """
    removes line to the of the file
    for example if file is from previous example
    remove_line("opinion on mars.txt", "already existsing string in file 1")
    will do

    already existsing string in file 2
    MARS IS A STUPID PLANET!!!!!!
    """
    editfile(fp).write("\n".join(i for i in openfile(fp).read().split("\n") if i != line))

def listpaths(fp: str) -> list[str]:
    """
    lists paths of files in folder

    >>> import temalib
    >>> temalib.listpaths("C:\\path\\to\\folder")
    ['C:\\path\\to\\folder\\banana.js', 'C:\\path\\to\\folder\\apple.js', 'C:\\path\\to\\folder\\ananas.js']
    """
    return [os.path.join(fp, i) for i in os.listdir(fp)]

def generate_ip(name: str) -> str:
    """
    generates random ip
    >>> import temalib
    >>> temalib.generate_ip("kreisi")
    '208.170.82.78'
    """
    import random
    random.seed(name)
    return ".".join([str(random.randint(0,255)) for _ in range(4)])