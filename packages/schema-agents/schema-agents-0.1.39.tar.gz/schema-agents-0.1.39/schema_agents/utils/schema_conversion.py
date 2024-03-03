"""Provide conversion functions for OpenAPI, JSON, and function schemas."""
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo
from inspect import signature
import inspect

from openapi_pydantic import OpenAPI
from openapi_pydantic.util import PydanticSchema, construct_open_api_with_schema_class
from pydantic import BaseModel, Field
from schema_agents.utils import schema_to_function, dict_to_pydantic_model

def extract_tool_schemas(func, func_name=None):
    assert callable(func), "Tool function must be callable functions"
    sig = signature(func)
    names = [p.name for p in sig.parameters.values()]
    for name in names:
        assert sig.parameters[name].annotation != inspect._empty, f"Argument `{name}` for `{func.__name__}` must have type annotation"
    types = [sig.parameters[name].annotation for name in names]
    defaults = []
    for name in names:
        if sig.parameters[name].default == inspect._empty:
            defaults.append(Field(..., description=name))
        else:
            assert isinstance(sig.parameters[name].default, FieldInfo), "Argument default must be a FieldInfo object with description"
            assert sig.parameters[name].default.description is not None, f"Argument `{name}` for `{func.__name__}` must have a description"
            defaults.append(sig.parameters[name].default)
    
    func_name = func_name or func.__name__
    return (
        dict_to_pydantic_model(
            func_name,
            {names[i]: (types[i], defaults[i]) for i in range(len(names))},
            func.__doc__,
        ),
        sig.return_annotation,
    )


def get_primitive_schema(type_, is_json_schema=False):
    """Maps Python types to OpenAPI schema types."""
    if type_ is str:
        return {"type": "string"}
    elif type_ is int:
        return {"type": "integer"}
    elif type_ is float:
        return {"type": "number"}
    elif type_ is bool:
        return {"type": "boolean"}
    elif is_json_schema:
        if type_ is inspect._empty:
            return {"type": "null"}
        elif inspect.isclass(type_) and issubclass(type_, BaseModel):
            return type_.schema()
        else:
            raise ValueError(f"Unsupported type: {type_}")
    else:
        if type_ is inspect._empty:
            return {}
        elif inspect.isclass(type_) and issubclass(type_, BaseModel):
            return PydanticSchema(schema_class=type_)
        else:
            raise ValueError(f"Unsupported type: {type_}")

def create_function_openapi_schema(func, func_name=None, method="post"):
    func_name = func_name or func.__name__
    input_schema, output_schema = extract_tool_schemas(func, func_name=func_name)
    output_schema_type = get_primitive_schema(output_schema, is_json_schema=False)
    return {
        method: {
            "description": func.__doc__,
            "operationId": func_name,
            "requestBody": {
                "content": {"application/json": {
                    "schema": PydanticSchema(schema_class=input_schema)
                }},
            },
            "responses": {"200": {
                "description": "Successful response",
                "content": {"application/json": {
                    "schema": output_schema_type if output_schema_type else None
                }},
            }},
        }
    }

def create_function_json_schema(func, func_name=None):
    func_name = func_name or func.__name__
    input_schema, output_schema = extract_tool_schemas(func, func_name=func_name)
    output_schema_type = get_primitive_schema(output_schema, is_json_schema=True)
    return input_schema.schema(), output_schema_type

def get_service_functions(service_config):
    functions = {}
    
    def extract_functions(config, path=""):
        for key, value in config.items():
            if isinstance(value, dict):
                extract_functions(value, path + key + ".")
            elif callable(value):
                functions[path + key] = value
    
    extract_functions(service_config)
    return functions

def get_service_openapi_schema(service_config, service_url="/"):
    functions = get_service_functions(service_config)
    paths = {}
    for path, func in functions.items():
        paths[f"/{path}"] = create_function_openapi_schema(func, func_name=path.replace(".", "_"))
    
    open_api = OpenAPI.parse_obj({
        "info": {"title": service_config['name'], "version": "v0.1.0"},
        "servers": [{"url": service_url or "/"}],
        "paths": paths,
    })
    open_api = construct_open_api_with_schema_class(open_api)

    # Return the generated OpenAPI schema in JSON format
    return open_api.dict(by_alias=True, exclude_none=True)


def get_service_json_schema(service_config):
    functions = get_service_functions(service_config)
    schemas = {}

    for path, func in functions.items():
        input_schema, output_schema = create_function_json_schema(func, func_name=path.replace(".", "_"))
        schemas[path] = {
            "input_schema": input_schema,
            "output_schema": output_schema
        }
    return schemas


def get_service_function_schema(service_config):
    functions = get_service_functions(service_config)
    function_schemas = []

    for path, func in functions.items():
        input_schema, _ = extract_tool_schemas(func, func_name=path)
        function_schemas.append({"type": "function", "function": schema_to_function(input_schema)})
    return function_schemas
