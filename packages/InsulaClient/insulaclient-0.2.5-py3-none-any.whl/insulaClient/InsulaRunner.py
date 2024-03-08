import requests
from time import sleep
from .InsulaApiConfig import InsulaApiConfig
from .InsulaJobParams import InsulaJobParams
from .InsulaJobStatus import InsulaJobStatus


class InsulaRunner(object):
    def __init__(self, insula_config: InsulaApiConfig):
        super().__init__()
        self.__insula_api_config = insula_config

    def __set_job_config(self, params: InsulaJobParams):
        r = requests.post(
            self.__insula_api_config.get_job_config_api_path(),
            data=str(params),
            headers=self.__insula_api_config.get_headers()
        )

        if r.status_code != 201:
            raise Exception(f'Cant create Job_config: {r.text}')

        resp_dict = r.json()

        return resp_dict['id']

    def __lunch_job(self, config_id):
        url = self.__insula_api_config.get_job_lunch_api_path(config_id)
        run_request = requests.post(url, headers=self.__insula_api_config.get_headers())
        if run_request.status_code != 202:
            raise Exception(f'Cant lunch the Job_config: {config_id}, error: {run_request.text}')

        run_request_dict = run_request.json()
        id_job = run_request_dict['content']['id']

        return id_job

    def __get_job_status(self, job_id):
        url_status = self.__insula_api_config.get_job_status_api_path(job_id)
        status = requests.get(url_status, headers=self.__insula_api_config.get_headers())

        if status.status_code != 200:
            raise Exception(f'Cant get status job: {job_id}')

        url_status_dict = status.json()

        job_status = url_status_dict['status']
        if job_status == 'COMPLETED' or job_status == 'ERROR' or job_status == 'CANCELLED':
            return job_status

        return 'RUNNING'

    # TODO: To create run from config_id
    def run(self, job_params: InsulaJobParams, **kwargs) -> InsulaJobStatus:
        insula_job_status = InsulaJobStatus()
        insula_job_status.set_properties({'params': str(job_params), 'kwargs': kwargs})

        try:
            insula_job_status.set_config_id(self.__set_job_config(job_params)).save()
            sleep(self.__insula_api_config.get_interval_between_requests())
            insula_job_status.set_job_status('LUNCHING').save()
            insula_job_status.set_job_id(self.__lunch_job(insula_job_status.get_config_id())).save()
            insula_job_status.set_job_status('RUNNING')
            while insula_job_status.get_job_status() == 'RUNNING':
                sleep(self.__insula_api_config.get_status_polling_interval())
                insula_job_status.set_job_status(self.__get_job_status(insula_job_status.get_job_id())).save()

        except Exception as error:
            insula_job_status.set_job_error('ERROR', error).save()

        insula_job_status.remove_if_completed()
        return insula_job_status
