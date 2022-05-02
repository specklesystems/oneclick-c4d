# Cinema 4D 26: One-Click Send to Speckle

## Introduction

This script allows you to send a Cinema4D model to Speckle with one click! Simply paste in a URL, execute the script, and away you go 🚀

![c4d-send](https://user-images.githubusercontent.com/7717434/166261286-eec09b76-2b0d-4651-bddf-8842e6c8b5c1.gif)

In order to achieve this, the script will (1) export your entire model to an `STL` file, (2) convert that file to Speckle, and (3) send and commit the converted mesh.

It is recommended that you have [Speckle Manager](https://speckle.guide/user/manager.html) installed before using this script, however you can also use a [token](https://speckle.guide/dev/tokens.html#personal-access-tokens) to authenticate yourself instead.

## Installation

### Windows

1. Extract the dependencies from `deps_windows_py39.zip`
2. Copy the contents of the extracted `deps_windows_py39` folder into your `%APPDATA%\Maxon\python\python39\libs`

![c4d-deps](https://user-images.githubusercontent.com/7717434/166263648-e0694f8f-f0a9-44ef-8589-024288dd32aa.png)

2. Copy the `send_to_speckle.py` script into your `%APPDATA%\Maxon\Maxon Cinema 4D R26_7DC20B77\library\scripts` (or load it in from wherever you like to save your Cinema4D python scripts)

### Mac

I was not able to get this on an M1 Pro mac, but feel free to try this manual installation out as you may have better luck.

1. Using Python 3.9, `pip install specklepy numpy-stl` into `~/Library/Preferences/MAXON/python39/libs` (**NOTE:** it is critical that you use Python 3.9 as the major version needs to match the one bundled with Cinema4D)
2. Copy the `send_to_speckle.py` script into your C4D scripts folder

## Usage

1. Load up the `send_to_speckle.py` script in the script tab
2. Paste in the url of the stream or branch you want to send to in the `STREAM_URL` field (defaults to `main` branch)
3. Optional: if you _don't_ have [Speckle Manager](https://speckle.guide/user/manager.html) installed with a Speckle account added to it, you can provide an authentication token to `TOKEN` field

![c4d-send](https://user-images.githubusercontent.com/7717434/166261286-eec09b76-2b0d-4651-bddf-8842e6c8b5c1.gif)

Note that C4D may become unresponsive for a minute or two until the operation is complete.
