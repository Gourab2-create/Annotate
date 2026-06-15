import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS to prevent browser blocks if accessed via different IP aliases
CORS(app)

# Define our directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'saved_annotations')

# Ensure the folder for saved XMLs exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
@app.route('/annotation_tool_v2.html')
def serve_tool():
    """Serve the frontend HTML tool."""
    return send_from_directory(BASE_DIR, 'annotation_tool_v2.html')

@app.route('/save_xml', methods=['POST'])
def save_xml():
    """Handle incoming XML save requests from the frontend."""
    data = request.get_json()
    
    if not data or 'filename' not in data or 'xml' not in data:
        return jsonify({"error": "Invalid payload, missing filename or xml"}), 400
    
    # Secure the filename to prevent directory traversal attacks
    filename = os.path.basename(data['filename'])
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    try:
        # Write the XML content to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(data['xml'])
        
        print(f"Successfully saved: {filepath}")
        return jsonify({"status": "success", "file": filename}), 200
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return jsonify({"error": "Failed to save file on server"}), 500

@app.route('/get_latest_annotation', methods=['GET'])
def get_latest_annotation():
    """Fetch all saved annotation files to restore previous data."""
    try:
        # Find all xml files in the saved_annotations directory
        files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.xml')]
        if not files:
            return jsonify({"status": "empty", "message": "No previous data to restore."}), 200
        
        # Get latest modification time for the timestamp
        files.sort(key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)), reverse=True)
        mtime = os.path.getmtime(os.path.join(OUTPUT_DIR, files[0])) # Gets timestamp of newest file
        
        annotations = []
        for f in files:
            with open(os.path.join(OUTPUT_DIR, f), 'r', encoding='utf-8') as fh:
                annotations.append({"file": f, "xml": fh.read()})
            
        return jsonify({"status": "success", "timestamp": mtime, "annotations": annotations, "img_count": len(files)}), 200
    except Exception as e:
        print(f"Error fetching history: {e}")
        return jsonify({"error": "Failed to retrieve history"}), 500

if __name__ == '__main__':
    # Run on 0.0.0.0 to allow other users on the network to access it
    app.run(host='0.0.0.0', port=8080, debug=True)