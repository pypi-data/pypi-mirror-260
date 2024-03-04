import sys
import logging
import argparse

from .main import Rtspntf
from .version import get_version
from .const import PACKAGE_NAME

def main():
    """CLI entrypoint for the rtspntf package
    """
    parser = argparse.ArgumentParser(prog=PACKAGE_NAME, usage='rtspntf ', description=PACKAGE_NAME + ': Motion detection from RTSP image stream (intended for intercom image)')

    parser.add_argument('-rtsp', '--rtsp_url', help='RTSP URL', type=str, required=True)

    parser.add_argument('-sx', '--screen_sx', help='Screen start X (0-1)', type=float, required=True)
    parser.add_argument('-sy', '--screen_sy', help='Screen start Y (0-1)', type=float, required=True)
    parser.add_argument('-ex', '--screen_ex', help='Screen end X (0-1)', type=float, required=True)
    parser.add_argument('-ey', '--screen_ey', help='Screen end Y (0-1)', type=float, required=True)

    parser.add_argument('-webhook', '--webhook_url', help='Webhook URL', type=str, required=True)

    parser.add_argument('-at', '--area_diff_threshold', help='Difference threshold for area', type=float, required=False)
    parser.add_argument('-et', '--else_diff_max_threshold', help='Maximum difference threshold for else section', type=float, required=False)
    parser.add_argument('-i', '--process_interval', help='Process interval', type=float, required=False)
    parser.add_argument('-d', '--save_img_dest', help='Save image destination', type=str, required=False)

    parser.add_argument('-v', '--version', help='Get version', action='version', version=PACKAGE_NAME + ": v" + get_version())

    parser.add_argument('--debug', help='Show debug logs', action='store_true')


    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if args.debug else logging.INFO)

    client = Rtspntf(
        rtsp_url=args.rtsp_url,
        screen_sx=args.screen_sx,
        screen_sy=args.screen_sy,
        screen_ex=args.screen_ex,
        screen_ey=args.screen_ey,
        webhook_url=args.webhook_url
        )

    if args.area_diff_threshold:
        client.area_diff_threshold = args.area_diff_threshold
    if args.else_diff_max_threshold:
        client.else_diff_max_threshold = args.else_diff_max_threshold
    if args.process_interval:
        client.process_interval = args.process_interval
    if args.save_img_dest:
        client.save_img_dest = args.save_img_dest

    client.run()

if __name__ == "__main__":
    main()
