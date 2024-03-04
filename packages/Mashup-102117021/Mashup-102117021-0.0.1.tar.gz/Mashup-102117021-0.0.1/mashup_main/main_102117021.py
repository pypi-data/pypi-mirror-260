import argparse
from yt_funcs import video_voice_only, get_urls
from merge_audio import cut_and_merge


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'Artist',
        type = str,
        help = 'Name of the artist'
    )
    parser.add_argument(
        'NumVideos',
        type = int,
        help = 'Number of videos to be downloaded'
    )
    parser.add_argument(
        'AudioDuration',
        type = int,
        help = 'Duration of the audio in seconds'
    )

    parser.add_argument(
        'OutputFileName',
        type = str,
        help = 'Name of the output file'
    )

    args = parser.parse_args()
    

    search_keyword = args.Artist
    num_videos = args.NumVideos
    audio_len = args.AudioDuration * 1000
    output_file = args.OutputFileName

    assert len(vars(args)) == 4, "Invalid number of arguments"
    assert(args.NumVideos > 0), "Number of videos should be greater than 0"
    assert(args.AudioDuration >=20), "Audio duration should be greater than 20 seconds"
    
    urls = get_urls(search_keyword, num_videos)
    audio_files = []
    for url in urls:
        audio_files += video_voice_only(url)
    cut_and_merge(audio_files, output_file, audio_len)

if __name__ == "__main__":
    main()
