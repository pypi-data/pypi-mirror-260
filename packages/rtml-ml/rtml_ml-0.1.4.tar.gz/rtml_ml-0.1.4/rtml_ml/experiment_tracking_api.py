from typing import Any

from comet_ml import API


class ExistingCometExperiment:

    def __init__(
        self,
        api_key: str,
        experiment_key: str
    ):
        """"""
        self.api_key = api_key
        self.experiment_key = experiment_key
        
        self.api = API(api_key=api_key)
        self.experiment = self.api.get_experiment_by_key(experiment_key)

    def get_parameter(
        self,
        name: str,
        type: str,
    ) -> Any:
        """"""
        assert type in {"int", "float", "str", "dict"}, "type must be one of {'int', 'float', 'str', 'dict'}"
        
        if type == "int":
            return int(self.experiment.get_parameters_summary(name)['valueCurrent'])

        elif type == "float":
            return float(self.experiment.get_parameters_summary(name)['valueCurrent'])
        
        elif type == "str":
            return self.experiment.get_parameters_summary(name)['valueCurrent']
        
        elif type == "dict":
            
            parameter = self.experiment.get_parameters_summary()
