
class Configuration:

    __instance__ = None

    sections: any = {
        'CELERABIT-ENDPOINTS': {
            'authenticate': 'https://sec-api.celerabit.com/authenticate',
            'run': 'https://app-api.celerabit.com/named/client/{client}/target/{application}/scenario/{scenario}/run',
            'get-job': 'https://app-api.celerabit.com/named/client/{client}/target/{application}/scenario/{scenario}/job/{job}',
            'get-scenario-last-status': 'https://app-api.celerabit.com/named/client/{client}/target/{application}/scenario/{scenario}/last-status'
        },
        'INVOKER': {
            'id': 'celerabitpipelineintegration',
            'wait-to-get-status': 10,
            'default-run-timeout-seconds': 500
        },
        'LOGGER': {
            'level': 'INFO',
            'quiet': False
        },
        'COMPLIANCE': {
            'UX-KPIs': {
                'performance': {
                    'ranges': [
                        {'name': 'low', 'min': 0, 'max': 49},
                        {'name': 'mid', 'min': 50, 'max': 89},
                        {'name': 'high', 'min': 90, 'max': 100}
                    ]
                }
            }
        }
    }

    def __init__(self, config_file: str):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls.__instance__ is None:
            cls.__instance__ = cls.__new__(cls)
        return cls.__instance__

    def get_config_value(self, group: str, key: str) -> str:
        value: str = None
        try:
            group_dict: any = self.sections[group]
            if group_dict:
                value = group_dict[key]
        except KeyError:
            pass
        
        return value

    def set_config_value(self, group: str, key: str, value: any):
        if group in self.sections:
            section: any = self.sections[group]
            if key in section:
                section[key] = value
