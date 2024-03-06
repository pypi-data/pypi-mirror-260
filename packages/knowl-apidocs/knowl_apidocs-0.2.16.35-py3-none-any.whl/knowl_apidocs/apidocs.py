import os
import platform
import subprocess
import sys
import argparse

import requests

from .version import VERSION


def remove_quotes(s):
    return s.replace('"', "").replace("'", "").replace("\`", "")


def detect_os():
    current_os = platform.system()
    if current_os == "Linux":
        return "linux"
    elif current_os == "Darwin":
        return "mac"
    else:
        raise RuntimeError(f"This script is not supported on {current_os}. Please run it on Linux, or macOS.")


def get_url(os, version, is_legacy):
    url = f"https://releases.knowl.io/api-docs/apidocs_{os}_v{version}"
    binary_name = f"apidocs_{os}_v{version}"
    if is_legacy:
        url = url + "_legacy"
        binary_name = binary_name + "_legacy"
    return url, binary_name


def run_subprocess(command, name="Operation"):
    try:
        binary_process = subprocess.Popen(
            command,
            universal_newlines=True,
        )
        binary_process.wait()
        if binary_process.returncode == 0:
            print(f"{name} completed successfully.")
        else:
            print(f"{name} failed with return code {binary_process.returncode}.")
            return 1
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error while running the script: {e}")
        return 1

def download_file(url, destination):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Downloaded: {destination}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def main():
 
    # Version is at the start because directory argument is compulsory and parse_args gives error with ONLY the -v argument
    if len(sys.argv) < 2:
        raise RuntimeError("Path to Repo not provided")
    if sys.argv[1] == "-v" or sys.argv[1] == "--version":
        print(VERSION)
        return
    
    # Taking care of hidden flag
    hidden_flag = "-op"
    output_prompt = hidden_flag in sys.argv
    if output_prompt:
        sys.argv.remove(hidden_flag)
    
    # parser is used only to elegantly support the -h flag
    parser = argparse.ArgumentParser(description="Generate external API documentation")
    parser.add_argument("-v", "--version", action="store_true", help="Show version and exit")
    parser.add_argument("directory", help="Directory path of the repository")
    parser.add_argument("-s", "--settings", default=None, help="Settings module of the project of the form <package>.<module>.settings")
    parser.add_argument("-sp", "--starting-point", default=None, help="Path to the starting point of the project")
    parser.add_argument("-u", "--url-file", default=None, help="Path of the file containing URLs")
    parser.parse_args()    

    if output_prompt:
        sys.argv.append(hidden_flag)
    
    if sys.argv[1].startswith("-"):
        print("Incorrect Arguments provided")
        exit(1)
    repo = sys.argv[1]
    package_path = os.path.dirname(os.path.abspath(__file__))
    current_os = detect_os()
    version = VERSION
    is_legacy = current_os == "linux" and sys.version_info < (3, 10)
    url, binary_name = get_url(current_os, version, is_legacy)
    binary_path = os.path.join(package_path, binary_name)
    if os.path.exists(binary_path):
        print("Binary file already exist.")
    else:
        download_file(url, binary_path)
    command = ["chmod", "+x", binary_path]
    run_subprocess(command, "Granting Executable Permission")
    command = [binary_path, repo, "-p", os.path.dirname(os.path.abspath(__file__))]
    if len(sys.argv) > 2:
        other_commands = sys.argv[2:]
        command.extend(other_commands)
    run_subprocess(command, "Document Generation")


if __name__ == "__main__":
    main()
