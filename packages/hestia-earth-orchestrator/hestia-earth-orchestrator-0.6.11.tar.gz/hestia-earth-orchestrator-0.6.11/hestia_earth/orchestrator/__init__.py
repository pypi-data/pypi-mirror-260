from pkgutil import extend_path
from os.path import isfile
import json
from hestia_earth.utils.tools import current_time_ms, non_empty_list

from .log import logger
from .models import run as run_models

__path__ = extend_path(__path__, __name__)


def _load_config_from_file(config):
    logger.info('Loading configuration from file: %s', config)
    with open(config) as f:
        return json.load(f)


def _load_config_from_preset(config: str, node_type: str):
    from .config import _load_config
    logger.info('Loading configuration from preset: %s (%s.json)', config, node_type)
    return _load_config(f"{config}/{node_type}.json")


def _load_config(config: str, node_type: str):
    return _load_config_from_file(config) if isfile(config) else _load_config_from_preset(config, node_type)


def _required(message): raise Exception(message)


def _filter_models_stage(models: list, stage: int = None):
    return models if stage is None else non_empty_list([
        (_filter_models_stage(m, stage) if isinstance(m, list) else m) for m in models if (
            not isinstance(m, dict) or m.get('stage') == stage
        )
    ])


def run(data: dict, configuration='hestia', stage: int = None) -> dict:
    """
    Runs a set of models on a Node.

    Parameters
    ----------
    data : dict
        Either a `Cycle`, a `Site` or an `ImpactAssessment`.
    configuration
        Can be the path of the config, or a preset (e.g. "hestia") or the plain config as dict. Defaults to "hestia"
    stage : int
        For multi-stage calculations, will filter models by "stage".

    Returns
    -------
    dict
        The data with updated content
    """
    now = current_time_ms()
    node_type = data.get('@type', data.get('type'))
    node_id = data.get('@id', data.get('id'))
    _required('Please provide an "@type" key in your data.') if node_type is None else None
    conf = configuration if isinstance(configuration, dict) else _load_config(configuration, node_type)
    _required('Please provide a valid configuration.') if conf is None or conf.get('models') is None else None
    models = _filter_models_stage(conf.get('models', []), stage=stage)
    logger.info(f"Running models on {node_type}" + f" with id: {node_id}" if node_id else '')
    data = run_models(data, models)
    logger.info('time=%s, unit=ms', current_time_ms() - now)
    return data
