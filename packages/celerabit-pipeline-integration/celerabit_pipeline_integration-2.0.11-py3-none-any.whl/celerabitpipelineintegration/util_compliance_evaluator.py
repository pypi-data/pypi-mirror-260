from enum import Enum

from celerabitpipelineintegration.util_logger import print_warn

VALID_JOB_STATUS:list = ["SUCCESS", "FINISHED"]

class JobType(Enum):
    API = "API"
    UX = "UX"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return self.name

DEFAULT_TOLERANCE = {
    JobType.API.value: {
        "latency": 0.8,
        "throughput": 0.5,
        "errors": 0.95,
        "deviation": 0.2
    },
    JobType.UX.value: {
        "performance": "MEDIUM"
    }
}

VALID_COLOR_RANGE_VALUES:list = ["GOOD", "MEDIUM", "BAD"]

class ComplianceEvaluator:

    def __init__(self, job_execution_result:dict, tolerance_str:str) -> None:
        self.job_execution_result = job_execution_result
        self.job_type = self.__get_job_type__()
        self.tolerance = self.__get_tolerance_dict__(tolerance_str, self.job_type)

    def __get_tolerance_dict__(self, tolerance_str:str, job_type:JobType) -> dict:
        if not tolerance_str:
            print_warn(f"Tolerance not received.  Working with default values: {DEFAULT_TOLERANCE[job_type.value]}")
            return DEFAULT_TOLERANCE[job_type.value]
        
        base_tolerance:dict = self.__get_dict_from_tokenized_string__(tolerance_str)
        tolerance:dict = {}

        if job_type == JobType.API:
            tolerance = self.__get_tolerance_dict_for_API_job__(base_tolerance)
        elif job_type == JobType.UX:
            tolerance = self.__get_tolerance_dict_for_UX_job__(base_tolerance)
        
        return tolerance
    
    def __get_tolerance_dict_for_UX_job__(self, base_tolerance:dict) -> dict:
        tolerance:dict = {
            "performance": base_tolerance["performance"] 
                                if "performance" in base_tolerance else DEFAULT_TOLERANCE[JobType.UX.value]["performance"]
        }
        return tolerance

    def __get_tolerance_dict_for_API_job__(self, base_tolerance:dict) -> dict:

        tolerance = {
            "latency": float(base_tolerance["latency"]) 
                            if "latency" in base_tolerance else DEFAULT_TOLERANCE[JobType.API.value]["latency"],
            "throughput": float(base_tolerance["throughput"])
                            if "throughput" in base_tolerance else DEFAULT_TOLERANCE[JobType.API.value]["throughput"],
            "errors": float(base_tolerance["errors"]) 
                            if "errors" in base_tolerance else DEFAULT_TOLERANCE[JobType.API.value]["errors"],
            "deviation": float(base_tolerance["deviation"])
                            if "deviation" in base_tolerance else DEFAULT_TOLERANCE[JobType.API.value]["deviation"]
        }

        return tolerance

    def __get_dict_from_tokenized_string__(self, tokenized_string:str) -> dict:
        if not tokenized_string:
            return {}
        
        dict_object:dict = {}
        tokens:list = tokenized_string.split(',')
        splited_token:list = None

        for token in tokens:
            splited_token = token.strip().split('=')

            if len(splited_token) != 2:
                raise Exception(f'Invalid tokenized string: "{token}".  Full string "{tokenized_string}"')

            dict_object[splited_token[0].strip()] = splited_token[1]

        return dict_object
                    
    def __is_valid_float_compliance_value__(self, value:any) -> bool:
        if not value:
            return False
        try:
            float(value)
        except ValueError:
            return False
        return True

    def __validate_job__(self) -> list:
        result_list:list = []

        if not "status" in self.job_execution_result:
            result_list.append('job without status')
        elif not self.job_execution_result["status"] in VALID_JOB_STATUS:
            result_list.append(f"job status is not in {VALID_JOB_STATUS}")

        if self.job_type == JobType.API:
            
            if  not "complianceLatency" in self.job_execution_result or \
                    not self.__is_valid_float_compliance_value__(self.job_execution_result["complianceLatency"]):
                result_list.append("complianceLatency not received in job_execution_result or has an invalid value")

            if not "complianceThroughput" in self.job_execution_result or \
                    not self.__is_valid_float_compliance_value__(self.job_execution_result["complianceThroughput"]):
                result_list.append("complianceThroughput not received in job_execution_result or has an invalid value")

            if not "complianceErrors" in self.job_execution_result or \
                    not self.__is_valid_float_compliance_value__(self.job_execution_result["complianceErrors"]):
                result_list.append("complianceErrors not received in job_execution_result or has an invalid value")

            if not "complianceDeviation" in self.job_execution_result or \
                    not self.__is_valid_float_compliance_value__(self.job_execution_result["complianceDeviation"]):
                result_list.append("complianceDeviation not received in job_execution_result or has an invalid value")

        elif self.job_type == JobType.UX:

            uxResults:dict = self.job_execution_result["uxResults"]
            if not "performance" in uxResults:
                result_list.append(f"No performance received for job UX in results:\n{uxResults}")
            elif not "color" in uxResults["performance"] or not uxResults["performance"]["color"]:
                result_list.append(f"No color range received for job UX in results:\n{uxResults}")
            elif not uxResults["performance"]["color"] in VALID_COLOR_RANGE_VALUES:
                result_list.append(f'No color range has en invalid value: {uxResults["performance"]["color"]}.  Allowed values: {VALID_COLOR_RANGE_VALUES}')

        return result_list            

    def __get_tolerance_value__(self, name:str) -> any:
        value:any = None

        try:
            value = self.tolerance[name]
        except KeyError:
            raise Exception(f'Tolerance string hasn\'t value "{name}"')
        
        return value

    def __evaluate_job_api__(self) -> list:
        current_value:float = 0.0
        minimum:float = 0.0
        error_messagges:list = []

        validation_list:list = self.__validate_job__()

        if len(validation_list) == 0:

            current_value = float(self.job_execution_result['complianceLatency'])
            minimum = self.__get_tolerance_value__('latency') * 100
            if (current_value < minimum):
                error_messagges.append(f'Latency {current_value} below tolerance {minimum}')

            current_value = float(self.job_execution_result['complianceThroughput'])
            minimum = self.__get_tolerance_value__('throughput') * 100
            if (current_value < minimum):
                error_messagges.append(f'Throughput current_value below tolerance minimum')

            current_value = float(self.job_execution_result['complianceErrors'])
            minimum = self.__get_tolerance_value__('errors') * 100
            if (current_value < minimum):
                error_messagges.append(f'Errors {current_value} below tolerance {minimum}')

            current_value = float(self.job_execution_result['complianceDeviation'])
            minimum = self.__get_tolerance_value__('deviation') * 100
            if (current_value < minimum):
                error_messagges.append(f'Deviation {current_value} below tolerance {minimum}')

        else:
            error_messagges = validation_list

        return error_messagges if len(error_messagges) > 0 else None

    def __evaluate_job_ux__(self) ->list:
        error_messagges:list = []
        validation_list:list = self.__validate_job__()

        if len(validation_list) == 0:
            performance:dict = self.job_execution_result["uxResults"]["performance"]
            color_range:str = performance["color"]
            if color_range.lower() != self.tolerance["performance"].lower():
                error_messagges.append(
                    f'Performance not in range.  Required "{self.tolerance["performance"]}", received "{color_range}"'
                )
        else:
            error_messagges = validation_list

        return error_messagges if len(error_messagges) > 0 else None

    def __is_ux_job__(self) -> bool:
        return "uxResults" in self.job_execution_result
    
    def __is_api_job__(self) -> bool:
        return "kpiLatency" in self.job_execution_result

    def __get_job_type__(self) -> JobType:
        if self.__is_ux_job__():
            return JobType.UX
        elif self.__is_api_job__():
            return JobType.API
        
        raise Exception("Can't define job_type from job_execution_result")

    def evaluate(self) -> list:
        if self.job_type == JobType.API:
            return self.__evaluate_job_api__()
        elif self.job_type == JobType.UX:
            return self.__evaluate_job_ux__()
        raise Exception("Invalid Job Type")