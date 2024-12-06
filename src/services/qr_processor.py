try:
    from pyzbar.pyzbar import decode, ZBarSymbol
    from pyzbar.pyzbar_error import PyZbarError  # Import specific exception
except FileNotFoundError:
    import sys
    import webbrowser
    from loguru import logger
    from tkinter import messagebox

    logger.error(
        "Failed to import pyzbar. Failed to import pyzbar. This may be because Microsoft Visual C++ 2013 Redistributable is not installed on your system."
    )
    logger.error(
        "Please download and install the Visual C++ Redistributable for Visual Studio 2013 from the following link:"
    )
    logger.error("https://www.microsoft.com/en-gb/download/details.aspx?id=40784")

    download_cpp_redistributable = messagebox.showerror(
        "Import Error",
        "Failed to import pyzbar. This may be because Microsoft Visual C++ 2013 Redistributable is not installed on your system.\n\n"
        "Would you like to download and install it manually?",
        type="yesno",
    )

    if download_cpp_redistributable == "yes":
        webbrowser.open(
            "https://www.microsoft.com/en-gb/download/details.aspx?id=40784"
        )

    sys.exit(1)

from PIL import Image
from loguru import logger
from typing import Optional, Tuple, Union


class QRCodeProcessor:
    """Handles QR code detection and processing"""

    @staticmethod
    def detect_qr_code(
        image: Optional[Union[Image.Image, str]],
    ) -> Tuple[Optional[str], bool]:
        """
        Detect and decode QR code from an image

        Args:
            image: Image to process or path to the image file

        Returns:
            Tuple of (detected data, detection success)
        """
        if image is None:
            logger.warning("Attempted to process None image")
            return None, False

        try:
            if isinstance(image, str):
                try:
                    with Image.open(image) as img:
                        image = img.copy()
                except IOError as e:
                    logger.error(f"Error opening image file: {e}")
                    return None, False

            logger.debug("Starting QR code detection")
            try:
                decoded_objects = decode(image, symbols=[ZBarSymbol.QRCODE])
            except PyZbarError as e:
                logger.error(f"Error decoding QR code: {e}")
                return None, False

            if decoded_objects:
                data = decoded_objects[0].data.decode("utf-8")
                if not data:
                    logger.warning("Empty QR Code detected")
                    return None, False
                logger.success(f"QR Code detected: {data}")
                return data, True

            logger.warning("No QR Code detected in image")
            return None, False
        except Exception as e:
            logger.exception(f"QR code detection error: {e}")
            return None, False
