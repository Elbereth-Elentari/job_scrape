import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from tqdm import tqdm

from utils import cook_soup, filter_jobs



def scrape_4dayweek():
    
    soup, jobs = cook_soup('https://4dayweek.io/remote-jobs/data-science')
    
    for job in tqdm(soup.find_all('h3'), desc='4dayweek'):
        title = job.find('a').text.strip()
        link = 'https://4dayweek.io' + job.find('a')['href']
        description = ''
        filter_jobs(title, link, description, jobs)

    return jobs


def scrape_linkedin():
    
    options = Options()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.get('https://www.linkedin.com/jobs/search?keywords=remote%20llm')
    time.sleep(5)

    try:
        next_pages = driver.find_elements(By.CLASS_NAME, 'artdeco-pagination__indicator')
        del next_pages[0]
    except:
        next_pages = [None]

    jobs = []

    while next_pages:

        try:
            elements = driver.find_elements(By.CLASS_NAME, 'job-card-list__entity-lockup')
            for job in tqdm(elements, desc='linkedin'):
                title = job.find_element(By.TAG_NAME, 'strong').text.strip()
                link = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
                description = ''
                jobs.append((title, link, description))

            next_page_button = next_pages.pop()
            next_page_button.click()
            time.sleep(5)

        except:
            continue

    driver.quit()

    return jobs


def scrape_remoteok():
    
    soup, jobs = cook_soup('https://remoteok.com')

    for job in tqdm(soup.find_all('a', class_='preventLink'), desc='remoteok'):
        title = job.find('h2')
        link = job

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

        for job in tqdm(soup.find_all('a', class_='mr-2'), desc='wellfound'):
            title = job
            link = job

            if title and link:
                title = title.text.strip()
                link = 'https://wellfound.com' + link['href']
                description = ''

                jobs.append((title, link, description))

        try:
            next_page = soup.find('li', class_='styles_next-rc-style__szoZ_').find('a')['href']
            next_page_url = 'https://wellfound.com' + next_page
            soup, _ = cook_soup(next_page_url)
        except:
            next_page = False

    return jobs


def scrape_ai_jobs():

    soup, jobs = cook_soup('https://aijobs.net/?cat=3&cat=18&cat=5&cat=15&cat=7&reg=7&key=&exp=&sal=')

    for job in tqdm(soup.find_all('div', class_='row'), desc='aijobs'):
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

    for job in tqdm(soup.find_all('a'), desc='datajobs'):
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

    for job in tqdm(soup.find_all('div', class_='p-6'), desc='remoterocketship'):
        title = job.find('h3')
        link = job.find('a')
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

        for job in tqdm(soup.find_all('h2', class_='jobTitle'), desc='indeed'):
            title = job.find('span')
            link = job.find('a')

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

    for job in tqdm(soup.find_all('div', class_='jobList-intro'), desc='ziprecruiter'):
        title = job.find('strong')
        link = job
        description = job.find('div', class_='jobList-description')

        if title and link and description:
            title = title.text.strip()
            link = link['href']
            description = description.text.strip()

            jobs.append((title, link, description))

    return jobs


def scrape_nofluffjobs():

    soup, jobs = cook_soup('https://nofluffjobs.com/pl/praca-zdalna/artificial-intelligence')

    for job in tqdm(soup.find_all('a', class_='posting-list-item'), desc='nofluffjobs'):
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

    for job in tqdm(soup.find_all('a', class_='tiles_o1859gd9'), desc='pracuj.pl'):
        title = job
        link = job

        if title and link:
            title = title.text.strip()
            link = link['href']
            description = ''

            jobs.append((title, link, description))

    return jobs



scrapers = [scrape_4dayweek, scrape_linkedin, scrape_remoteok, scrape_wellfound, scrape_ai_jobs, scrape_datajobs,
            scrape_remote_rocketship, scrape_indeed, scrape_ziprecruiter_llm_jobs, scrape_nofluffjobs, scrape_pracuj]
