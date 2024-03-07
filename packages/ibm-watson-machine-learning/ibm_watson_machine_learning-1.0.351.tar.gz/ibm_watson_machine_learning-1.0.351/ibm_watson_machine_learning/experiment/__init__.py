#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2020-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
from ibm_watson_machine_learning.experiment.autoai.autoai import AutoAI

__all__ = ['AutoAI',
           'TuneExperiment']

def __getattr__(name: str) -> None:
    if name == 'TuneExperiment':
        from ibm_watson_machine_learning.experiment.fm_tune.tune_experiment import TuneExperiment
        return TuneExperiment
    else:
        raise AttributeError
