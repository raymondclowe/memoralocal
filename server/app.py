from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import json
import glob
from faster_whisper import WhisperModel
from queue import Queue
import threading
import time

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
TRANSCRIPT_FOLDER = 'transcripts'
processing_queue = Queue()
# model = WhisperModel("tiny", device="cpu", compute_type="int8") # tiny works and is fast but accuracy is very low
# model = WhisperModel("base.en", device="cpu", compute_type="int8") # tiny works and is fast but accuracy is very low
model = WhisperModel("small.en", device="cpu", compute_type="int8") # tiny works and is fast but accuracy is very low
# model = WhisperModel("tiny.en", device="cpu", compute_type="int8") # tiny works and is fast but accuracy is very low
# model = WhisperModel("distil-large-v2", device="cpu", compute_type="int8") # distill large v2 is accurate but slow and is English only

# Define processing_status in global scope
processing_status = {
    'current_file': None,
    'files_processed': 0,
    'files_pending': 0,
    'last_transcript': None
}

# Add these global variables at the top with the other globals
current_transcript = {
    'text': '',
    'last_update': None,
    'base_metadata': None,
    'output_file': None
}

for folder in [UPLOAD_FOLDER, TRANSCRIPT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created directory: {os.path.abspath(folder)}")

def update_status(status_update):
    global processing_status
    print(f"Updating status: {status_update}")
    processing_status.update(status_update)

def get_latest_transcript_info():
    transcript_files = glob.glob(f"{TRANSCRIPT_FOLDER}/*.txt")
    if not transcript_files:
        return None, None
    latest_file = max(transcript_files, key=os.path.getmtime)
    return latest_file, os.path.getmtime(latest_file)

def should_append_transcript(current_time):
    latest_file, latest_mtime = get_latest_transcript_info()
    if not latest_file:
        return False
    return (current_time - latest_mtime) <= 30  # 30 seconds threshold

def process_audio_files():
    global current_transcript
    
    while True:
        wav_files = glob.glob(f"{UPLOAD_FOLDER}/*.wav")
        update_status({'files_pending': len(wav_files)})
        
        current_time = time.time()
        # Check if we need to reset due to time gap (60 seconds passed)
        if (current_transcript['last_update'] and 
            current_time - current_transcript['last_update'] > 60):
            current_transcript = {
                'text': '',
                'last_update': None,
                'base_metadata': None,
                'output_file': None
            }
        
        for wav_path in wav_files:
            json_path = wav_path.replace('.wav', '.json')
            
            # Clean up orphaned files
            if not os.path.exists(json_path):
                os.remove(wav_path)
                print(f"Removed orphaned WAV file: {wav_path}")
                continue

            update_status({'current_file': os.path.basename(wav_path)})
            print(f"\nProcessing: {wav_path}")
            
            # Load metadata
            with open(json_path, 'r') as f:
                metadata = json.load(f)
            
            # Transcribe audio
            segments, info = model.transcribe(wav_path)
            transcript = "\n".join([seg.text for seg in segments])
            
            if not transcript.strip():
                print(f"Empty transcript, skipping: {wav_path}")
                continue

            # Handle transcript storage
            if not current_transcript['text']:
                # Start new transcript file
                current_transcript['base_metadata'] = metadata
                current_transcript['output_file'] = os.path.join(
                    TRANSCRIPT_FOLDER, 
                    os.path.basename(wav_path).replace('.wav', '.txt')
                )
                current_transcript['text'] = f"""Recording from {metadata['timestamp']}
Username: {metadata['username']}
Location: {metadata.get('gps_lat', 'N/A')}, {metadata.get('gps_lon', 'N/A')}

Transcript:
{transcript}"""
            else:
                # Append to existing transcript
                current_transcript['text'] += f"\n{transcript}"
            
            # Update timestamp and save to file
            current_transcript['last_update'] = current_time
            with open(current_transcript['output_file'], 'w', encoding='utf-8') as f:
                f.write(current_transcript['text'])
            
            # Clean up original files
            os.remove(wav_path)
            os.remove(json_path)
            print(f"Processed and removed: {wav_path} and {json_path}")
            
            update_status({
                'files_processed': processing_status['files_processed'] + 1,
                'last_transcript': current_transcript['output_file']
            })
        
        time.sleep(5)






# Start processing thread
processing_thread = threading.Thread(target=process_audio_files, daemon=True)
processing_thread.start()


@app.route('/latest', methods=['GET'])
def get_latest_transcript():
    transcript_files = glob.glob(f"{TRANSCRIPT_FOLDER}/*.txt")
    if not transcript_files:
        return jsonify({'message': 'No transcripts available'})
    
    # Sort by modification time, newest first
    latest_file = max(transcript_files, key=os.path.getmtime)
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return jsonify({
        'filename': os.path.basename(latest_file),
        'content': content,
        'timestamp': os.path.getmtime(latest_file)
    })



@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        'status': processing_status,
        'transcripts': glob.glob(f"{TRANSCRIPT_FOLDER}/*.txt")
    })

@app.route('/upload', methods=['POST'])
def upload_audio():
    print("\n=== New Upload Request ===")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request files: {request.files}")
    print(f"Request form data: {dict(request.form)}")

    audio_file = request.files.get('audio')
    if not audio_file:
        print("ERROR: No audio file in request")
        return jsonify({'error': 'No audio file provided'}), 400

    metadata = {
        'timestamp': datetime.utcnow().isoformat(),
        'client_ip': request.remote_addr,
        'username': request.form.get('username', 'anonymous'),
        'gps_lat': request.form.get('gps_lat'),
        'gps_lon': request.form.get('gps_lon'),
        'device_info': request.user_agent.string,
        'content_type': audio_file.content_type,
        'file_size': 0
    }

    base_filename = f"{metadata['timestamp'].replace(':', '-')}_{metadata['username']}"
    audio_filepath = os.path.join(UPLOAD_FOLDER, f"{base_filename}.wav")
    json_filepath = os.path.join(UPLOAD_FOLDER, f"{base_filename}.json")
    
    print(f"Saving audio to: {audio_filepath}")
    audio_file.save(audio_filepath)
    metadata['file_size'] = os.path.getsize(audio_filepath)
    
    print(f"Saving metadata to: {json_filepath}")
    with open(json_filepath, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Files saved successfully. Audio size: {metadata['file_size']} bytes")
    return jsonify({
        'status': 'success',
        'audio_file': f"{base_filename}.wav",
        'metadata_file': f"{base_filename}.json",
        'metadata': metadata
    })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)