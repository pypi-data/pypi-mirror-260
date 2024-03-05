import array
import json
from celerabitpipelineintegration.model_credentials import Credentials
from celerabitpipelineintegration.uc_scenario_status import ScenarioStatus
from celerabitpipelineintegration.util_compliance_evaluator import ComplianceEvaluator
from celerabitpipelineintegration.util_configuration import Configuration
from celerabitpipelineintegration.model_execution_params import ExecutionParams, parse_from_args
from celerabitpipelineintegration.uc_authenticator import Authenticator
from celerabitpipelineintegration.uc_scenario_runner import ScenarioRunner
from celerabitpipelineintegration.util_misc import to_float
from celerabitpipelineintegration.version import print_version

class ModuleMain:

    __execution_params__:ExecutionParams = None

    def __is_debug_enabled__(self) -> bool:
        return  self.__execution_params__.exists_swtich('--DEBUG') or \
                self.__execution_params__.exists_swtich('-DEBUG') or \
                self.__execution_params__.exists_swtich('DEBUG')

    def __is_quiet__(self) -> bool:
        return  not (
                    self.__execution_params__.exists_swtich('-v') or \
                    self.__execution_params__.exists_swtich('--v')
                )

    def __configure_logger__(self):
        if self.__execution_params__:
            if (self.__is_debug_enabled__()):
                Configuration.instance().set_config_value('LOGGER', 'level', 'DEBUG')
            if (self.__is_quiet__()):
                Configuration.instance().set_config_value('LOGGER', 'quiet', True)

    def __get_credentials__(self) -> Credentials:
        login:str = self.__execution_params__.get_arg('login')
        password:str = self.__execution_params__.get_arg('password')
        if not login:
            raise Exception('Login not received')
        if not password:
            raise Exception('Password not received')
        return Credentials(login, password)

    def __do_authenticate__(self):
        credentials:Credentials = self.__get_credentials__()
        authenticator:Authenticator = Authenticator()
        token:str = authenticator.authenticate(credentials)
        print(token)

    def __job_info_to_string__(self, job_info:dict) -> str:
        if not job_info:
            return None
        json_string:str = json.dumps(job_info)
        return json_string

    def __do_run__(self):
        token:str = self.__execution_params__.get_arg('token')
        client:str = self.__execution_params__.get_arg('client')
        application:str = self.__execution_params__.get_arg('application')
        scenario:str = self.__execution_params__.get_arg('scenario')
        run_timeout_seconds:int = self.__execution_params__.get_arg('timeout')

        if not token:
            raise Exception('Token not received')
        
        if not client:
            raise Exception('Client not received')

        if not application:
            raise Exception('Application not received')

        if not scenario:
            raise Exception('Scenario not received')

        if not run_timeout_seconds:
            run_timeout_seconds = Configuration.instance().get_config_value('INVOKER', 'default-run-timeout-seconds')

        scenario_runner:ScenarioRunner = ScenarioRunner( \
                                                client_name = client, \
                                                application_name = application, \
                                                scenario_code = scenario, \
                                                token = token,
                                                run_timeout_seconds = run_timeout_seconds
                                            )

        job_info:dict = scenario_runner.run_sync()
        print(self.__job_info_to_string__(job_info))

    def __get_job_execution_result_json__(self, job_execution_result_str:str) -> any:
        job_execution_result:any = None
        try:
            job_execution_result = json.loads(job_execution_result_str)
        except Exception as e:
            raise Exception(f'job-result is not a json object. {e} *-*-* \n{job_execution_result_str}')

        return job_execution_result

    def __do_eval_job_results__(self):
        job_execution_result_str:str = self.__execution_params__.get_arg('job-result')
        tolerance_str:str = self.__execution_params__.get_arg('tolerance')

        if not job_execution_result_str:
            raise Exception('job-result not received')
        
        job_execution_result:any = self.__get_job_execution_result_json__(job_execution_result_str)

        evaluator:ComplianceEvaluator = ComplianceEvaluator(job_execution_result, tolerance_str)
        errors:array = evaluator.evaluate()
        if errors and len(errors) > 0:
            error_message:str = ''
            for error in errors:
                error_message += error + "\n"
            print(error_message)

    def __do_get_last_status__(self):
        token:str = self.__execution_params__.get_arg('token')
        client:str = self.__execution_params__.get_arg('client')
        application:str = self.__execution_params__.get_arg('application')
        scenario:str = self.__execution_params__.get_arg('scenario')

        if not token:
            raise Exception('Token not received')
        
        if not client:
            raise Exception('Client not received')

        if not application:
            raise Exception('Application not received')

        if not scenario:
            raise Exception('Scenario not received')
        
        scenario_status:ScenarioStatus = ScenarioStatus( \
                                                client_name = client, \
                                                application_name = application, \
                                                scenario_code = scenario, \
                                                token = token
                                            )
        

        job_info:dict = scenario_status.get_last_job()
        print(self.__job_info_to_string__(job_info))

    def __show_version__(self):
        print_version()

    def run(self, args:array):
        self.__execution_params__ = parse_from_args(args)
        self.__configure_logger__()

        if self.__execution_params__.operation == 'authenticate':
            self.__do_authenticate__()
        elif self.__execution_params__.operation == 'run':
            self.__do_run__()
        elif self.__execution_params__.operation == 'eval-job-results':
            self.__do_eval_job_results__()
        elif self.__execution_params__.operation == 'last-status':
            self.__do_get_last_status__()
        elif self.__execution_params__.operation == 'version':
            self.__show_version__()
