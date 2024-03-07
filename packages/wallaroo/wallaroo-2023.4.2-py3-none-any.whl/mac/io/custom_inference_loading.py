"""This module features helper functions for loading a CustomInference for BYOP."""

import importlib
import inspect
import logging
from pathlib import Path
from typing import Any, Callable, Set

from mac.inference.creation.inference_builder import InferenceBuilder

logger = logging.getLogger(__name__)


def is_class_member(obj: Callable) -> bool:
    """Checks if the given object is a class member.

    :param obj: The object to check.

    :return: True if the given object is a class member, False otherwise.
    """
    return inspect.isclass(obj)


def is_object_derived_from_class(obj: Any, cls: Any) -> bool:
    """Checks if the given object is derived from the given class.

    :param obj: The object to check.
    :param cls: The class to check.

    :return: True if the given object is derived from the given class, False otherwise.
    """
    return issubclass(obj, cls) and obj.__name__ != cls.__name__


def import_py_module_from_path(file_path: Path, spec_name: str) -> Any:
    """Import a python module from a given file path.

    :param file_path: The path of the file to import the module from.
    :param spec_name: The name to import the module as.

    :return: The imported module.
    """
    spec = importlib.util.spec_from_file_location(spec_name, file_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore

    try:
        spec.loader.exec_module(module)  # type: ignore
    except FileNotFoundError as exc:
        message = f"Could not load module from file: {file_path.as_posix()}."
        logger.error(message, exc_info=True)
        raise exc

    return module


def load_custom_inference_builder(
    matching_files: Set[Path],
) -> InferenceBuilder:
    """Load custom inference builder from the python modules specified in a
    given custom inference config.

    :param matching_files: A set of paths to the python files that contain the
    custom InferenceBuilder and its related components.

    :return: An InferenceBuilder subclass instance.
    """
    logger.info("Loading custom InferenceBuilder from Python files...")

    inference_builder = None

    for py_file in matching_files:  # type: ignore
        module = import_py_module_from_path(py_file, "custom_inference")
        for _, obj in inspect.getmembers(module, is_class_member):
            if is_object_derived_from_class(obj, InferenceBuilder):
                if inference_builder is None:
                    inference_builder = obj()
                else:
                    message = "Multiple InferenceBuilder subclasses found in the given files."  # noqa: E501
                    logger.error(message)
                    raise ValueError(message)

    if inference_builder is None:
        message = "No InferenceBuilder subclass found in the given files."
        logger.error(message)
        raise AttributeError(message)

    logger.info("Loading successful.")

    return inference_builder
