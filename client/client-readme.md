
---

### **`client-readme.md`**

```markdown
# MemoraLocal Client

The **MemoraLocal Client** is the frontend component of the application. It handles audio recording, metadata collection, local storage, and uploading data to the server.

## Features
- Records audio in 10-second chunks.
- Captures metadata (e.g., timestamp, GPS location, screenshots).
- Stores data locally using IndexedDB when offline.
- Uploads data to the server when online.

## Setup
1. Install dependencies:
   ```bash
   npm install