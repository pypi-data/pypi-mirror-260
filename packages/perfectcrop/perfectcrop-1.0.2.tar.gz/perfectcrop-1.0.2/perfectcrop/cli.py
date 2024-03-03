import argparse
from . import grid, perfect_crop, shots, video_standardize

#   -p   [video or directory]    | crop a video or directory of clips to select label (runs perfect_crop.py)

#   -s   [video]                 | create .json file identifying shots (scene changes) in a long form video. shots.py will then splice the video into individual clips (or scenes).
  
#   -vs  [video or directory]    | standardizes video length, codecs, etc. with ffmpeg bash. needed for concatenation!
  
#   -g   [video or directory]    | creates a dynamic, randomized moving video grid with ffmpeg bash commands. this is a legacy file from Court Laureate, not necessary for the project itself :)

def main():
    parser = argparse.ArgumentParser(description="Perfect Crop is a tool to crop videos to a specific object in the video.")

    # first arguement is the flag, the second is the video file or directory

    parser.add_argument("-p", help="Crop a video or directory of clips to select label (runs perfect_crop.py)")
    parser.add_argument("-s", help="Create .json file identifying shots (scene changes) in a long form video. shots.py will then splice the video into individual clips (or scenes).")
    parser.add_argument("-vs", help="Standardizes video length, codecs, etc. with ffmpeg bash. needed for concatenation!")
    parser.add_argument("-g", help="Creates a dynamic, randomized moving video grid with ffmpeg bash commands. this is a legacy file from Court Laureate, not necessary for the project itself :)")

    args = parser.parse_args()

    if args.p:
        perfect_crop.main(args.p)
    elif args.s:
        shots.main(args.s)
    elif args.vs:
        video_standardize.main(args.vs)
    elif args.g:
        grid.main(args.g)
    else:
        print("Please enter a valid usage.")
    


