"""__init__.py."""
import inspect
import os
from importlib.util import find_spec, module_from_spec, spec_from_file_location

from strangeworks_core.config.config import Config

from strangeworks_remote_job.artifact import ArtifactGenerator
from strangeworks_remote_job.remote import RemoteJobAPI


_cfg = Config()

_REMOTE_JOB_API_IMPL_FILE_LOC = os.getenv("REMOTE_JOB_API_FILE_LOCATION")
_REMOTE_JOB_API_CLASS_NAME = os.getenv("REMOTE_JOB_API_CLASS_NAME")

if _REMOTE_JOB_API_IMPL_FILE_LOC is None:
    raise ValueError("REMOTE_JOB_API_FILE_LOCATION is not set")
if _REMOTE_JOB_API_CLASS_NAME is None:
    raise ValueError("REMOTE_JOB_API_CLASS_NAME is not set")
# Early example of how to load a class from a file.
# This is currently working because the packages IBMJobAPI
# imports are already available in the environment. Simply importing
# the file would not work if it had dependencies that were not already
# available in the environment.
#
# TODO: Need to make sure we are very clear on how all this works.
spec = spec_from_file_location("job", _REMOTE_JOB_API_IMPL_FILE_LOC)
mymod = module_from_spec(spec)
spec.loader.exec_module(mymod)


RemoteJobAPIClass: RemoteJobAPI = None
_classes = inspect.getmembers(mymod, inspect.isclass)

for name, _class in _classes:
    if name == _REMOTE_JOB_API_CLASS_NAME:
        RemoteJobAPIClass = _class
        break

if RemoteJobAPIClass is None:
    raise ValueError(
        f"unable to inject the {_REMOTE_JOB_API_CLASS_NAME} implementation of the RemoteJobAPI class."  # noqa
    )


# An example of loading a function from a module that is in the environment already.
# _SUBMIT_ARTIFACT_GENERATOR_MODULE = os.getenv(
#     "SUBMIT_ARTIFACT_GENERATOR", "strangeworks_ibm.artifacts.circuit"
# )
# SubmitArtifactGen: ArtifactGenerator = None
# submit_mod_spec = find_spec(_SUBMIT_ARTIFACT_GENERATOR_MODULE)
# if submit_mod_spec is None:
#     raise ValueError(f"unable to find {_SUBMIT_ARTIFACT_GENERATOR_MODULE} module.")
# submit_mod_spec.loader.exec_module(submit_mod)
# _functions = inspect.getmembers(submit_mod)
# for name, _fn in _functions:
#     if name == "generator":
#         SubmitArtifactGen = _fn
#         break
def _get_generator_fn(module: str, function_name: str = "generator"):
    """Load the generator function from the module."""
    mod_spec = find_spec(module)
    if mod_spec is None:
        raise ValueError(f"unable to find the {module} module.")
    mod = module_from_spec(mod_spec)
    mod_spec.loader.exec_module(mod)

    _functions = inspect.getmembers(mod, inspect.isfunction)

    for name, _fn in _functions:
        if name == function_name:
            return _fn
    return None


no_op_artifact_generator = lambda *args, **kwargs: iter([])  # noqa

_SUBMIT_ARTIFACT_GENERATOR_MODULE = os.getenv("SUBMIT_ARTIFACT_GENERATOR")
if _SUBMIT_ARTIFACT_GENERATOR_MODULE:
    SubmitArtifactGen: ArtifactGenerator = _get_generator_fn(
        _SUBMIT_ARTIFACT_GENERATOR_MODULE
    )
else:
    SubmitArtifactGen: ArtifactGenerator = no_op_artifact_generator

_RESULT_ARTIFACT_GENERATOR_MODULE = os.getenv("RESULT_ARTIFACT_GENERATOR")
if _RESULT_ARTIFACT_GENERATOR_MODULE:
    ResultGenerator: ArtifactGenerator = _get_generator_fn(
        _RESULT_ARTIFACT_GENERATOR_MODULE
    )
else:
    ResultGenerator: ArtifactGenerator = no_op_artifact_generator
