#!/usr/bin/env python3

from picamera import PiCamera, Color
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
stream_formatter = logging.Formatter('%(asctime)s - %(name)s [%(lineno)3d] - %(levelname)s: %(message)s')
ch.setFormatter(stream_formatter)
logger.addHandler(ch)
logger.info('using picamera')

camera = PiCamera(resolution=(1280, 720))

camera.vflip = True
camera.hflip = True
#   camera = PiCamera(resolution=(1280, 720), framerate=Fraction(2, 1))
#   camera.iso = 100
#   camera.shutter_speed = 500000 # camera.exposure_speed

logger.info(f'resolution: {camera.resolution}')
# logger.info(f'framerate: {camera.framerate}')
# logger.info(f'shutter_speed: {camera.shutter_speed}')
logger.info(f'hflip: {camera.hflip}')
logger.info(f'vflip: {camera.vflip}')

def capture(to_path):
    time.sleep(2)
    # camera.annotate_background = Color('black')
    # annotate_text = to_path.stem
    # annotate_text += 'ss: %d\tiso: %d' % (camera.shutter_speed, camera.iso)
    # camera.annotate_text = annotate_text
    camera.capture(str(to_path))
    logger.info('capture success: %s' % str(to_path))


if __name__ == '__main__':
    from sys import argv

    capture(argv[1])
