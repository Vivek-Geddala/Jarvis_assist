import os
import struct

import pyaudio
import pvporcupine


porcupine = pvporcupine.create(
    access_key=os.getenv("PICOVOICE_ACCESS_KEY"),
    keywords=["jarvis"],
)


def is_wake_word():
    print("Waiting for wake word...")

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

    try:
        while True:
            pcm = stream.read(
                porcupine.frame_length,
                exception_on_overflow=False,
            )
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm) >= 0:
                print("Wake word detected")
                return True

    except KeyboardInterrupt:
        print("\nStopping wake word...")

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()