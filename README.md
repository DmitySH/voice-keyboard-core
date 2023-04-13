# Voice keyboard core

![](https://img.shields.io/badge/python-v3.10-blue)
![](https://img.shields.io/badge/RPC-gRPC-brightgreen)

The core fulfills two main purposes described below.

Core is packaged as executable file and can be used in different operating systems (Windows, Mac OS).

### Part 1
Responsible for the functions of interaction with the user's OS and voice command handling:

- user's microphone listening
- speech2text recognition
- command handling
- virtual keyboard keys pressing

### Part 2
Introduces an API for frontend applications to interact with the command store:

- it is a server running locally
- provides CRUD for commands
- uses gRPC system

Core implementation - Python3.10

_Used by_ **_[evamoorey](https://github.com/evamoorey)_** _in_:\
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=evamoorey&repo=voice-keyboard-app)](https://github.com/DmitySH/voice-keyboard-app)
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=evamoorey&repo=voice-keyboard-windows)](https://github.com/DmitySH/voice-keyboard-windows)

Part of the HSE Moscow 2022-2023 _Software Engineering_ Course Project
