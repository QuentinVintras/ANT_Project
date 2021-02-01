from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Ant Simulator",
    version = "1",
    description = "Ant simulator programm",
    executables = [Executable("ui.py")],
)

