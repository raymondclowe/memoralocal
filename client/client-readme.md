# MemoraLocal Client

The **MemoraLocal Client** handles continuous audio recording and uploading to a local server.

## Features
- Records continuous 10-second audio chunks using MediaRecorder API
- Uploads chunks with metadata in background
- Shows real-time status updates
- Captures GPS coordinates when available

## Setup
1. Install mkcert and generate certificates
2. Serve over HTTPS for geolocation access
