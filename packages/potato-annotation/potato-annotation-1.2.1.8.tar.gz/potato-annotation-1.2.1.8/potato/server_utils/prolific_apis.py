"""
Utility functions for handling prolific apis

"""
import pandas as pd
import requests
import json
import pandas

# The base wrapper of prolific apis
class ProlificBase(object):
    def __init__(self, token):
        self.headers = {
            'Authorization': f'Token {token}',
        }

    def list_all_studies(self):
        url = 'https://api.prolific.com/api/v1/studies/'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()  # If the response contains JSON data
            studies = pd.DataFrame.from_records(data['results'])
            print('You currently have %s studies'%len(data['results']))
            print(studies[['id','name','study_type','internal_name','status']].to_records())
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def get_study_by_id(self, study_id):
        if study_id == None:
            study_id = self.study_id
        url = f'https://api.prolific.com/api/v1/studies/{study_id}/'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()  # If the response contains JSON data
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    #get all submissions, might be super slow when you have a long list of submissions
    def get_submissions(self):
        url = 'https://api.prolific.com/api/v1/submissions/'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()  # If the response contains JSON data
            print('You currently have %s submissions'%len(data['results']))
            return data['results']
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    # get the list of submissions from a study
    def get_submissions_from_study(self, study_id = None):
        if study_id == None:
            study_id = self.study_id
        api_endpoint = 'https://api.prolific.com/api/v1/submissions?study={}'
        url = api_endpoint.format(study_id)
        response = requests.get(url, headers=self.headers)
        data = response.json()['results']
        #print(len(data))
        #print(data.keys())
        return data

    # get the status of a specific submission
    def get_submission_from_id(self, submission_id):
        url = f'https://api.prolific.com/api/v1/submissions/{submission_id}/'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()  # If the response contains JSON data
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")

    # get the list of recent submissions from a study
    def get_recent_study_submissions(self, study_id):
        if study_id == None:
            study_id = self.study_id
        url = f'https://api.prolific.com/api/v1/studies/{study_id}/submissions/'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()  # If the response contains JSON data
            print('You currently have %s submissions' % len(data['results']))
            return (data['results'])
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    #get study status
    def get_study_status(self, study_id = None):
        if study_id == None:
            study_id = self.study_id
        data = self.get_study_by_id(study_id)
        if data:
            return data['status']
        else:
            return None

    #pause study based on the given study id, if id not given, use the study id
    #in the current object
    def pause_study(self, study_id = None):
        if study_id == None:
            study_id = self.study_id
        api_endpoint = 'https://api.prolific.com/api/v1/studies/{}/transition/'
        url = api_endpoint.format(study_id)
        data = {
                  "action": "PAUSE"
        }
        response = requests.post(url, headers=self.headers, json=data)
        #data = response.json()
        print(study_id, prolific.get_study_status(study_id))
        return data

    #start study based on the given study id, if id not given, use the study id
    #in the current object
    def start_study(self, study_id = None):
        if study_id == None:
            study_id = self.study_id
        api_endpoint = 'https://api.prolific.com/api/v1/studies/{}/transition/'
        url = api_endpoint.format(study_id)
        data = {
                  "action": "START"
        }
        response = requests.post(url, headers=self.headers, json=data)
        #data = response.json()
        print(study_id, prolific.get_study_status(study_id))
        return data


# The class to manage the status of a prolific study
class ProlificStudy(ProlificBase):
    def __init__(self, token, study_id):
        ProlificBase.__init__(self, token)
        self.study_id = study_id
        self.session2user = {}
        self.users = {}
        self.session_status_sets = {'completed':set(), 'returned':set(), 'timeout':set(), 'active':set()}
        self.study_status = None
        self.status_path = None

    #load the saved user inforamtion and initalize this object
    def load_saved_data(self):
        return None

    def get_


    #get returned user list
    #def

    #manage study status


prolific = ProlificStudy(token = 'yRB91_ngkHclqd36bhXCGWwl5fqU4iVlXX-2i61cfNoh7Tpvh4tH8R6IAxEBsYrkMnyc4X8tEpmmJhHXiHiRkFZYIm_Jr-pCoXFqyrIHX30qUuT5RMcIc7rG',
                         study_id='6500644505e4c811e95fb6de')
prolific.list_all_studies()
#print(prolific.get_submissions_from_study())
print(prolific.get_study_status())
#prolific.start_study()
#prolific.pause_study()

#prolific.get_study_by_id('651d90aa31f42a08bce57feb')
#prolific.get_recent_study_submissions('651d90aa31f42a08bce57feb')
#print(prolific.get_submission_from_id('651db6a7718107d07e95639d'))
#print(prolific.get_submissions_from_study())