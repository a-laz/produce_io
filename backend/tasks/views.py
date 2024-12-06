import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
import assemblyai as aai
import subprocess
from django.conf import settings

# Initialize AssemblyAI API
aai.settings.api_key = settings.ASSEMBLY_AI_API_KEY
transcriber = aai.Transcriber()

# Set up logging
logger = logging.getLogger(__name__)

class TaskView(APIView):
    """
    API View to handle task creation, transcription, and calendar event creation.
    """

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # Save the Task object with the audio file
            task = serializer.save()

            # Get the absolute URL for the audio file
            audio_file_url = request.build_absolute_uri(task.audio_file.url)

            try:
                # If using ngrok for development, replace localhost URL with ngrok URL
                if 'localhost' in audio_file_url:
                    ngrok_url = 'https://6e67-162-83-137-149.ngrok-free.app'
                    audio_file_url = audio_file_url.replace("http://localhost:8000", ngrok_url)

                # Convert the audio file to WAV if it's in a different format like WEBM
                wav_file_path = self.convert_audio_to_wav(task.audio_file.path)

                # Transcribe the audio using AssemblyAI
                transcript = transcriber.transcribe(wav_file_path)

                # Update the Task with the Transcription
                task.transcription = transcript.text
                task.save()

                # Create a calendar event (Example for Google Calendar)
                calendar_event_id = self.create_calendar_event(task.name, transcript.text)
                task.calendar_event_id = calendar_event_id
                task.save()

                return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Error during task creation or transcription: {str(e)}")
                return Response(
                    {"error": f"Failed to transcribe audio or create event: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        logger.error(f"Invalid data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def convert_audio_to_wav(self, audio_file_path):
        """
        Convert the audio file (e.g., webm) to wav format using ffmpeg
        :param audio_file_path: Path to the original audio file
        :return: Path to the converted wav file
        """
        wav_file_path = audio_file_path.replace(".webm", ".wav")  # Change extension from .webm to .wav

        # Run the ffmpeg command to convert webm to wav
        command = [
            "ffmpeg", 
            "-i", audio_file_path,  # Input file path (webm or other formats)
            "-acodec", "pcm_s16le",  # Audio codec for WAV
            "-ar", "44100",  # Audio sample rate
            "-ac", "2",  # Stereo output
            wav_file_path  # Output file path (wav)
        ]

        try:
            subprocess.run(command, check=True)  # Run the conversion
            return wav_file_path  # Return the converted wav file path
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to convert audio to wav: {e}")

    def create_calendar_event(self, task_name, description):
        """
        Create a calendar event and return its ID.
        Replace this with the actual integration logic
        """
        return "mock-calendar-event-id"
