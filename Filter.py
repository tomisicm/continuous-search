import pandas as pd
import functools

from CsvSchema import CsvSchema

class Filter(CsvSchema):
    def __init__(self) -> None:
        """
        This class is feed the data and is filtering
        """
        self.current_jobs = self.read_existing_job_list()
        self.schema = CsvSchema().schema
        self.preferences = {
            'salary': {
              'criteria': 'between',
               'value': [16000, 28000]
            },
            'technology': {
                'criteria': 'contains',
                'value': [
                    'js', 'javascript', 'node', 'nodejs', 'node.js',
                    'ts', 'typescript',
                    'express', 'express.js', 'nestjs', 'nest.js',
                    'jest',
                    'graphql', 'apollo',
                    'vue', 'vuejs', 'vue.js',
                    'react', 'reactjs', 'react.js', 'react-redux', 'redux',
                    'php', 'laravel',
                    'mysql', 'sql', 'mariadb', 'mongodb', 'redis'
                    'docker', 'microservices'
                ],
                'dislike': [
                ]
            },
            'seniority': {
                'criteria': 'contains',
                'value': ['mid', 'medior', 'intermediate']
            },
            'location': {
                'criteria': 'equals',
                'value': 'EU'
            }
        }

    def read_existing_job_list(self) -> pd.DataFrame:
        existing_job_data = pd.read_csv('companies.csv')
        return existing_job_data

    def check_job_exists(self, job_data) -> bool:
        """
        This method checks if the job already exists in the given csv
        """
        company_name = job_data['COMPANY']
        position_name = job_data['POSITION']

        company_jobs = self.current_jobs[self.current_jobs['company'].str.contains(r'{}'.format(company_name), na=False)]
        postion_already_present = company_jobs[company_jobs['position'].str.contains(r'{}'.format(position_name), na=False)]

        if (postion_already_present.size > 0):
            return True
        return False

    def check_job_preferences_match_requrements(self, job_data) -> bool:
        """
        Returns True if job should be added to the job List, otherwise False.
        """
        fulfilled_conditions_bool = []

        # print(job_data)

        salary_requirements = job_data['SALARY']
        is_salary_fulfilled = self.check_amount_between(salary_requirements)
        fulfilled_conditions_bool.append(is_salary_fulfilled)

        tech_requirements = job_data['TECHNOLOGY']
        is_tech_fulfilled = self.get_match_quantity(tech_requirements)
        print('-----------------------')
        print(tech_requirements)
        print(is_tech_fulfilled)
        print('-----------------------')
        fulfilled_conditions_bool.append(is_tech_fulfilled)

        # for preference, conditions in self.preferences.items():
        #     criteria = conditions['criteria']
        #     preference_value = conditions['value']
        #     # print(preference)

        # if (preference == 'seniority'):
        #     is_fulfilled = self.check_contains(job_data[self.schema['SENIORITY']], preference_value)
        #     fulfilled_conditions_bool.append(is_fulfilled)
        # if (value and criteria == 'location'):
        #     is_fulfilled = self.check_equals(job_data[self.schema['LOCATION']], preference_value)
        #     fulfilled_conditions_bool.append(is_fulfilled)

        return functools.reduce(lambda a,b : a and b, fulfilled_conditions_bool)

    def check_criteria(self, job_data) -> bool:
        if (self.check_job_preferences_match_requrements(job_data)):
            return self.check_job_exists(job_data)
        return False

    def check_amount_between(self, value):
        if (value == ''):
            return True         # amount not specified
        if (isinstance(value, int)):
            return (value > 16000 and value < 28000)
        if (isinstance(value, str)):
            return (int(value) > 16000 and int(value) < 28000)

    def check_contains(self, value, boundary_values):
        lowercase_value = value.lower()
        return lowercase_value in boundary_values

    def check_equals(self, value, boundary_value):
        if (isinstance(value, str)):
            return value.lower() == boundary_value

    def get_match_quantity(self, job_data_reqs):
        count = 0
        preferences = self.preferences['technology']['value']
        dislike = self.preferences['technology']['dislike']
        for req in job_data_reqs:
            if (req in preferences):
                count = count + 1
        return count >= 2