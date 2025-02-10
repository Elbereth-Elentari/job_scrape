from tqdm import tqdm

from utils import load_seen_jobs, send_email, save_seen_jobs
from scrapers import scrapers



if __name__ == '__main__':

    seen_jobs = load_seen_jobs()
    new_jobs = []
    for scraper in tqdm(scrapers):
        jobs = scraper()
        for title, link, description in jobs:
            if link not in seen_jobs:
                new_jobs.append((title, link, description))
                seen_jobs.add(link)

    if new_jobs:
        send_email(new_jobs)
        save_seen_jobs([job[1] for job in new_jobs])
        print('Sent email with new jobs')
