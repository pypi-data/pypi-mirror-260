import rtsp
import time
import requests
import numpy as np
from PIL import ImageDraw
from typing import Optional
from logging import getLogger

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from PIL.Image import Image

class Rtspntf:
    def __init__(self, rtsp_url: str, screen_sx: float, screen_sy: float, screen_ex: float, screen_ey: float, webhook_url: str, area_diff_threshold: float = 40.0, else_diff_max_threshold: float = 20.0, process_interval: float = 0.2, save_img_dest: Optional[str] = None) -> None:
        self.logger = getLogger(__name__)

        self.rtsp_url = rtsp_url

        self.screen_sx = screen_sx
        self.screen_sy = screen_sy
        self.screen_ex = screen_ex
        self.screen_ey = screen_ey

        self.webhook_url = webhook_url

        self.area_diff_threshold = area_diff_threshold
        self.else_diff_max_threshold = else_diff_max_threshold

        self.process_interval = process_interval

        self.save_img_dest = save_img_dest

        self.previous_img_screen = None
        self.previous_img_else = None

    def _get_screen_area(self, img_w: int, img_h: int) -> tuple[int]:
        sx = int(self.screen_sx * img_w)
        sy = int(self.screen_sy * img_h)
        ex = int(self.screen_ex * img_w)
        ey = int(self.screen_ey * img_h)
        return sx, sy, ex, ey

    def _get_processed_img(self, img: Image, screen_area: tuple[int]) -> tuple[Image]:
        img_screen = img.crop(screen_area)
        img_else = img.copy()
        img_else_draw = ImageDraw.Draw(img_else)
        img_else_draw.rectangle(screen_area, fill=(0, 0, 0))
        return img_screen, img_else

    def _is_previous_img_exists(self) -> bool:
        return (self.previous_img_screen is not None) and (self.previous_img_else is not None)

    def _get_img_diff(self, img_1: Image, img_2: Image) -> float:
        return np.abs(np.array(img_1).astype(int) - np.array(img_2).astype(int))

    def _detect_motion(self, img_screen: Image, img_else: Image) -> tuple[bool, tuple[float, float, float]]:
        diff_screen_ = self._get_img_diff(img_screen, self.previous_img_screen)
        diff_else_ = self._get_img_diff(img_else, self.previous_img_else)

        diff_screen_mean = diff_screen_.mean()
        diff_else_mean = diff_else_.mean()
        area_mean_diff = diff_screen_mean - diff_else_mean

        if (area_mean_diff > self.area_diff_threshold and diff_else_mean < self.else_diff_max_threshold):
            self.logger.info("Motion Detected %s %s %s", diff_screen_.mean(), diff_else_.mean(), area_mean_diff)
            return True, (diff_screen_.mean(), diff_else_.mean(), area_mean_diff)
        else:
            self.logger.debug("No Motion Detected %s %s %s", diff_screen_.mean(), diff_else_.mean(), area_mean_diff)
            return False, (diff_screen_.mean(), diff_else_.mean(), area_mean_diff)

    def _update_previous_img(self, img_screen: Image, img_else: Image) -> None:
        self.previous_img_screen = img_screen
        self.previous_img_else = img_else

    def _save_img(self, img: Image, path: str) -> None:
        img.save(path)

    def _send_webhook(self, diff_screen: float, diff_else: float, diff_area: float) -> None:
        data = {
            "data": {
                "diff_screen": diff_screen,
                "diff_else": diff_else,
                "diff_area": diff_area
            }
        }
        requests.post(self.webhook_url, json=data)

    def run(self) -> None:
        with rtsp.Client(rtsp_server_uri=self.rtsp_url) as client:
            while client.isOpened():
                _image = client.read()
                if _image:
                    screen_area = self._get_screen_area(_image.width, _image.height)
                    img_screen, img_else = self._get_processed_img(_image, screen_area)

                    if self._is_previous_img_exists():
                        result, data = self._detect_motion(img_screen, img_else)
                        if result:
                            self._send_webhook(*data)

                    self._update_previous_img(img_screen, img_else)

                    if self.save_img_dest:
                        self._save_img(_image, self.save_img_dest)
                time.sleep(0.2)
