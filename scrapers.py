import requests
from bs4 import BeautifulSoup

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from utils import cook_soup, filter_jobs



def scrape_4dayweek():
    
    soup, jobs = cook_soup('https://4dayweek.io/remote-jobs/data-science')
    
    for job in soup.find_all('div', class_='job-tile'):
        title = job.find('h3').text.strip()
        link = 'https://4dayweek.io' + job.find('a')['href']
        description = ''
        filter_jobs(title, link, description, jobs)

    return jobs


def scrape_linkedin():
    
    options = Options()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.get('https://www.linkedin.com/jobs/search?keywords=remote%20llm')

    try:
        next_pages = driver.find_elements(By.CLASS_NAME, 'artdeco-pagination__indicator')
        del next_pages[0]
    except:
        next_pages = [None]

    jobs = []

    while next_pages:

        try:
            elements = driver.find_elements(By.CLASS_NAME, 'job-card-list__title-link')
            for job in elements:
                title = job.text.strip()
                link = job.get_attribute('href')
                description = ''
                jobs.append((title, link, description))

            next_page_button = next_pages.pop()
            next_page_button.click()

        except:
            continue

    driver.quit()

    return jobs


def scrape_remoteok():
    
    soup, jobs = cook_soup('https://remoteok.com')

    for job in soup.find_all('tr', class_='job'):
        title = job.find('h2', itemprop='title')
        link = job.find('a', class_='preventLink')

        if title and link:
            title = title.text.strip()
            link = 'https://remoteok.com' + link['href']
            description = ''

            filter_jobs(title, link, description, jobs)

    return jobs


def scrape_wellfound():

    soup, jobs = cook_soup('https://wellfound.com/role/r/artificial-intelligence-engineer')
    next_page = True

    while next_page:

        for job in soup.find_all('a', class_='text-brand-burgundy'):
            title = job
            link = job

            if title and link:
                title = title.text.strip()
                link = 'https://wellfound.com' + link['href']
                description = ''

                filter_jobs(title, link, description, jobs)

        try:
            next_page = soup.find('li', class_='styles_next-rc-style__szoZ_').find('a')['href']
            next_page_url = 'https://wellfound.com' + next_page
            soup, _ = cook_soup(next_page_url)
        except:
            next_page = False

    return jobs


def scrape_ai_jobs():

    soup, jobs = cook_soup('https://aijobs.net/?cat=3&cat=18&cat=5&cat=15&cat=7&reg=7&key=&exp=&sal=')

    for job in soup.find_all('div', class_='row'):
        title = job.find('h5')
        link = job.find('a')

        if title and link:
            title = title.text.strip()
            link = 'https://ai-jobs.net' + link['href']
            description = ''

            jobs.append((title, link, description))

    return jobs


def scrape_datajobs():

    soup, jobs = cook_soup('https://datajobs.com/Llm-Jobs')

    for job in soup.find_all('a'):
        title = job.find('strong')
        link = job

        if title and link:
            title = title.text.strip()
            link = 'https://datajobs.com' + link['href']
            description = ''

            jobs.append((title, link, description))

    return jobs


def scrape_remote_rocketship():

    soup, jobs = cook_soup('https://www.remoterocketship.com/jobs/jobTitle%3Dllm?page=1&sort=DateAdded&jobTitle=llm')

    for job in soup.find_all('div', class_='items-start'):
        title = job.find('h3')
        link = job.find('a', href=True)
        description = job.find('p')

        if title and link and description:
            title = title.text.strip()
            link = 'https://www.remoterocketship.com' + link['href']
            description = description.text.strip()

            jobs.append((title, link, description))

    return jobs


def scrape_indeed():

    soup, jobs = cook_soup('https://www.indeed.com/jobs?q=llm&l=&sc=0kf%3Aattr%28DSQF7%29%3B&')
    next_page = True

    while next_page:

        for job in soup.find_all('div', class_='job_seen_beacon'):
            title = job.find('h2', class_='jobTitle')
            link = job.find('a', href=True)

            if title and link:
                title = title.text.strip()
                link = 'https://www.indeed.com' + link['href']
                description = ''

                filter_jobs(title, link, description, jobs)

        try:
            next_page = soup.find('a', class_='css-17ffcjx')['href']
            next_page_url = 'https://www.indeed.com' + next_page
            soup, _ = cook_soup(next_page_url)
        except:
            next_page = False

    return jobs


def scrape_ziprecruiter_llm_jobs():

    soup, jobs = cook_soup('https://www.ziprecruiter.ie/jobs/search?l=Remote&q=Llm&remote=full')

    for job in soup.find_all('li', class_='job-listing'):
        title = job.find('strong')
        link = job.find('a', href=True)
        description = job.find('div', class_='jobList-description')

        if title and link and description:
            title = title.text.strip()
            link = link['href']
            description = description.text.strip()

            jobs.append((title, link, description))

    return jobs


def scrape_nofluffjobs():

    soup, jobs = cook_soup('https://nofluffjobs.com/pl/praca-zdalna/artificial-intelligence')

    for job in soup.find_all('a', class_='posting-list-item'):
        title = job.find('h3')
        link = job

        if title and link:
            title = title.text.strip()
            link = 'https://nofluffjobs.com' + link['href']
            description = ''

            jobs.append((title, link, description))

    return jobs


def scrape_pracuj():

    soup, jobs = cook_soup('https://it.pracuj.pl/praca/praca%20zdalna;wm,home-office?its=ai-ml')

    for job in soup.find_all('h2', class_='tiles_hlp4o5k6'):
        title = job.find('a')
        link = title

        if title and link:
            title = title.text.strip()
            link = link['href']
            description = ''

            jobs.append((title, link, description))

    return jobs



scrapers = [scrape_4dayweek, scrape_linkedin, scrape_remoteok, scrape_wellfound, scrape_ai_jobs, scrape_datajobs,
            scrape_remote_rocketship, scrape_indeed, scrape_ziprecruiter_llm_jobs, scrape_nofluffjobs, scrape_pracuj]
