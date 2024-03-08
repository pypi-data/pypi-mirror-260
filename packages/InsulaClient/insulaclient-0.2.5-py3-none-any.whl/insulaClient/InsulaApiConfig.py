import base64


class InsulaApiConfig(object):
    def __init__(self, insula_host, username, token, **kwargs):
        self.__insula_host = insula_host
        self.__username = username
        self.__token = token
        self.__headers = {
            'Authorization': f"Basic {base64.b64encode(bytes(str(self.__username) + ':' + str(self.__token), 'utf-8')).decode('utf-8')}",
            'Content-Type': 'application/hal+json;charset=UTF-8'}

        self.__init_kwargs_options(**kwargs)

    def __init_kwargs_options(self, **kwargs):
        self.__status_polling_interval = 60 * 5
        if 'status_polling_interval' in kwargs.keys():
            self.__status_polling_interval = int(kwargs['status_polling_interval'])

        self.__interval_between_requests = 5
        if 'interval_between_requests' in kwargs.keys():
            self.__interval_between_requests = int(kwargs['interval_between_requests'])

        self.__max_processor_attempts = 3
        if 'max_processor_attempts' in kwargs.keys():
            return int(kwargs['max_processor_attempts'])

    def get_max_processor_attempts(self):
        return self.__max_processor_attempts


    def get_status_polling_interval(self) -> int:
        return self.__status_polling_interval

    def get_interval_between_requests(self) -> int:
        return int(self.__interval_between_requests)

    def get_headers(self):
        return self.__headers

    def get_authorization_header(self):
        return {'Authorization': self.__headers['Authorization']}

    def get_job_logs_api_path(self, job_id):
        return f'{self.__insula_host}/secure/api/v2.0/jobs/{job_id}/logs'

    def get_job_output_file_api_path(self, job_id):
        return f'{self.__insula_host}/secure/api/v2.0/jobs/{job_id}/outputFiles?projection=detailedPlatformFile'

    def get_job_config_api_path(self):
        return f'{self.__insula_host}/secure/api/v2.0/jobConfigs/'

    def get_job_lunch_api_path(self, config_id):
        return f'{self.__insula_host}/secure/api/v2.0/jobConfigs/{config_id}/launch'

    def get_job_status_api_path(self, job_id):
        return f'{self.__insula_host}/secure/api/v2.0/jobs/{job_id}'

    def get_search_api_path(self):
        return f'{self.__insula_host}/secure/api/v2.0/search'

    def get_platform_service_url_api_path(self, service_id):
        return f'{self.__insula_host}/secure/api/v2.0/services/{service_id}'
