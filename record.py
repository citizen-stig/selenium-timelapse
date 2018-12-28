import time
from datetime import datetime
from collections import namedtuple
import os
from subprocess import call
from urllib.parse import urlparse, ParseResult

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

Resolution = namedtuple('Resolution', ['width', 'height'])

base_dir = 'screens'


def init_driver(resolution: Resolution = None) -> webdriver.Firefox:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    if resolution is None:
        resolution = Resolution(1024, 800)
    driver.set_window_size(resolution.width, resolution.height)

    return driver


def prepare_folder(parsed_url: ParseResult) -> str:
    folder = os.path.join(base_dir, parsed_url.netloc, datetime.now().strftime('%y-%m-%d_%H:%M:%S'))

    if not os.path.exists(folder):
        os.makedirs(folder)

    return folder


def record(url: str, pause: int, duration: int = 30, resolution: Resolution = None):
    driver = init_driver(resolution)
    parsed_url = urlparse(url)

    folder = prepare_folder(parsed_url)

    i = 0
    errors = 0
    fps = 30
    iterations = duration * fps

    driver.get(url)
    while i < iterations or errors > 10:
        try:
            driver.refresh()
        except WebDriverException:
            errors += 1
            continue
        file_name = os.path.join(folder, 'screen_{:010d}.png'.format(i))
        driver.save_screenshot(file_name)
        time.sleep(pause)
        i += 1
    driver.quit()

    return save(folder)


# ffmpeg -r 15 -i  screens/bitcointicker.co/18-12-28_12\:40\:27/screen_%010d.png  -c:v libx264 -pix_fmt yuv420p -y movie.mp4
def save(folder: str):
    return call(
        [
            'ffmpeg',
            '-i {}/screen_%010d.png'.format(folder),
            '-r 30',
            '-c:v libx264',
            '-pix_fmt yuv420p',
            '-y {}/movie.mp4'.format(folder),
        ]
    )
