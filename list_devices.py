import pyaudio

p = pyaudio.PyAudio()

print("Available devices:")
for i in range(p.get_device_count()):
    print(f"{i}: {p.get_device_info_by_index(i)['name']}")

p.terminate()
