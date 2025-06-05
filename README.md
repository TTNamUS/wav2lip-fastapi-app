# Real-time Lip-syncing WebSocket API

## Description

This project provides a real-time lip-syncing API using WebSockets, powered by the Wav2Lip model. Users can upload a face image and an audio file, and receive a lip-synced video in response. The backend is built with FastAPI and leverages deep learning models for accurate and high-quality lip synchronization.

## Features

- Real-time lip-syncing via WebSocket API
- Supports image and audio file uploads
- Returns generated video with synchronized lips
- Easy-to-use web frontend for quick testing
- Powered by the state-of-the-art Wav2Lip model

## How It Works

1. The client sends a face image and an audio file (both base64-encoded) to the WebSocket endpoint.
2. The backend receives the data, processes it with the Wav2Lip model, and generates a video with synchronized lips.
3. The server responds with a base64-encoded video file.
4. The client decodes and displays or saves the video.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/TTNamUS/wav2lip-fastapi-app.git
   cd wav2lip-fastapi-app
   ```

2. **Install dependencies:**  
    - Install [uv](https://github.com/astral-sh/uv) (Python package manager)
        ```sh
        pip install uv
        ```

    - Setup dependencies from `pyproject.toml`
        ```sh
        uv sync
        ```

3. **Download the Wav2Lip model checkpoint:**
   - Place the `Wav2Lip.pth` file in the `checkpoints/` directory.
   - See [checkpoints/README.md](checkpoints/README.md) for details.

4. **Start the server:**
   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

5. **Access the web demo:**
   - Open [http://localhost:8000](http://localhost:8000) in your browser.

## Running with Docker
```sh
# Build and start with Docker
docker-compose up --build

# Open your browser and go to web demo:
http://localhost:8000
```

### Frontend Demo
Face Image: [andrew-ng.png](andrew-ng.png)  
Audio: [test.wav](test.wav)  

=> Output: [output.mp4](output.mp4)
![Frontend Demo Screenshot](frontend_screenshot.png)

## Usage

### WebSocket API

- **Endpoint:** `/ws/lipsync`
- **Protocol:** WebSocket

**Request Payload:**
```json
{
  "base64_image": "<base64-encoded image>",
  "base64_audio": "<base64-encoded audio>"
}
```

**Response:**
- On success: `{ "status": "success", "video": "<base64-encoded mp4>" }`
- On error: `{ "status": "error", "detail": "<error message>" }`

### Example - Testing with test.py

You can use the provided `test.py` script to test the WebSocket API.

**Usage:**

```sh
uv run test.py
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements and bug fixes.

## License

This project is for research and personal use only. For commercial use, please contact the authors. See [app/models/Wav2Lip/README.md](app/models/Wav2Lip/README.md) for details and citation requirements.