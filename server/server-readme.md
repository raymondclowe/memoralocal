# MemoraLocal Server

The **MemoraLocal Server** receives and stores audio recordings with metadata.

## Features
- Receives audio chunks and metadata via HTTP POST
- Stores .wav files with matching .json metadata
- Supports CORS for local development
- Runs on any platform with Python 3.11

## Setup
1. Create virtual environment with uv
2. Install Flask and dependencies
3. Run with HTTPS support for geolocation


## Running

`python server/app.py`

`python server/https_server.py`

