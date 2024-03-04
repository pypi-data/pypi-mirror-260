from pydub import AudioSegment

def cut_and_merge(input_files, output_file, audio_len):
    merged_audio = AudioSegment.empty()
    for i in range(len(input_files)):
        try :
            audio = AudioSegment.from_file(input_files[i])
            if len(audio) > audio_len:
                audio = audio[:audio_len]
            else:
                audio = audio
            merged_audio += audio
        except:
            pass
    merged_audio.export(output_file, format="mp3")
    return output_file