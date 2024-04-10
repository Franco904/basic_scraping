from bs4 import BeautifulSoup
import requests


# Select required job skills to filter out
print('Put some skill(s) you are unfamiliar with (comma separated):')

unfamiliar_skill_input = input('> ')
unfamiliar_skills = list(map(lambda uf_skill: uf_skill.strip(), unfamiliar_skill_input.split(',')))


def visit_jobs_page():
    # Get all jobs page content
    jobs_page_content = requests.get(
        'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc'
        '=&searchTextText=&txtKeywords=python&txtLocation='
    )
    soup = BeautifulSoup(jobs_page_content.text, 'lxml')

    # Find all job items
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    print(f'Filtering out ', end='')
    for unfamiliar_skill in unfamiliar_skills:
        skill = f'{unfamiliar_skill}' if unfamiliar_skill == unfamiliar_skills[-1] else f'{unfamiliar_skill}, '
        print(skill, end='')
    print('...\n')

    # Iterate over job items
    for i, job in enumerate(jobs):
        publish_date = job.find('span', class_='sim-posted').span.text

        # Filter recent jobs
        if 'few' in publish_date:
            required_skills = job.find('span', class_='srp-skills').text.replace(' ', '').replace('\n', '').replace(', ', ',').split(',')

            # Filter out jobs with unfamiliar skills previously selected
            if any(uf_skill in required_skills for uf_skill in unfamiliar_skills):
                continue

            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '').replace('\n', '')

            job_info_link = job.header.h2.a['href']

            # Export the extracted info to a file (w = write access)
            try:
                with open(f'posts/{i}.txt', 'w') as file:
                    file.write(f'Company name: {company_name}\n')
                    file.write(f'Required skills: {required_skills}\n')
                    file.write(f'More info: {job_info_link}\n')

                print(f'Successfully saved data to file "posts/{i}.txt"')
            except:
                print(f'Error saving data to file "posts/{i}.txt"')
