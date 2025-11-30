# check operating system and graphics card

from fastapi import APIRouter


import subprocess
import importlib
import platform
import sys
import os


def get_compatible_flows():
    os_name = platform.system()
    print(f"Operating System: {os_name}")

    if os_name == "Darwin":
        # NOTE: presumes darwin is always Apple Silicon for GPU
        return import_modules("darwin_silicon")
        

    elif os_name == "Linux":
        # ensure that nvidia-smi is installed
        if not subprocess.run(["nvidia-smi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            print("nvidia-smi is not installed")
            exit(1)

        return import_modules("linux_nvidia")
    else:
        print("Unknown")
        exit(1)


def import_modules(dir_name):

    flows = []

    if not os.path.isdir(dir_name):
        print(f"Directory {dir_name} does not exist.")
    else:
        sys.path.insert(0, dir_name)
        for filename in os.listdir(dir_name):
            if filename.endswith(".py") and not filename.startswith("__"):
                modulename = filename[:-3]
                try:
                    importlib.import_module(modulename)
                    print(f"Imported module: {modulename}")
                    flows.append(modulename)
                except Exception as e:
                    print(f"Failed to import module {modulename}: {e}")
        sys.path.pop(0)

    return flows


router = APIRouter()

# return a list of all flows that work on this system
@router.get("/list-flows")
async def list_flows():
    flows = get_compatible_flows()
    return {"message": "Hello from custom API"}
