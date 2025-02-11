from dotenv import load_dotenv
import os
import ssl
import smtplib
import time

from bs4 import BeautifulSoup
import requests



def load_keywords(keywords_file: str):
    with open(keywords_file) as f:
        keywords = f.read().lower().splitlines()

    return keywords


def cook_soup(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    time.sleep(5)

    return soup, []


def filter_jobs(title: str, link: str, description: str, jobs: list):

    ad_text = f'{title}\n{description}'.lower()

    if any(keyword in ad_text for keyword in KEYWORDS) and not any(excluded_word in ad_text for excluded_word in EXCLUDED_WORDS):
        jobs.append((title, link, description))

    return None


load_dotenv()

SEEN_JOBS_FILE = os.getenv('SEEN_JOBS_FILE')
KEYWORDS = load_keywords('keywords.txt')
EXCLUDED_WORDS = load_keywords('negative_keywords.txt')

def load_seen_jobs():
    if not os.path.exists(SEEN_JOBS_FILE):
        return set()
    with open(SEEN_JOBS_FILE, 'r') as f:
        return set(f.read().splitlines())


def save_seen_jobs(jobs):
    with open(SEEN_JOBS_FILE, 'a') as f:
        for job in jobs:
            f.write(job + '\n')


SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

def send_email(new_jobs):

    subject = 'New Scraped Jobs'
    body = '\n\n'.join([f'{title}\n{link}\n{desc[:200]}...' for title, link, desc in new_jobs])
    body = body.encode('ascii', errors='ignore').decode()
    email_text = f'Subject: {subject}\n\n{body}'

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, email_text)
