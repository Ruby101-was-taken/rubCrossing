import cx_Freeze

executables = [cx_Freeze.Executable("main.py", icon="icon.ico", base = "Win32GUI")]

includedFiles=["player.png", "icon.png", "logo/", "floor/", "levels/", "ui/", "sound/", "npcs/", "font.ttf"]

packages=["os", "pygame", "asyncio"]

cx_Freeze.setup(
    name="UNANIMATED WOMAN'S ENDING SIMULATOR",
    options={"build_exe": {"packages":packages,
                           "include_files":includedFiles}},
    executables = executables

    )

#python.exe setup.py build