from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import requests
import re
import sys
from Scrapper import Scrapper
from Filter import Filter
from CsvSchema import CsvSchema

class StrategyStackOverflow(Scrapper):
    """
    Concrete Strategies implement the algorithm while following the base Strategy
    interface. The interface makes them interchangeable in the Context.
    """

    # TODO: Clean element accessors
    # https://linuxhint.com/find_children_nodes_beautiful_soup/
    # https://stackoverflow.com/questions/5999747/beautifulsoup-nextsibling

    DOMAIN = 'https://stackoverflow.com/'
    PAGES = 8

    def __init__(self) -> None:
        self.schema = CsvSchema().schema
        self.filter = Filter()

    def jobs_page(self, page_num):
        """Scrape the page number from job postings."""

        print('Scraping the StackOverflow.com Jobs!!!')
        # /jobs?r=true&sort=p&tl=node+vuejs2+laravel+express+reactjs+react-redux&pg=2
        return  requests.get(self.DOMAIN + '/jobs?r=true&sort=p&tl=node+vuejs2+laravel+express+reactjs+react-redux&pg={}'.format(page_num))

    def process_page_data(self, response):
        """Scrape a page for Python jobs."""

        content = bs(response.text, 'html.parser')
        jobs = content.find_all('div', class_='-job')

        all_job_data = []

        for job in jobs:
            job_data = {
                'COMPANY': '',
                'POSITION': '',
                'SENIORITY': '',
                'TECHNOLOGY': '',
                'SALARY': '',
                'LOCATION': '',
                'URL': '',
                'EMAIL': '',
                'SENT_AT': '',
                'FILE_LOCATION': ''
            }

            job_title, seniority = self.get_job_title(job)
            job_data['POSITION'] = job_title
            job_data['SENIORITY'] = seniority

            # company_element = self.get_company_element(job)

            company_name = self.get_company_name(job)
            job_data['COMPANY'] = company_name

            job_technology = self.get_job_technology(job)
            job_data['TECHNOLOGY'] = job_technology

            company_location = self.get_company_location(job)
            job_data['LOCATION'] = company_location

            job_salary = self.get_job_salary(job)
            job_data['SALARY'] = job_salary

            job_time_of_posting  = self.transform_job_of_posting(self.get_job_time_of_posting(job))
            # print(job_time_of_posting)

            job_link = self.get_job_link(job)
            job_data['URL'] = job_link

            # should_be_added = self.filter.check_criteria(job_data)   # // this will be
            conditions_match = self.filter.check_job_preferences_match_requrements(job_data)

            if (conditions_match and job_time_of_posting=='today'):
                job_data = self.transformRow(
                    company = job_data['COMPANY'],
                    position = job_data['POSITION'],
                    seniority = job_data['SENIORITY'],
                    technology = job_data['TECHNOLOGY'],
                    salary = job_data['SALARY'],
                    url = job_data['URL']
                )
                all_job_data.append(job_data)

        return all_job_data

    def filter_jobs(self, job):
        pass

    def get_job_title(self, job):
        title = job.select('a.s-link')[0].text
        seniority = 'senior' if 'SENIOR' in title.upper() else 'medior'
        return [title, seniority]

    def get_company_element(self, job):
        company_elem = job.select('h3')[0]
        return company_elem

    def get_company_name(self, job):
        company = self.get_company_element(job)
        return company.select('span')[0].text.strip()

    def get_company_location(self, job):
        company = self.get_company_element(job)
        return company.select('span.fc-black-500')[0].text.strip().replace("\r\n","")

    def get_job_link(self, job):
        link = job.find('a', class_='s-link').get('href')
        return self.DOMAIN + link

    def get_job_technology(self, job):
        technology = []
        technology_element = job.find('div', class_='ps-relative d-inline-block z-selected')
        for tag_a in technology_element.findChildren('a'):
            technology.append(tag_a.text)
        return technology

    def get_job_time_of_posting(self, job):
        try:
            time_of_posting = job.find('ul', class_='mt4 fs-caption fc-black-500 horizontal-list') \
                .findNext('li').findNext('span').text
            return time_of_posting
        except Exception:
            print('Error occured while getting time of posting')
            return ''

    def transform_job_of_posting(self, time_of_posting):
        if 'h ago' in time_of_posting:
            return 'today'
        return ''

    def get_job_salary(self, job):
        """
        Returns salary if salary is specified
        """
        salary_li = job.findChildren('li[title]' , recursive=True)
        if len(salary_li):
            return salary_li[0].text
        return ''