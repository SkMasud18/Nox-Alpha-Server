import os
import io
from typing import Dict, Any

class WhisperTurboSTT:
    """
    Hardware-accelerated Speech-To-Text pipeline.
    Utilizes OpenAI's faster-whisper 'turbo' model on NVIDIA CUDA with float16 precision
    for sub-second transcription and native multilingual preservation.
    """

    def __init__(
        self,
        model_name: str = "turbo",
        device: str = "cuda",
        compute_type: str = "float16"
    ):
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self.model = None

    def load_model(self):
        """Lazy loader ensuring GPU resources are initialized on demand."""
        if not self.model:
            from faster_whisper import WhisperModel
            self.model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type=self.compute_type
            )

    def transcribe(self, audio_bytes: bytes) -> Dict[str, Any]:
        """
        Transcribes binary audio payload with Silero Voice Activity Detection (VAD).
        Preserves original spoken language and native scripts (Bengali, Hindi, English, Urdu).
        """
        self.load_model()
        audio_stream = io.BytesIO(audio_bytes)

        # Transcribe with neutral prompt avoiding language bias
        segments, info = self.model.transcribe(
            audio_stream,
            beam_size=1,  # Greedy search for maximum speed
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=5000),
            initial_prompt="Transcribe the spoken audio perfectly in its original language and native script."
        )

        transcript = " ".join([seg.text.strip() for seg in segments]).strip()

        return {
            "text": transcript,
            "detected_language": info.language,
            "language_probability": round(info.language_probability, 3),
            "duration": round(info.duration, 2)
        }
