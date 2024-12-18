import pyautogui
from PIL import ImageFile, Image
from loguru import logger
from typing import Optional


class ScreenshotCapture:
    """Responsible for capturing screenshots"""

    @staticmethod
    def take_bounded_screenshot(
        x1: int, y1: int, width: int, height: int
    ) -> Optional[Image.Image]:
        """
        Capture a screenshot within specified bounds

        Args:
            x1: Top-left x coordinate
            y1: Top-left y coordinate
            width: Width of the screenshot
            height: Height of the screenshot

        Returns:
            Captured screenshot or None if error occurs
        """
        try:
            width = max(1, width)
            height = max(1, height)

            screenshot: ImageFile.Image = pyautogui.screenshot(
                region=(x1, y1, width, height)
            )
            logger.debug(f"Screenshot captured: {width}x{height} at ({x1},{y1})")
            return screenshot
        except Exception as e:
            logger.exception(f"Screenshot capture error: {e}")
            return None
