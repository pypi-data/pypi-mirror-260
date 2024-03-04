import argparse
import sys
from . import grid, perfect_crop, shots, video_standardize

def main():
    """
    Run the command line version of Perfect Crop.
    """

    parser = argparse.ArgumentParser(
        add_help=False,
        description="Perfect Crop is a tool to crop videos to a specific object in the video.")

    parser.add_argument(
        "--input",
        "-i",
        help="The input video file or directory of video files to process.",
        # necessary to have atleast one input...
        nargs="+",
        required=True,
        dest="input")

    # it gets a little complicated layering, so I've just made it a function arguement
    parser.add_argument(
        "-f",
        "--function",
        dest="function",
        nargs="+",
        choices = ["perfect_crop", "shots", "standardize", "grid"],
        help="The function to run.")
    
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        # if no output is given, set it to the current directory
        default=".",
        help="The output directory to save the processed videos.")

    # add help option
    parser.add_argument(
        "-h",
        "--help",
        action="store_true",)

    args = parser.parse_known_args(['--help'])

    if args.function == "perfect_crop":
        perfect_crop(args.input, args.output)
    elif args.function == "shots":
        shots.get_shots(args.input, args.output)
    elif args.function == "standardize":
        video_standardize(args.input, args.output)
    elif args.function == "grid":
        grid(args.input, args.output)
    else:
        print("Please provide a function to run.")
        sys.exit(1)

if __name__ == "__main__":
    main()
