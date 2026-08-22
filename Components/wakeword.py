import os
import time
from importlib import import_module

try:
    pyaudio = import_module("pyaudio")
except ImportError:
    pyaudio = None
import numpy as np
from scipy.signal import resample_poly

try:
    Model = import_module("openwakeword.model").Model
except ImportError:
    Model = None


# --------------------------------------------------
# Jarvis Wake Word Detector
# Uses openWakeWord instead of Picovoice Porcupine
# --------------------------------------------------

model = None
pa = None
stream = None

RATE = 16000
CHUNK = 1280  # 80 ms of audio; the size recommended by openWakeWord.
WAKE_WORD_THRESHOLD = float(os.getenv("WAKE_WORD_THRESHOLD", "0.30"))
MICROPHONE_DEVICE_INDEX = os.getenv("MICROPHONE_DEVICE_INDEX")


def _get_wakeword_model():
    global model

    if model is not None:
        return model

    if Model is None:
        raise RuntimeError(
            "openWakeWord is required for wake-word detection. "
            "Install it with: python -m pip install openwakeword"
        )

    print("Loading openWakeWord...")

    model = Model(
        wakeword_models=["hey_jarvis"],
        inference_framework="onnx",
        # The VAD gate can suppress valid wake words on some Windows microphone
        # drivers. The wake-word model itself is the primary detector here.
        vad_threshold=0.0,
    )

    print("openWakeWord loaded successfully.")

    return model


def is_wake_word():
    global pa, stream

    print("Waiting for wake word...")

    if pyaudio is None:
        raise RuntimeError(
            "PyAudio is required for wake-word detection. "
            "Install it with: python -m pip install pyaudio"
        )

    detector = _get_wakeword_model()

    pa = pyaudio.PyAudio()

    device_index = None
    if MICROPHONE_DEVICE_INDEX:
        try:
            device_index = int(MICROPHONE_DEVICE_INDEX)
        except ValueError as exc:
            raise RuntimeError(
                "MICROPHONE_DEVICE_INDEX must be a numeric PyAudio device index."
            ) from exc

    device = (
        pa.get_device_info_by_index(device_index)
        if device_index is not None
        else pa.get_default_input_device_info()
    )
    print(f"Using microphone: {device['name']} (index {device['index']})")
    print(
        f"Say 'Hey Jarvis' clearly. Wake threshold: {WAKE_WORD_THRESHOLD:.2f}. "
        "Press Ctrl+C to stop."
    )

    input_rate = int(device["defaultSampleRate"])
    input_chunk = round(input_rate * CHUNK / RATE)
    print(f"Capturing at {input_rate} Hz and converting to {RATE} Hz for detection.")

    try:
        stream = pa.open(
            # Some Windows devices only expose their native rate (often 44.1 kHz).
            # Capture at that rate and convert to the 16 kHz required by openWakeWord.
            rate=input_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=input_chunk,
            input_device_index=device_index,
        )
    except OSError as exc:
        pa.terminate()
        pa = None
        raise RuntimeError(
            "Windows could not open the selected microphone. In Settings > Privacy "
            "& security > Microphone, turn on Microphone access and Let desktop apps "
            "access your microphone. Then confirm the microphone works in Settings > "
            "System > Sound > Input and restart MyJarvis."
        ) from exc

    try:
        last_status_at = 0.0
        while True:

            audio_data = stream.read(
                input_chunk,
                exception_on_overflow=False,
            )

            audio_frame = np.frombuffer(
                audio_data,
                dtype=np.int16,
            )

            if input_rate != RATE:
                # resample_poly keeps the conversion stable and avoids the
                # distortion produced by simply dropping samples.
                audio_frame = resample_poly(
                    audio_frame.astype(np.float32),
                    RATE,
                    input_rate,
                ).astype(np.int16)

            predictions = detector.predict(audio_frame)

            # Get Hey Jarvis confidence
            score = predictions.get("hey_jarvis", 0.0)

            # This lightweight diagnostic confirms the app is receiving sound
            # without flooding the terminal on every 80 ms audio frame.
            now = time.monotonic()
            if now - last_status_at >= 2:
                level = float(np.abs(audio_frame.astype(np.int32)).mean())
                print(f"Mic level: {level:.0f} | Hey Jarvis score: {score:.3f}")
                last_status_at = now

            if score >= WAKE_WORD_THRESHOLD:
                print(f"Wake word detected! Score: {score:.2f}")

                # Reset detector to prevent immediate
                # repeated activation.
                detector.reset()

                return True

    except KeyboardInterrupt:
        print("\nStopping wake word...")

    except Exception as e:
        print(f"Wake word error: {e}")
        return False

    finally:

        if stream is not None:
            stream.stop_stream()
            stream.close()
            stream = None

        if pa is not None:
            pa.terminate()
            pa = None
