from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import re
import pandas as pd

class Scrapper(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @property
    def DOMAIN(self):
        raise NotImplementedError

    def transformRow(
        self,
        company = '',
        position = '',
        salary = '',
        seniority = '',
        technology = '',
        location = '',
        url = '',
        email = '',
        sentAt = '',
        fileLocation = ''
    ):
        """Create row which will be used for creating a new dataframe"""

        return [
            company if company else '',
            position if position else '',
            seniority  if seniority else '',
            technology if technology else '',
            salary if salary else '',
            location if location else '',
            url if url else '',
            email if email else '',
            sentAt if sentAt else '',
            fileLocation if fileLocation else '',
        ]

    def saveResults(self, results, output = 'companies.csv'):
        """Save the scraping results to a file."""

        print('Appending data')
        df=pd.DataFrame(results)
        #append to csv
        try:
            df.to_csv(output, mode='a', header=False)
        except Exception as e:
            print('Failed appending to the csv')

    @abstractmethod
    def jobs_page(self, page_num):
        pass

    @abstractmethod
    def process_page_data(self, page_num):
        pass

    @abstractmethod
    def filter_jobs(self, job):
        pass

    @abstractmethod
    def get_job_title(self, job):
        pass

    @abstractmethod
    def get_company_element(self, job):
        pass

    @abstractmethod
    def get_company_name(self, job):
        pass

    @abstractmethod
    def get_company_location(self, job):
        pass

    @abstractmethod
    def get_job_link(self, job):
        pass