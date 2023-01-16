# voice-keyboard-core
The repository contains the functional core of the Voice Keyboard application


The core consists of two parts, each of which is packaged in an executable file. These two files, depending on the packaging, can be used in different operating systems (Windows, Mac OS)

**Part 1** is responsible for the functions of interaction with the user's OS and voice command handling:
- user's microphone listening
- speech2text recognition
- command handling
- virtual keyboard keys pressing

**Part 2** introduces an API for frontend applications to interact with the command store:
- it is a server running locally
- provides CRUD for commands
- uses gRPC system

Core implementation - Python3.10

Part of the HSE Moscow 2022-2023 Software Engineering Course Project
