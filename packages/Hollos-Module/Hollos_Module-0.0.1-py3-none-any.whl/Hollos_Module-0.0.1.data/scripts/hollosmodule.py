"""
![logo](https://devhollo.github.io/!assets/dev_assets/hollosmodule/img/logo.png)
see the Github page [here](https://github.com/DevHollo/Hollos-Module)
"""
def check_for_latest_hollosmodule_version():
    """
    Checks if you have the latest version of Hollo's Module. If not, it installs the latest version.
    """
    from importlib import metadata as pypi
    import subprocess
    import requests
    import logging
    try:
        user_ver = str(pypi.version('hxml'))
        pypi_ver = str(requests.get("https://pypi.org/pypi/HollosModule/json").json()['info']['version'])
        if not user_ver == pypi_ver:
            subprocess.run(['pip', 'install', f'hxml=={pypi_ver}'])
        else:
            pass
    except pypi.PackageNotFoundError as e:
        logging.error(f"Package HollosModule not found: {e}")
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve version from PyPI for HollosModule: {e}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install HollosModule package: {e}")

class DiscordAPI:
    def __init__(self, *args, **kwargs) -> None:
        """
        This is for simple Discord stuff like sending webhook messages!
        """
        pass

    @staticmethod
    def webhook_send_msg(msg: str, webhook_url: str) -> None:
        """
        Send a message to a Discord webhook.

        Args:
            message (str): The message to send.
            webhook_url (str): The URL of the Discord webhook.

        Raises:
            requests.HTTPError: If there's an error sending the webhook message.
        """
        import requests as rq
        import json as j
        payload = {
            "content": msg
        }
        payload_dat = j.dumps(payload)
        hdrs = {"Content-Type": "application/json"}
        response = rq.post(webhook_url, data=payload_dat, headers=hdrs)
        if response.status_code == 204:
            pass
        else:
            raise rq.HTTPError(f"Error sending webhook message. (Status code: {response.status_code})")

class Text:
    def __init__(self, *args, **kwargs):
        """
        Custom text styling!
        """
        #from sty import fg, Style, RgbFg, rs, ef
        #from colorama import Fore, Style
        
        def redtext(txt: str | None):
            """
            Makes text red
            """
            from sty import RgbFg, Style, fg
            fg.cus = Style(RgbFg(222, 8, 11))
            return fg.cus + txt + fg.rs
        self.red = redtext

        def orangetext(txt: str | None):
            """
            Makes text orange
            """
            from sty import fg, Style, RgbFg
            fg.cus = Style(RgbFg(255, 115, 0))
            return fg.cus + txt + fg.rs
        self.orange = orangetext

        def yellowtext(txt: str | None):
            """
            Makes text yellow
            """
            from sty import fg, Style, RgbFg
            fg.cus = Style(RgbFg(255, 213, 0))
            return fg.cus + txt + fg.rs
        self.yellow = yellowtext

        def greentext(txt: str | None):
            """
            Makes text green
            """
            from sty import fg, Style, RgbFg
            fg.cus = Style(RgbFg(0, 210, 21))
            return fg.cus + txt + fg.rs
        self.green = greentext

        def bluetext(txt: str | None):
            """
            Makes text blue
            """
            from sty import fg, RgbFg, Style
            fg.cus = Style(RgbFg(53, 59, 222))
            return fg.cus + txt + fg.rs
        self.blue = bluetext

        def purpletext(txt: str | None):
            """
            Makes text purple
            """
            from sty import fg, Style, RgbFg
            fg.cus = Style(RgbFg(175, 17, 218))
            return fg.cus + txt + fg.rs
        self.purple = purpletext

        def cyantext(txt: str | None):
            """
            Makes text cyan
            """
            from sty import fg, Style, RgbFg
            fg.cus = Style(RgbFg(80, 221, 246))
            return fg.cus + txt + fg.rs
        self.cyan = cyantext

        def pinktext(txt: str | None):
            """
            Makes text pink
            """
            from sty import fg, Style, RgbFg
            fg.cus = Style(RgbFg(255, 54, 198))
            return fg.cus + txt + fg.rs
        self.pink = pinktext

        def customrgbtext(txt: str | None, rgb: tuple | list = (255,255,255)):
            """
            Makes text custom RGB
            """
            from sty import fg, Style, RgbFg
            if type(rgb) == list:
                rgb = list(rgb)
            fg.cus = Style(RgbFg(int(rgb[0]), int(rgb[1]), int(rgb[2])))
            return fg.cus + txt + fg.rs
        self.custom_rgb = customrgbtext

        def blacktext(txt: str | None):
            """
            Makes text black (looks gray in vscode console)
            """
            from sty import Style, fg, RgbFg
            fg.cus = Style(RgbFg(0, 0, 0))
            return fg.cus + txt + fg.rs
        self.black = blacktext

        def italictext(txt: str | None):
            """
            Makes text italic
            """
            from sty import ef
            return ef.italic + txt + ef.rs
        self.italic = italictext

        def boldtext(txt: str | None):
            """
            Makes text bold
            """
            from sty import ef
            return ef.bold + txt + ef.rs
        self.bold = boldtext

        def strikethroughtext(txt: str | None):
            """
            Makes text strikethrough
            """
            from sty import ef
            return ef.strike + txt + ef.rs
        self.strikethrough = strikethroughtext

        def blinktext(txt: str | None):
            """
            Makes text blink (doesn\'t currently work in the vscode console)
            """
            from sty import ef
            return ef.blink + txt + ef.rs
        self.blink = blinktext

        def underlinetext(txt: str | None):
            """
            Makes text underlined
            """
            from sty import ef
            return ef.underl + txt + ef.rs
        self.underline = underlinetext

    @staticmethod
    def reverse(txt: str | None):
        """
        Returns a reversed version of `txt`
        """
        return txt[::-1]
    
    @staticmethod
    def to_human_readable_number(number: int):
        """
        Makes a number human readable
        ### Examples:
        - 10000 would turn into 10,000
        """
        return f"{number:,}"
    
class Math:
    def __init__(self, *args, **kwargs):
        """
        A simple math class.
        """
        pass

    @staticmethod
    def factorial(n: int | float):
        """
        Get the factorial of `n`
        """
        try:
            fact = 1
            if n < 0:
                raise ValueError("Number cannot be negative.")
            for i in range(1, n+1):
                fact = fact * i
            return fact
        except (TypeError, ValueError, OverflowError, FloatingPointError):
            return None
        
    @staticmethod
    def to_the_power_of(base: int | float, exp: int | float, mod: int | float = None):
        """
        Get `base` to the power of `exp`
        """
        try:
            if mod is None:
                return base**exp
            else:
                return base**exp % mod
        except (TypeError, ValueError, OverflowError, FloatingPointError):
            return None


def inputstr(prompt) -> str:
    """
    Returns input that will return a string
    """
    return str(input(prompt))

def inputint(prompt) -> int:
    """
    Returns input that will return a integer
    """
    return int(input(prompt))

def inputfloat(prompt) -> float:
    """
    Returns input that will return a float
    """
    return float(input(prompt))

def maskedinput(prompt, maskchar: str = "*") -> str:
    """
    #### This GIF shows what this function does:
    ![Example](https://devhollo.github.io/!assets/dev_assets/hollosmodule/img/masked_input.gif)
    """
    import getpass4
    return str(getpass4.getpass(prompt, char=maskchar))

def joinstr(*values) -> str:
    """
    Returns a string of the joined values
    """
    result = ""
    for val in values:
        result += str(val)
    return result

class loop:
    """
    ### This is for a `for` loop
    -----
    ## Examples:
    ----
    ### Without
    ```py
    for i in range(3):
        print(f"Hello World! [{i}]")
    ```
    Output:
    ![without](https://devhollo.github.io/!assets/dev_assets/hollosmodule/img/without_loop_class.png)
    ----
    ### With
    ```py
    from hollosmodule import loop

    for i in loop(3):
        print(f"Hello World! [{i}]")
    ```
    Output:
    ![with](https://devhollo.github.io/!assets/dev_assets/hollosmodule/img/with_loop_class.png)
    """
    def __init__(self, number: int):
        self.number = number

    def __iter__(self):
        self.current = 1
        return self

    def __next__(self):
        if self.current > self.number:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1

def userinfo(json_indent: int = None):
    """
    Returns info in json data like this:
    ```
    {
        \'pc-name\': \'PCNAME\',
        \'user\': \'USER\'
    }
    ```
    """
    import getpass
    import socket
    import json
    data = {'pc-name': socket.gethostname(), 'user': getpass.getuser()}
    dumped_data = None
    if json_indent is None or json_indent == 0:
        dumped_data = json.dumps(data)
        return json.loads(dumped_data)
    else:
        dumped_data = json.dumps(data, indent=json_indent)
        return json.loads(dumped_data)
    
class Exceptions:
    def __init__(self, *args, **kwargs):
        """
        Some custom Exceptions!
        """
        pass

    class UnsupportedFileExtensionError(Exception):
        """
        unsupported file extension
        """
        def __init__(self, file_extension: str, error_code=None):
            self.file_extension = file_extension
            self.error_code = error_code
            self.message = f"File extension '{file_extension}' is not supported."
            super().__init__(self.message)

        def __str__(self):
            if self.error_code:
                return f"{self.message} (Error code: {self.error_code})"
            else:
                return self.message

    class ConnectionError(Exception):
        def __init__(self, message="Connection error occurred", error_code=None):
            self.message = message
            self.error_code = error_code
            super().__init__(self.message)

        def __str__(self):
            if self.error_code:
                return f"{self.message} (Error code: {self.error_code})"
            else:
                return self.message
    
class HTTPS:
    def __init__(self, *args, **kwargs):
        """
        HTTPS related stuff!
        """
        pass

    @staticmethod
    def download_image_from_url(url: str, save_path: str):
        """
        used download a image from a url.
        ### Supported files:
        - .png
        - .jpg
        - .jpeg
        - .gif
        - .webp
        """
        import requests as rq
        import os
        response = rq.get(url)
        file_extension = os.path.splitext(url)[1]
        supported_files = [
            '.png',
            '.jpg',
            '.jpeg',
            '.gif',
            '.webp'
        ]
        if file_extension in supported_files:
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
            else:
                raise rq.HTTPError(f"Error downloading image. (Status code: {response.status_code})")
        else:
            raise Exceptions().UnsupportedFileExtensionError(file_extension)
        
class Decorators:
    def __init__(self, *args, **kwargs):
        """
        Some Useful Decorators!
        """
        pass

    @staticmethod
    def delay_execution(time_to_wait: int | float):
        """
        delays running the function by the specified seconds.
        """
        import time
        def decorator(func):
            def wrapper(*args, **kwargs):
                time.sleep(time_to_wait)
                return func(*args, **kwargs)
            return wrapper
        return decorator

class Files:
    def __init__(self, *args, **kwargs):
        """
        File handling things!
        """
        pass

    @staticmethod
    def convert_image(old_file: str, new_file: str, delete_old_file: bool = False):
        """
        Convert `old_file` to `new_file`
        ### Supported files:
        - .png
        - .jpg
        - .jpeg
        """
        from PIL import Image
        import os
        supported_files = [
            '.png',
            '.jpg',
            '.jpeg'
        ]
        _, old_ext = os.path.splitext(old_file)
        _, new_ext = os.path.splitext(new_file)
        if old_ext.lower() not in supported_files:
            raise Exceptions().UnsupportedFileExtensionError(f"Error: Unsupported file format: {old_ext}")
        if new_ext.lower() not in supported_files:
            raise Exceptions().UnsupportedFileExtensionError(f"Error: Unsupported file format: {new_ext}")
        with Image.open(old_file) as img:
            if img.mode == 'RGBA' and new_ext.lower() in ('.jpg', '.jpeg'):
                img = img.convert('RGB')
            img.save(new_file)
        if delete_old_file:
            os.remove(os.path.abspath(old_file))