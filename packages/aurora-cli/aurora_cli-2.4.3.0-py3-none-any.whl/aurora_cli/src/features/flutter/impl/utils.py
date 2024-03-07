"""
Copyright 2024 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
from pathlib import Path

GDB_INIT_DATA = '''handle SIGILL pass nostop noprint
set remote exec-file /usr/bin/{package}'''

GDB_VSCODE_DATA = r'''{{
    "version": "0.2.0",
    "configurations": [
        {{
            "name": "Attach with GDB",
            "type": "cppdbg",
            "request": "launch",
            "program": "{rmp_path}",
            "MIMode": "gdb",
            "miDebuggerPath": "/usr/bin/gdb-multiarch",
            "miDebuggerServerAddress": "{ip}:{port}",
            "useExtendedRemote": true,
            "cwd": "${{workspaceRoot}}"
         }}
    ]
}}'''

DART_VSCODE_DATA = r'''{{
    "version": "0.2.0",
    "configurations": [
        {{
            "name": "Attach with Debug",
            "type": "dart",
            "request": "attach",
            "vmServiceUri": "{vm_service_uri}",
            "program": "{main_path}",
        }},
    ]
}}'''

CUSTOM_DEVICE_CODE_DATA = r'''{{
  "custom-devices": [
    {{
      "id": "aurora",
      "label": "Aurora",
      "sdkNameAndVersion": "5.0",
      "platform": null,
      "enabled": true,
      "ping": [
        "ping",
        "-c",
        "1",
        "-w",
        "1",
        "{ip}"
      ],
      "pingSuccessRegex": null,
      "postBuild": null,
      "install": [
        "scp",
        "-r",
        "-o",
        "BatchMode=yes",
        "${{localPath}}",
        "defaultuser@{ip}:/tmp/${{appName}}"
      ],
      "uninstall": [
        "ssh",
        "-o",
        "BatchMode=yes",
        "defaultuser@{ip}",
        "rm -rf \"/tmp/${{appName}}\""
      ],
      "runDebug": [
        "ssh",
        "-o",
        "BatchMode=yes",
        "defaultuser@{ip}",
        "/usr/bin/{package}"
      ],
      "forwardPort": [
        "ssh",
        "-o",
        "BatchMode=yes",
        "-o",
        "ExitOnForwardFailure=yes",
        "-L",
        "127.0.0.1:${{hostPort}}:127.0.0.1:${{devicePort}}",
        "defaultuser@{ip}",
        "echo 'Port forwarding success'; read"
      ],
      "forwardPortSuccessRegex": "Port forwarding success",
      "screenshot": null
    }}
  ]
}}'''


# Get list installed flutter
def get_list_flutter_installed() -> []:
    path = Path.home() / '.local' / 'opt'
    folders = [folder for folder in os.listdir(path) if os.path.isdir(path / folder)
               and 'flutter-' in folder
               and os.path.isfile(path / folder / 'bin' / 'flutter')]
    folders.sort(reverse=True)
    return [v.replace('flutter-', '') for v in folders]


# Get keys form spec file
# Name
# Version
# Release
def get_spec_keys(file: Path) -> [None, None, None]:
    result = [None, None, None]
    if not file.is_file():
        return [None, None, None]
    with open(file, 'r') as file:
        for line in file:
            if 'Name:' in line:
                result[0] = line.replace('Name: ', '').strip()
            if 'Version:' in line:
                result[1] = line.replace('Version: ', '').strip()
            if 'Release:' in line:
                result[2] = line.replace('Release: ', '').strip()
    return result
