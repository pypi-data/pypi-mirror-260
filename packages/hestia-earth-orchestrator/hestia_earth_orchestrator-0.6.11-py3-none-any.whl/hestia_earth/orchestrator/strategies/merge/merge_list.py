import pydash
from hestia_earth.schema import UNIQUENESS_FIELDS

from hestia_earth.orchestrator.utils import _non_empty_list, update_node_version
from .merge_node import merge as merge_node

_TERM_KEY = 'term.@id'
_METHOD_MODEL_KEY = 'methodModel.@id'


def _matching_properties(model: dict, node_type: str):
    return UNIQUENESS_FIELDS.get(node_type, {}).get(model.get('key'), [])


def _match_list_el(source: list, dest: list, key: str):
    src_value = sorted(_non_empty_list([pydash.objects.get(x, key) for x in source]))
    dest_value = sorted(_non_empty_list([pydash.objects.get(x, key) for x in dest]))
    return 1 if all([
        len(src_value) > 0,
        len(dest_value) > 0,
        src_value == dest_value
    ]) else -1 if src_value != dest_value else 0


def _match_el_count(source: dict, dest: dict, keys: list):
    # assign different points to matched keys
    # 1 if both keys are defined and match
    # -1 if src and dest differ
    # 0 otherwise
    def match(key: str):
        keys = key.split('.')
        src_value = pydash.objects.get(source, key)
        dest_value = pydash.objects.get(dest, key)
        is_list = len(keys) >= 2 and (
            isinstance(pydash.objects.get(source, keys[0]), list) or
            isinstance(pydash.objects.get(dest, keys[0]), list)
        )
        value = _match_list_el(
            pydash.objects.get(source, keys[0], []),
            pydash.objects.get(dest, keys[0], []),
            '.'.join(keys[1:])
        ) if is_list else (
            1 if all([
                src_value is not None,
                dest_value is not None,
                src_value == dest_value
            ]) else -1 if src_value != dest_value else 0
        )
        return value

    return sum(map(match, keys)) if pydash.objects.get(source, _TERM_KEY) == pydash.objects.get(dest, _TERM_KEY) else 0


def _has_property(values: list, key: str): return any([pydash.objects.get(v, key, None) for v in values])


def _handle_local_property(values: list, properties: list, local_id: str):
    # Handle "impactAssessment.@id" if present in the data
    existing_id = local_id.replace('.id', '.@id')

    if local_id in properties:
        # remove if not used
        if not _has_property(values, local_id):
            properties.remove(local_id)

        # add if used
        if _has_property(values, existing_id):
            properties.append(existing_id)

    return properties


def _find_match_el_index(values: list, el: dict, same_methodModel: bool, model: dict, node_type: str):
    """
    Find an element in the values that match the new element, based on the unique properties.
    To find a matching element:

    1. Filter values that match the same `term.@id`
    2. Compute a "matching score" for each element, by assigning a score to each unique property
    3. Order matching elements by match score > 0
    4. Take last element (if any) => the one with the highest score
    """
    properties = _matching_properties(model, node_type)
    properties = list(set(properties + [_METHOD_MODEL_KEY])) if same_methodModel else [
        p for p in properties if p != _METHOD_MODEL_KEY
    ]
    properties = _handle_local_property(values, properties, 'impactAssessment.id')

    elements = [(i, _match_el_count(values[i], el, properties)) for i in range(0, len(values))]
    elements = [(i, match_count) for i, match_count in elements if match_count > 0]
    elements = sorted(elements, key=lambda x: x[1])
    return elements[-1][0] if elements else None


def merge(source: list, merge_with: list, version: str, model: dict = {}, merge_args: dict = {}, node_type: str = ''):
    source = source if source is not None else []

    # only merge node if it has the same `methodModel`
    same_methodModel = merge_args.get('sameMethodModel', False)
    # only merge if the
    skip_same_term = merge_args.get('skipSameTerm', False)

    for el in _non_empty_list(merge_with):
        source_index = _find_match_el_index(source, el, same_methodModel, model, node_type)
        if source_index is None:
            source.append(update_node_version(version, el))
        elif not skip_same_term:
            source[source_index] = merge_node(source[source_index], el, version, model, merge_args)
    return source
