import pyaudio
import wave


# 设置音频参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 512
RECORD_SECONDS = 5

# 写输出地址
WAVE_OUTPUT_FILENAME = "" 


# 初始化 PyAudio
audio = pyaudio.PyAudio()

# 获取系统中的输入设备信息
for i in range(audio.get_device_count()):
    device_info = audio.get_device_info_by_index(i)
    print("Device {}: {}".format(i, device_info["name"]))

# 选择你想要的输入设备
input_device_index = int(input("Enter input device index: "))

# 打开输入流
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=input_device_index)

print("* Recording audio...")

frames = []

# 录制音频
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* Done recording")

# 关闭输入流
stream.stop_stream()
stream.close()
audio.terminate()

# 保存录制的音频到 WAV 文件
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print("Audio saved to", WAVE_OUTPUT_FILENAME)


