import cloudpickle
from truera_model import TruEraPredFuncModel  # pylint: disable=import-error


def _load_model_from_local_file(path):
    with open(path, "rb") as f:
        return TruEraPredFuncModel(cloudpickle.load(f))


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
