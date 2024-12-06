# Project Setup and Usage

## Getting Started

This project consists of a frontend built with React and a backend built with Django. Follow the instructions below to set up and run both servers.

### Prerequisites

- Python 3.x
- Node.js and npm
- FFmpeg (for audio file conversions)
- ngrok (for exposing local servers)

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd path/to/backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install FFmpeg:**
   - On Windows, download from [FFmpeg official site](https://ffmpeg.org/download.html).
   - On macOS, use Homebrew:
     ```bash
     brew install ffmpeg
     ```
   - On Linux, use:
     ```bash
     sudo apt-get install ffmpeg
     ```

6. **Start the backend server:**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd path/to/frontend
   ```

2. **Install frontend dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend server:**
   ```bash
   npm start
   ```

### Running ngrok

To expose your local backend server to the internet, you can use ngrok:

1. **Install ngrok from [ngrok.com](https://ngrok.com/download).**

2. **Run ngrok on the port your backend server is using (default is 8000):**
   ```bash
   ngrok http 8000
   ```

3. **Update the URL in `tasks/views.py` with the ngrok URL provided.** 
   - Look for the line in the `post` method where the `audio_file_url` is modified:
     ```python
     if 'localhost' in audio_file_url:
         ngrok_url = 'https://your-ngrok-url-here'
         audio_file_url = audio_file_url.replace("http://localhost:8000", ngrok_url)
     ```

Using ngrok allows the AssemblyAI API to work effectively by exposing your local server to the internet, enabling it to receive requests from the AssemblyAI service.

### Additional Information

- **Transcription and Calendar Events:** The backend uses AssemblyAI for audio transcription and can create calendar events. Ensure you have the correct API keys set in your Django settings.

- **Error Handling:** If you encounter issues during transcription or event creation, check the logs for detailed error messages.

## Learn More

- [Django Documentation](https://docs.djangoproject.com/en/stable/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [AssemblyAI Documentation](https://docs.assemblyai.com/)
