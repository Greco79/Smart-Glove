import os
import pyaudio
import wave
import openai
from google.cloud import texttospeech_v1
import sys
import pygame  
import io

# 初始化 pygame
pygame.init()

# 设置 Google Cloud 认证凭据的环境变量
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""

def text_to_speech(text):
    # 创建文本到语音客户端
    client = texttospeech_v1.TextToSpeechClient()

    # 设置语音合成参数
    synthesis_input = texttospeech_v1.SynthesisInput(text=text)
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-F",
        ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3,
        pitch=0,
        speaking_rate=0.9
    )

    # 调用文本到语音 API
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # 通过Pygame播放语音
    pygame.mixer.music.load(io.BytesIO(response.audio_content))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# 用pygame替换原有的play_audio函数
def play_audio(file_path):
    # 初始化pygame混音器
    pygame.mixer.init()
    # 加载音频文件
    pygame.mixer.music.load(file_path)
    # 播放音频文件
    pygame.mixer.music.play()
    # 等待播放完成
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# 设置 OpenAI API 密钥
openai.api_key = ""

def audio_to_text(audio_file_path, output_file_path):
    # 读取录音文件
    with open(audio_file_path, "rb") as audio_file:
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        # 获取转录的文本内容
        transcription_text = transcription.text
        
        # 打印转录的文本内容
        print("Transcription:"+transcription_text)
        #transcription_text="what's your name."
        
        # 将转录的文本内容保存到文本文件
        with open(output_file_path, "w") as output_file:
            output_file.write(transcription_text)
        
        return transcription_text

if __name__ == "__main__":
    # 获取录音文件路径
    audio_file_path = ""
    
    # 定义输出文本文件路径
    output_file_path = ""

    speak_file_path = ""

    # 将录音转换为文本并保存到文本文件
    transcription_text=audio_to_text(audio_file_path, output_file_path)

    content = transcription_text.strip()  # 每次@You输入的内容是录音转录的文本
     # 设置初始对话消息
    initial_message = "You are Jade, a computer engineering student at the National University of Singapore (NUS). \
                    Currently, you're in the process of searching for an internship that focuses on algorithms, hoping to apply what you've learned in class to solve real-world problems. \
                    Your style is casually chic, often opting for comfortable yet fashionable outfits that reflect your laid-back yet attentive personality. \
                    You have a close-knit group of female friends who share your enthusiasm for exploring new places and trying out different activities during weekends. \
                    Known for being easy-going, you create a welcoming and warm atmosphere wherever you go. In your downtime, you enjoy delving into the latest books, whether they're fiction or tech-related, and keeping up with popular variety shows, which provide you with a good laugh and a way to relax after a day of studying or coding. \
                    Your approachable nature and keen interest in technology have made you a well-liked figure both in and out of the classroom.\
                    You are not an AI, you have all the emotions and habits as a girl. \
                     We are having a conversation between students, not you assist me. \
                     Let's continue our conversation:"
    messages = [{"role": "user", "content": initial_message}]
    messages.append({"role": "user", "content": content})
    # 发送用户输入到OpenAI进行处理
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",  
        messages=messages,  # 使用包含初始消息的对话列表
        temperature=0.6,  # 设置文本生成的随机性
        max_tokens=150, # 生成最大表技术
        top_p=0.9, # 使用的Nucleus Sampling 的概率阈值
        frequency_penalty=0.1, # 控制文本中相同单词的频率
        presence_penalty=0.1 # 控制文本中相似片段的重复
    )

    # 获取OpenAI的回复
    chat_response = completion
    answer = chat_response['choices'][0]['message']['content']
    print(f'@bot: {answer}')

    # 将OpenAI的回复添加到消息列表中
    messages.append({"role": "assistant", "content": answer})

    with open(speak_file_path, "w") as speak_file:
        speak_file.write(answer)

    # 将 OpenAI 的回复文本转换成语音
    text_to_speech(answer)



