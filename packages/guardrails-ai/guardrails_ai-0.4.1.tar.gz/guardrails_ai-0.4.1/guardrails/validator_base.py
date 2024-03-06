import inspect
from collections import defaultdict
from copy import deepcopy
from string import Template
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
)

from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable, RunnableConfig
from pydantic import BaseModel, Field

from guardrails.classes import InputType
from guardrails.constants import hub
from guardrails.errors import ValidationError


class Filter:
    pass


class Refrain:
    pass


def check_refrain_in_list(schema: List) -> bool:
    """Checks if a Refrain object exists in a list.

    Args:
        schema: A list that can contain lists, dicts or scalars.

    Returns:
        bool: True if a Refrain object exists in the list.
    """
    for item in schema:
        if isinstance(item, Refrain):
            return True
        elif isinstance(item, list):
            if check_refrain_in_list(item):
                return True
        elif isinstance(item, dict):
            if check_refrain_in_dict(item):
                return True

    return False


def check_refrain_in_dict(schema: Dict) -> bool:
    """Checks if a Refrain object exists in a dict.

    Args:
        schema: A dict that can contain lists, dicts or scalars.

    Returns:
        True if a Refrain object exists in the dict.
    """
    for key, value in schema.items():
        if isinstance(value, Refrain):
            return True
        elif isinstance(value, list):
            if check_refrain_in_list(value):
                return True
        elif isinstance(value, dict):
            if check_refrain_in_dict(value):
                return True

    return False


def check_refrain(schema: Union[List, Dict]) -> bool:
    if isinstance(schema, List):
        return check_refrain_in_list(schema)
    return check_refrain_in_dict(schema)


def filter_in_list(schema: List) -> List:
    """Remove out all Filter objects from a list.

    Args:
        schema: A list that can contain lists, dicts or scalars.

    Returns:
        A list with all Filter objects removed.
    """
    filtered_list = []

    for item in schema:
        if isinstance(item, Filter):
            pass
        elif isinstance(item, list):
            filtered_item = filter_in_list(item)
            if len(filtered_item):
                filtered_list.append(filtered_item)
        elif isinstance(item, dict):
            filtered_dict = filter_in_dict(item)
            if len(filtered_dict):
                filtered_list.append(filtered_dict)
        else:
            filtered_list.append(item)

    return filtered_list


def filter_in_dict(schema: Dict) -> Dict:
    """Remove out all Filter objects from a dictionary.

    Args:
        schema: A dictionary that can contain lists, dicts or scalars.

    Returns:
        A dictionary with all Filter objects removed.
    """
    filtered_dict = {}

    for key, value in schema.items():
        if isinstance(value, Filter):
            pass
        elif isinstance(value, list):
            filtered_item = filter_in_list(value)
            if len(filtered_item):
                filtered_dict[key] = filtered_item
        elif isinstance(value, dict):
            filtered_dict[key] = filter_in_dict(value)
        else:
            filtered_dict[key] = value

    return filtered_dict


def filter_in_schema(schema: Union[Dict, List]) -> Union[Dict, List]:
    if isinstance(schema, List):
        return filter_in_list(schema)
    return filter_in_dict(schema)


validators_registry = {}
types_to_validators = defaultdict(list)


def validator_factory(name: str, validate: Callable):
    def validate_wrapper(self, *args, **kwargs):
        return validate(*args, **kwargs)

    validator = type(
        name,
        (Validator,),
        {"validate": validate_wrapper, "rail_alias": name},
    )
    return validator


def register_validator(name: str, data_type: Union[str, List[str]]):
    """Register a validator for a data type."""
    from guardrails.datatypes import registry as types_registry

    if isinstance(data_type, str):
        data_type = list(types_registry.keys()) if data_type == "all" else [data_type]
    # Make sure that the data type string exists in the data types registry.
    for dt in data_type:
        if dt not in types_registry:
            raise ValueError(f"Data type {dt} is not registered.")

        types_to_validators[dt].append(name)

    def decorator(cls_or_func: Union[Type[Validator], Callable]):
        """Register a validator for a data type."""
        if isinstance(cls_or_func, type) and issubclass(cls_or_func, Validator):
            cls = cls_or_func
            cls.rail_alias = name
        elif callable(cls_or_func) and not isinstance(cls_or_func, type):
            func = cls_or_func
            func.rail_alias = name  # type: ignore
            # ensure function takes two args
            if not func.__code__.co_argcount == 2:
                raise ValueError(
                    f"Validator function {func.__name__} must take two arguments."
                )
            # dynamically create Validator subclass with `validate` method as `func`
            cls = validator_factory(name, func)
        else:
            raise ValueError(
                "Only functions and Validator subclasses "
                "can be registered as validators."
            )
        validators_registry[name] = cls
        return cls

    return decorator


def get_validator(name: str):
    is_hub_validator = name.startswith(hub)
    validator_key = name.replace(hub, "") if is_hub_validator else name
    registration = validators_registry.get(validator_key)
    if not registration and name.startswith(hub):
        # This should import everything and trigger registration
        import guardrails.hub  # noqa

        return validators_registry.get(validator_key)
    return registration


class ValidationResult(BaseModel):
    outcome: str
    metadata: Optional[Dict[str, Any]] = None


class PassResult(ValidationResult):
    outcome: Literal["pass"] = "pass"

    class ValueOverrideSentinel:
        pass

    # should only be used if Validator.override_value_on_pass is True
    value_override: Optional[Any] = Field(default=ValueOverrideSentinel)


class FailResult(ValidationResult):
    outcome: Literal["fail"] = "fail"

    error_message: str
    fix_value: Optional[Any] = None


class Validator(Runnable):
    """Base class for validators."""

    rail_alias: str

    run_in_separate_process = False
    override_value_on_pass = False
    required_metadata_keys = []
    _metadata = {}

    def __init__(self, on_fail: Optional[Union[Callable, str]] = None, **kwargs):
        if on_fail is None:
            on_fail = "noop"
        if isinstance(on_fail, str):
            self.on_fail_descriptor = on_fail
            self.on_fail_method = None
        else:
            self.on_fail_descriptor = "custom"
            self.on_fail_method = on_fail

        # Store the kwargs for the validator.
        self._kwargs = kwargs

        assert (
            self.rail_alias in validators_registry
        ), f"Validator {self.__class__.__name__} is not registered. "

    def validate(self, value: Any, metadata: Dict[str, Any]) -> ValidationResult:
        """Validates a value and return a validation result."""
        raise NotImplementedError

    def to_prompt(self, with_keywords: bool = True) -> str:
        """Convert the validator to a prompt.

        E.g. ValidLength(5, 10) -> "length: 5 10" when with_keywords is False.
        ValidLength(5, 10) -> "length: min=5 max=10" when with_keywords is True.

        Args:
            with_keywords: Whether to include the keyword arguments in the prompt.

        Returns:
            A string representation of the validator.
        """
        if not len(self._kwargs):
            return self.rail_alias

        kwargs = self._kwargs.copy()
        for k, v in kwargs.items():
            if not isinstance(v, str):
                kwargs[k] = str(v)

        params = " ".join(list(kwargs.values()))
        if with_keywords:
            params = " ".join([f"{k}={v}" for k, v in kwargs.items()])
        return f"{self.rail_alias}: {params}"

    def to_xml_attrib(self):
        """Convert the validator to an XML attribute."""

        if not len(self._kwargs):
            return self.rail_alias

        validator_args = []
        init_args = inspect.getfullargspec(self.__init__)
        for arg in init_args.args[1:]:
            if arg not in ("on_fail", "args", "kwargs"):
                arg_value = self._kwargs.get(arg)
                str_arg = str(arg_value)
                if str_arg is not None:
                    str_arg = "{" + str_arg + "}" if " " in str_arg else str_arg
                    validator_args.append(str_arg)

        params = " ".join(validator_args)
        return f"{self.rail_alias}: {params}"

    def get_args(self):
        """Get the arguments for the validator."""
        return self._kwargs

    def __call__(self, value):
        result = self.validate(value, {})
        if isinstance(result, FailResult):
            from guardrails.validator_service import ValidatorServiceBase

            validator_service = ValidatorServiceBase()
            return validator_service.perform_correction(
                [result], value, self, self.on_fail_descriptor
            )
        return value

    def __eq__(self, other):
        if not isinstance(other, Validator):
            return False
        return self.to_prompt() == other.to_prompt()

    # TODO: Make this a generic method on an abstract class
    def __stringify__(self):
        template = Template(
            """
            ${class_name} {
                rail_alias: ${rail_alias},
                on_fail: ${on_fail_descriptor},
                run_in_separate_process: ${run_in_separate_process},
                override_value_on_pass: ${override_value_on_pass},
                required_metadata_keys: ${required_metadata_keys},
                kwargs: ${kwargs}
            }"""
        )
        return template.safe_substitute(
            {
                "class_name": self.__class__.__name__,
                "rail_alias": self.rail_alias,
                "on_fail_descriptor": self.on_fail_descriptor,
                "run_in_separate_process": self.run_in_separate_process,
                "override_value_on_pass": self.override_value_on_pass,
                "required_metadata_keys": self.required_metadata_keys,
                "kwargs": self._kwargs,
            }
        )

    def invoke(
        self, input: InputType, config: Optional[RunnableConfig] = None
    ) -> InputType:
        output = BaseMessage(content="", type="")
        str_input = None
        input_is_chat_message = False
        if isinstance(input, BaseMessage):
            input_is_chat_message = True
            str_input = str(input.content)
            output = deepcopy(input)
        else:
            str_input = str(input)

        response = self.validate(str_input, self._metadata)

        if isinstance(response, FailResult):
            raise ValidationError(
                (
                    "The response from the LLM failed validation!"
                    f"{response.error_message}"
                )
            )

        if input_is_chat_message:
            output.content = str_input
            return cast(InputType, output)
        return cast(InputType, str_input)

    """
    This method allows the user to provide metadata to validators used in an LCEL chain.
    This is necessary because they can't pass metadata directly to `validate` in a chain
        because is called internally during `invoke`.

    Usage
    ---
    my_validator = Validator(args).with_metadata({ "key": "value" })

    chain = prompt | model | my_validator | output_parser
    chain.invoke({...})

    When called multiple times on the same validator instance,
        the metadata value will be override.
    This allows the user to change the metadata programmatically
        for different chains or calls.
    """

    def with_metadata(self, metadata: Dict[str, Any]):
        """Assigns metadata to this validator to use during validation."""
        self._metadata = metadata
        return self


ValidatorSpec = Union[Validator, Tuple[Union[Validator, str, Callable], str]]
