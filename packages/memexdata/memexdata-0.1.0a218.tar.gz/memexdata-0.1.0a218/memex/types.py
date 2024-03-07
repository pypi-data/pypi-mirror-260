import inspect
import re
from typing import Type, get_origin, get_args
from pydantic import BaseModel


def serialize_type(typ: Type) -> dict:
    if isinstance(typ, type) and not get_origin(typ) and issubclass(typ, BaseModel):
        return {"kind": "pydantic", "name": typ.__name__, "schema": typ.model_json_schema()}
    elif get_origin(typ):
        inner_types = [serialize_type(t) for t in get_args(typ)]
        return {"kind": "generic", "origin": get_origin(typ).__name__, "args": inner_types}
    else:
        return {"kind": "basic", "name": getattr(typ, "__name__", str(typ))}


def _udf_payload(func, prompt, resources=None, remote=False):
    sig = inspect.signature(func)
    parameter_types = [serialize_type(param.annotation) for param in sig.parameters.values()]
    param_names = [param.name for param in sig.parameters.values()]
    return_type = serialize_type(sig.return_annotation)
    if not prompt:
        from dill.source import getsource

        source = getsource(func)
        # Exclude any function decorator from the source
        source = re.sub(r"@.*\n", "", source)
        payload = dict(
            name=func.__name__,
            content="",
            variables=param_names,
            source=source,
            parameter_types=parameter_types,
            return_type=return_type,
            native=True,
            remote=remote,
        )
    else:
        docstring = func.__doc__
        payload = dict(
            name=func.__name__,
            content=docstring,
            variables=param_names,
            parameter_types=parameter_types,
            return_type=return_type,
            native=False,
        )
    if resources:
        payload["resources"] = resources
    return payload
