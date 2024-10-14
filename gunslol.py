import requests
import datetime
import humanize
import time
from halo import Halo
from termcolor import colored
from colorama import init, Fore, Style

init(autoreset=True)
gunslolapi = 'ur gunslol apikey'

def lookup_user(username):
    api_url = 'https://guns.lol/api/user/lookup?type=username'
    payload = {
        "key": gunslolapi,
        "username": username,
        "uid": 0
    }

    spinner = Halo(text="loading...", spinner="dots")
    spinner.start()

    try:
        time.sleep(1)
        response = requests.post(api_url, json=payload)
        spinner.stop()
        if response.status_code == 200:
            user_data = response.json()

            account_creation_timestamp = user_data.get('account_created', 0)
            if account_creation_timestamp:
                account_creation_date = datetime.datetime.utcfromtimestamp(account_creation_timestamp)
                time_since_creation = humanize.naturaltime(datetime.datetime.utcnow() - account_creation_date)

            else:
                time_since_creation = "unknown date"
            views = user_data['config'].get('page_views', 0)
            uid = user_data.get('uid', 'N/A')
            profile_url = f"https://guns.lol/{username}"

            badges = user_data['config'].get('user_badges', [])
            badge_emojis = {
                "premium": "premium",
                "imagehost_access": "image host",
                "verified": "verified",
                "staff": "staff",
                "og": "og",
                "bughunter": "bug hunter",
                "donor": "donor",
                "beta": "beta",
                "server_booster": "server booster",
            }
            badge_display = " ".join([
                badge_emojis.get(badge.get('name', ''), badge.get('name', '')) if isinstance(badge, dict) else badge_emojis.get(badge, badge)
                for badge in badges if badge
            ])

            badge_display = badge_display if badge_display else "no"
            description = user_data['config'].get('description', 'no')
            def format_url(url):
                return url if url else "no"
            
            print(colored(f"\n{'•'*20}", 'magenta'))
            print(colored(f"info about {username}:", 'magenta', attrs=['bold', 'underline']))
            print(colored(f"• guns.lol profile:", 'magenta'), profile_url)
            print(colored(f"• account created:", 'magenta'), time_since_creation)
            print(colored(f"• page views:", 'magenta'), views)
            print(colored(f"• uid:", 'magenta'), uid)
            print(colored(f"• badge:", 'magenta'), badge_display)
            print(colored(f"• description:", 'magenta'), description)
            print(colored(f"• background:", 'magenta'), format_url(user_data['config'].get('url')))
            print(colored(f"• avatar:", 'magenta'), format_url(user_data['config'].get('avatar')))
            print(colored(f"• cursor:", 'magenta'), format_url(user_data['config'].get('custom_cursor')))
            print(colored(f"{'•'*20}\n", 'magenta'))

            audio_files = user_data['config'].get('audio', [])
            if audio_files:
                print(colored("audio:", 'magenta'))
                for audio in audio_files:
                    if 'url' in audio:
                        print(f"  • {audio['title']}: {audio['url']}")
            else:
                print(colored("no", 'red'))
        elif response.status_code == 400:
            print(colored("404", 'red'))
        elif response.status_code == 404:
            print(colored(f"'{username}' not found in guns.lol", 'red'))
        else:
            print(colored("404", 'red'))

    except Exception as e:
        spinner.stop()
        print(colored(f"{str(e)}", 'red'))

if __name__ == "__main__":
    while True:
        username = input(colored("\nhi enter guns.lol username (type [nigga] to exit): ", 'magenta', attrs=['bold']))
        if username.lower() == 'nigga':
            print(colored("ok", 'red', attrs=['bold']))
            break
        lookup_user(username)
