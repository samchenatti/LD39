import cx_Freeze

executables = [cx_Freeze.Executable("Game.py")]

cx_Freeze.setup(
    name="Roboot",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["Resources"]}},
    executables = executables

    )
