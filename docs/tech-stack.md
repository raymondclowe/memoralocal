# MemoraLocal Tech Stack

## Frontend (Client)
- **Core Language:** JavaScript/TypeScript
- **Framework:** React (for web) + React Native (for mobile)
- **Audio Recording:**
  - Web: `MediaRecorder API` or `Recorder.js`
  - Mobile/Desktop: `react-native-audio-recorder-player` or `node-record-lpcm16`
- **Local Storage:** IndexedDB (`idb` or `localForage`)
- **Screenshot Capture:**
  - Web: `html2canvas`
  - Mobile/Desktop: `react-native-view-shot` or `screenshot-desktop`
- **Location Data:**
  - Web: Geolocation API
  - Mobile/Desktop: `react-native-geolocation-service` or `geolocation`
- **Networking:** `fetch` or `axios`

## Backend (Server)
- **Language:** Node.js
- **Framework:** Express.js
- **Transcription:** Faster Whisper or similar tools
- **Storage:** SQLite, PostgreSQL, or MongoDB
- **File Uploads:** Multer or similar middleware
- **API Documentation:** Swagger/OpenAPI

## Cross-Platform Tools
- **Web App:** Vite or Webpack for bundling.
- **Mobile App:** Expo or React Native CLI for building mobile apps.
- **Desktop App:** Electron or Tauri for packaging desktop applications.

## Additional Libraries
- **Queue Management:** `bull` (Node.js) or `react-native-queue`
- **Compression:** `ffmpeg` for audio compression
- **Error Handling:** Sentry or similar tools for monitoring

## Future Considerations
- Explore WebAssembly for performance-critical tasks.
- Use GraphQL for flexible querying.
- Integrate LLMs for advanced summarization and querying.