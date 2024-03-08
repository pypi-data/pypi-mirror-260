import yaml
from .InsulaApiConfig import InsulaApiConfig
from .InsulaWorkflowStep import InsulaWorkflowStep
from .InsulaJobStatus import InsulaJobStatus
from .InsulaFilesJobResult import InsulaFilesJobResult
from .InsulaWorkflowStepRunner import InsulaWorkflowStepRunner
from .s3 import S3Client
from .WorkflowManager import WorkflowManager


class InsulaWorkflow(object):

    def __init__(self, insula_config: InsulaApiConfig, workflow: str, parameters: dict = None):
        super().__init__()
        self.__insula_api_config = insula_config

        self.__wfm = WorkflowManager(yaml.safe_load(workflow))
        self.__steps_order = []

        self.__validate_version()
        self.__init_config()
        self.__init_workflow()
        self.__load_templates()
        self.__update_templates()
        self.__check_parameters_and_add_external(parameters)

        self.__init_requirements()

    def __load_templates(self):

        workflow_wfm = self.__wfm.get_workflow()
        templates_wfm = self.__wfm.get_templates()

        if 'templates' in workflow_wfm:
            for template in workflow_wfm['templates']:
                if 'name' in template:
                    templates_wfm[template['name']] = template

    @staticmethod
    def __update_existing_param(template_param: list, step_param: list):
        for template in template_param:
            template_name = template['name']
            find_param = False
            for step in step_param:
                step_name = step['name']
                if template_name == step_name:
                    find_param = True
                    break

            if not find_param:
                step_param.append(template)

    # TODO: questo metodo e' senza parole, va sistemato
    def __update_templates(self):

        workflow_wfm = self.__wfm.get_workflow()
        templates = self.__wfm.get_templates()

        to_jump = ['name']
        if 'templates' in workflow_wfm:
            for steps in self.__steps_order:
                for step in steps:
                    if 'template' in step:
                        if step['template'] in templates:
                            template = templates[step['template']]

                            for key, value in template.items():
                                if key not in to_jump:
                                    if key not in step:
                                        step[key] = value
                                    else:
                                        if key == 'params':
                                            self.__update_existing_param(value, step[key])
                        else:
                            raise Exception(f'Template {step["template"]} not found')

    def __validate_version(self):

        workflow_wfs = self.__wfm.get_workflow()

        if 'version' not in workflow_wfs:
            print('This workflow requires insulaClient version 0.0.1')
            exit(1)
        self.__version = workflow_wfs['version']
        if self.__version != 'beta/1':
            print('Version not compatible with beta/1')
            exit(1)

    def __init_config(self):

        workflow_wfs = self.__wfm.get_workflow()
        config_wfs = self.__wfm.set_config({
            'continue_on_error': False,
            'max_parallel_jobs': 3,
            'delete_workflow_log': False
        })

        if 'configuration' in workflow_wfs:
            if 'continue_on_error' in workflow_wfs['configuration']:
                config_wfs['continue_on_error'] = workflow_wfs['configuration']['continue_on_error']

        if 'max_parallel_jobs' in workflow_wfs['configuration']:
            config_wfs['max_parallel_jobs'] = int(workflow_wfs['configuration']['max_parallel_jobs'])

        if 'delete_workflow_log' in workflow_wfs['configuration']:
            config_wfs['delete_workflow_log'] = workflow_wfs['configuration']['delete_workflow_log']

    def __check_parameters_and_add_external(self, parameters):

        parameters_wfm = self.__wfm.get_parameters()

        if parameters is not None and isinstance(parameters, dict):
            for key, value in parameters.items():
                parameters_wfm[key] = value

        for key, value in parameters_wfm.items():
            if isinstance(value, str):
                pass
            elif isinstance(value, list):
                for v in value:
                    if not isinstance(v, str):
                        raise Exception(f'Parameter {key} format type not supported')
            else:
                raise Exception(f'Parameter {key} format type not supported')

    # TODO: separare questo metodo
    def __init_workflow(self):

        workflow_wfs = self.__wfm.get_workflow()
        requirements_wfm = self.__wfm.get_requirements()

        self.__name = workflow_wfs['name']
        self.__type = workflow_wfs['type']

        if 'requirements' in workflow_wfs and 'jobs' in workflow_wfs['requirements']:
            for job in workflow_wfs['requirements']['jobs']:
                requirements_wfm['jobs'].append(job)

        if 'parameters' in workflow_wfs:
            self.__wfm.set_parameters(workflow_wfs['parameters'])

        for step in workflow_wfs['steps']:
            self.__steps_order.append(InsulaWorkflowStep(step))

    def __filter_from_parameters(self, value: str):

        res = (self.__wfm.parse_match(value)
               .get_param_changed())

        if len(res) == 0:
            return value

        return res[0].get('default')

    def __init_job_requirements(self):

        requirements_wfm = self.__wfm.get_requirements()
        steps_wfm = self.__wfm.get_steps()

        for req in requirements_wfm['jobs']:
            job_id = self.__filter_from_parameters(str(req['id']))
            run = {
                'name': req['name'],
                'service_id': 0,
                'status': {
                    "config_id": 0,
                    "job_id": job_id,
                    "status": "REQUIREMENTS_RETRIEVED"
                },
                'results':
                    InsulaFilesJobResult(self.__insula_api_config).get_result_from_job(job_id)
            }

            steps_wfm.append(run)

    def __init_connection_requirements(self):

        workflow_wfm = self.__wfm.get_workflow()
        connection_wfm = self.__wfm.get_connections()

        if 'requirements' in workflow_wfm and 'connections' in workflow_wfm['requirements']:
            for conn in workflow_wfm['requirements']['connections']:
                if 'type' not in conn or 'name' not in conn:
                    raise Exception('The connection must have a type and name.')

                connection = {
                    'name': conn['name'],
                    'type': conn['type'],
                    'connection': None
                }

                if conn['type'] == 's3':
                    access_key = self.__filter_from_parameters(conn['params']['access_key'])
                    secret_key = self.__filter_from_parameters(conn['params']['secret_key'])
                    endpoint = self.__filter_from_parameters(conn['params']['endpoint'])
                    bucket = self.__filter_from_parameters(conn['params']['bucket'])

                    connection['connection'] = S3Client(access_key=access_key, secret_key=secret_key, endpoint=endpoint,
                                                        bucket=bucket)
                    connection_wfm[connection['name']] = connection

                else:
                    raise Exception(f"Connection type {conn['type']} not supported.")

    def __filter_log_properties(self):
        to_save = {
            'workflow': self.__wfm.get_workflow(),
            'parameters': self.__wfm.get_parameters(),
            'requirements': self.__wfm.get_requirements(),
            'steps': self.__wfm.get_steps(),
        }

        return to_save

    def __init_requirements(self):
        self.__init_job_requirements()
        self.__init_connection_requirements()

    def run(self) -> WorkflowManager:

        config_wfm = self.__wfm.get_config()

        print(f'configuration: {config_wfm}')
        print('Running...')

        insula_job_status = InsulaJobStatus()
        insula_job_status.set_job_id("wf_" + self.__name)
        insula_job_status.set_properties(self.__filter_log_properties()).save()

        try:
            for step in self.__steps_order:
                print(f'running... step: Step: {step}')
                _ = InsulaWorkflowStepRunner(
                    self.__insula_api_config,
                    step,
                    self.__wfm,
                    continue_on_error=config_wfm['continue_on_error'],
                    max_parallel_jobs=config_wfm['max_parallel_jobs']
                )
                results = _.run()
                for result in results['results']:
                    self.__wfm.get_steps().append(result['run'])
                insula_job_status.set_properties(self.__filter_log_properties()).save()

                if results['error']:
                    if not config_wfm['continue_on_error']:
                        raise Exception('there is an error, check the pid file')

            if config_wfm['delete_workflow_log']:
                insula_job_status.remove()

            return self.__wfm

        except Exception as error:
            insula_job_status.set_job_error('ERROR', error).save()
            raise Exception(error)
