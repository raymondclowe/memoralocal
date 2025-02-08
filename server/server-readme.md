
---

### **`server-readme.md`**

```markdown
# MemoraLocal Server

The **MemoraLocal Server** is the backend component of the application. It handles receiving uploaded data, processing it (e.g., transcription), and storing it for later querying.

## Features
- Receives audio chunks, metadata, and screenshots from clients.
- Processes audio using transcription services (e.g., Faster Whisper).
- Stores data in a structured repository (e.g., database or file system).
- Provides APIs for querying stored data.

## Setup
1. Install dependencies:
   ```bash
   npm install