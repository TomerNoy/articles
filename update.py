import os
import subprocess
import requests

# Article class definition
class Article:
    def __init__(self, article_id, title):
        self.id = article_id
        self.title = title

articles = [
    # These go to the root directory in the repo
    Article("11-KecDIhQHdlbZZqExRLCsvBNUM3_Au8PvP0t9cuun4", "CBT.html"),
    Article("19gNFP3QRmINt7g-TtIVJXQySRmAH8WqkHQiuRgHpMME", "about.html"),

    # These need to go to the path articles/ in the repo
    Article("1FWvG6SKLkgCiJP9ZuCf5l-ONRVEG1Xw3VoVMleHW5_g", "articles/ויסות רגשי.html"),
    Article("10ecIkuPTo8zgoEtc9Fcm_Uk7TtkswGOhapfVeVHV2SY", "articles/אכילה ריגשית.html"),
    Article("1bPINnDnQpaUdXgsbZ4nI2TowHrJh01utOYYVdaAgtUQ", "articles/OCD.html"),
    Article("1dA6tN7aCONxYi5Of1PIus8K7ZW80sbJkm_2eRaceeU4", "articles/חרדה.html"),
    Article("1vP1Ux4e4oz0-p5QCevlMNhDwb1X0ZefwrW8V1e2xMN4", "articles/דיכאון.html"),
]

def run_command(command):
    """ Run a shell command and exit on failure """
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(command)}")
        exit(1)

def pull_latest_changes():
    """ Fetch the latest changes from GitHub and reset local state to match """
    run_command(["git", "fetch", "origin"])
    run_command(["git", "reset", "--hard", "origin/main"])
    print("Pulled and reset to latest changes from GitHub.")

def download_articles():
    """ Download articles from Google Docs as HTML files """
    for article in articles:
        directory = os.path.dirname(article.title)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        response = requests.get(
            f"https://docs.google.com/feeds/download/documents/export/Export?id={article.id}&exportFormat=html"
        )

        if response.status_code == 200:
            with open(article.title, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"Downloaded: {article.title}")
        else:
            print(f"Failed to download: {article.title} (Status code: {response.status_code})")
            exit(1)

def commit_and_push_changes():
    """ Commit and push the downloaded articles to GitHub """
    run_command(["git", "add", "."])
    run_command(["git", "commit", "-m", "Updated articles to latest version"])
    run_command(["git", "push", "-u", "--force", "origin", "main"])
    print("Pushed changes to GitHub successfully.")

# Main execution flow
pull_latest_changes()    # Make sure we're starting with the latest from the remote
download_articles()      # Download the latest versions of the articles
commit_and_push_changes()  # Push the updated files to the remote repository
