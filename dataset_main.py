from datasets import load_dataset
import soundfile as sf
import os
import pathlib


language = "Japanese"   # 言語
character = "Kaeya"    # キャラクター名
repository = 'simon3000/genshin-voice'


language  = input("Language(e.g Japanese,Chinese,English):")
character = input("Character(e.g Kaeya,Paimon):")
repository= input("repository(e.g. simon3000/genshin-voice,simon3000/starrail-voice):")

dataset = load_dataset(repository, split='train', streaming=True)

# データセットをフィルタリング
data_query = dataset.filter(lambda voice: voice['language'] == language and voice['speaker'] == character and voice['transcription'] != '')


character = character.replace(" ","_")  # replace space to underline
# ダウンロード先のファルダ
output_folder_path = character + "-" + language
wav_folder_path = os.path.join(output_folder_path,"raw")
esd_file_path = os.path.join(output_folder_path,"esd.list")

os.makedirs(output_folder_path, exist_ok=True)
os.makedirs(wav_folder_path, exist_ok=True)
pathlib.Path(esd_file_path).touch(exist_ok=True)

# ダウンロード
for i, voice in enumerate(data_query):
  audio_file_name = f'{character}_{language}-{i}.wav'
  audio_path = os.path.join(output_folder_path, "raw",audio_file_name)  # Path to save the audio file
  sf.write(audio_path, voice['audio']['array'], voice['audio']['sampling_rate'])
  print(f'{i} done') 
  # Add transcription to esd.lst
  with open(esd_file_path, 'a', encoding="utf-8") as esd_file:
    esd_file.write(f"{audio_file_name}|{character}|JP|{voice['transcription']}\n")

