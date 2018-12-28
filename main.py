import argparse
from record import record, Resolution


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--url', type=str, help='URL to be recorded')
    parser.add_argument('--duration',
                        type=int,
                        default=30,
                        help='Duration of video in seconds with 30 fps')
    parser.add_argument('--pause',
                        type=int,
                        default=5,
                        help='Pause between screenshots in seconds')
    parser.add_argument('--width',
                        type=int,
                        default=1024,
                        help='Window width in pixels')
    parser.add_argument('--height',
                        type=int,
                        default=800,
                        help='Window height in pixels')
    args = parser.parse_args()

    resolution = Resolution(width=args.width, height=args.height)

    record(
        url=args.url,
        pause=args.pause,
        duration=args.duration,
        resolution=resolution,
    )


if __name__ == '__main__':
    main()
