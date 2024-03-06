from typing import Union, List, Callable
import logging
import pkg_resources
import os
import symengine
from functools import lru_cache, wraps


def get_installed_packages():
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]
    return installed_packages


def get_standard_packages():
    # Get the directory where standard library modules are located
    std_lib_dir = os.path.dirname(os.__file__)

    # List all files in the standard library directory
    std_lib_modules = os.listdir(std_lib_dir)

    # Filter out directories and non-Python files
    std_lib_modules = [module[:-3] for module in std_lib_modules if module.endswith(".py")]

    return std_lib_modules


def get_all_packages():
    installed_packages = get_installed_packages()
    std_lib_modules = get_standard_packages()
    all_packages = installed_packages + std_lib_modules
    return all_packages


_ALL_PACKAGES = get_all_packages()

def is_package_installed(pkg_name, installed_packages=None):
    installed_packages = (
        get_all_packages() if installed_packages is None else installed_packages
    )
    return pkg_name in installed_packages


def set_seed(seed: int):
    packages = ["torch", "numpy", "random", "tensorflow"]
    installed_packages = _ALL_PACKAGES
    for package in packages:
        if is_package_installed(package, installed_packages=installed_packages):
            if package == "torch":
                import torch

                torch.manual_seed(seed)
            elif package == "numpy":
                import numpy as np

                np.random.seed(seed)
            elif package == "random":
                import random

                random.seed(seed)
            elif package == "tensorflow":
                import tensorflow as tf

                tf.random.set_seed(seed)
            else:
                raise ValueError(f"Package {package} not supported.")
        else:
            print(f"Not setting seed for {package} as it's not installed.")


def seed_decorator(seed=None):
    """Decorator to set the seed before calling the function."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if seed is not None:
                set_seed(seed)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def set_high_precision():
    packages = ["torch", "jax", "tensorflow"]
    installed_packages = _ALL_PACKAGES
    for package in packages:
        if is_package_installed(package, installed_packages=installed_packages):
            if package == "torch":
                import torch

                torch.set_default_dtype(torch.float64)
            elif package == "jax":
                import jax

                jax.config.update("jax_enable_x64", True)
            elif package == "tensorflow":
                import tensorflow as tf

                tf.keras.backend.set_floatx("float64")
            else:
                raise ValueError(f"Package {package} not supported")


def set_default_precision():
    packages = ["torch", "jax", "tensorflow"]
    installed_packages = _ALL_PACKAGES
    for package in packages:
        if is_package_installed(package, installed_packages=installed_packages):
            if package == "torch":
                import torch

                torch.set_default_dtype(torch.float32)
            elif package == "jax":
                import jax

                jax.config.update("jax_enable_x64", False)
            elif package == "tensorflow":
                import tensorflow as tf

                tf.keras.backend.set_floatx("float32")
            else:
                raise ValueError(f"Package {package} not supported")


def high_precision_and_reset_decorator():
    """Decorator to set the precision to high before calling the function and then set the precision back to the default."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            set_high_precision()
            result = func(*args, **kwargs)
            set_default_precision()
            return result

        return wrapper

    return decorator


class LogColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class CustomFormatter(logging.Formatter):
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: LogColors.OKBLUE + format + LogColors.ENDC,
        logging.INFO: LogColors.OKGREEN + format + LogColors.ENDC,
        logging.WARNING: LogColors.WARNING + format + LogColors.ENDC,
        logging.ERROR: LogColors.FAIL + format + LogColors.ENDC,
        logging.CRITICAL: LogColors.FAIL + format + LogColors.ENDC,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def get_logger() -> logging.Logger:
    # Create a logger
    logger = logging.getLogger("paramdiffusion_logger")
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    # Create a console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create and add the formatter to the handler
    ch.setFormatter(CustomFormatter())

    # Add the handler to the logger
    logger.addHandler(ch)
    return logger


def arrays_equal(
    arrays: List,
    equality_comparison: Callable[[List], bool],
    almost_equality_comparison: Callable[[List], bool],
    msg: Union[None, str] = None,
    silent: bool = True,
    allow_almost_equal: bool = False,
):
    equal = True
    almost_equal = False
    for i in range(len(arrays) - 1):
        if equality_comparison(arrays[i], arrays[i + 1]):
            pass

        elif almost_equality_comparison(arrays[i], arrays[i + 1]):
            if allow_almost_equal:
                almost_equal = True
                equal = False
            else:
                raise AssertionError(
                    f"Array {i} : {arrays[i]} != Array {i+1} : {arrays[i+1]}"
                )
        else:
            if allow_almost_equal:
                raise AssertionError(
                    f"Array {i} : {arrays[i]} != or ~= Array {i+1} : {arrays[i+1]}"
                )
            else:
                raise AssertionError(
                    f"Array {i} : {arrays[i]} != Array {i+1} : {arrays[i+1]}"
                )

    if not silent:
        if equal:
            print(f"The {msg} arrays are equal")
        elif almost_equal:
            print(f"The {msg} arrays are almost equal")


def check_nan_inf(
    array: List,
    msg: str,
    nan_check: Callable[[List], bool],
    infinity_check: Callable[[List], bool],
    logger: logging.Logger = get_logger(),
) -> bool:
    ret_val = False
    if nan_check(array):
        logger.error(f"{msg} has NAN values")
        ret_val = True
    if infinity_check(array):
        logger.error(f"{msg} has INF values")
        ret_val = True
    return ret_val


class SanityChecker:
    @classmethod
    def sanity_check_inputs(
        cls,
        name,
        inputs: dict[str, dict[str, any]],
        expected_keys,
        optional_keys={},
        logger: logging.Logger = get_logger(),
    ) -> None:
        # Check for unexpected keys in inputs
        for key in inputs.keys():
            if key not in expected_keys and key not in optional_keys:
                logger.warning(
                    f"{cls.__name__}, {name}: Ignoring unexpected key: {key}!"
                )

        # Check if all expected keys are present in inputs
        for expected_key in expected_keys:
            if expected_key not in inputs:
                logger.error(
                    f"{cls.__name__}, {name}: Missing expected key: {expected_key}!"
                )

    @classmethod
    def sanity_check_function_inputs(
        cls,
        name,
        inputs: dict[str, dict[str, any]],
        expected_keys,
        logger: logging.Logger = get_logger(),
    ) -> None:
        # Check for unexpected keys in inputs
        for key in inputs.keys():
            if key not in expected_keys:
                logger.warning(
                    f"{cls.__name__}, {name}: Unexpected key: {key}! The key, {key}, will be passed to the {name} function, but ignored by derived functions."
                )

        # Check if all expected keys are present in inputs
        for expected_key in expected_keys:
            if expected_key not in inputs:
                logger.error(
                    f"{cls.__name__}, {name}: Missing expected key: {expected_key}!"
                )

    @classmethod
    def sanity_check_shape(
        cls, name, object_shape, expected_shape, logger: logging.Logger = get_logger()
    ) -> None:
        if object_shape != expected_shape:
            logger.error(
                f"{cls.__name__}, {name}: Expected shape: {expected_shape}, but got: {object_shape}!"
            )

@lru_cache(maxsize=None)
def get_baseline_sde_no_parameters(DIM: int):
    variable = symengine.symbols("t", real=True, positive=True)
    initial_data = symengine.symarray("data0", DIM)

    mean = symengine.Matrix(
        (
            symengine.exp(
                -1 / 4 * variable**2 * (80 - 0.002) - 1 / 2 * variable * 0.002
            )
            * initial_data
        ).tolist()
    )
    covariance = (1 - symengine.exp(-1 / 2 * variable**2 * (80 - 0.002) - variable * 0.002)) ** 2 * symengine.diag(*[1] * DIM)

    inputs = {
        "mean": {"initial_mean": initial_data, "parameters": []},
        "covariance": {"parameters": []},
    }

    return variable, mean, covariance, inputs

@lru_cache(maxsize=None)
def get_baseline_sde_parameters(DIM: int):
    variable = symengine.symbols("t", real=True, positive=True)
    initial_data = symengine.symarray("data0", DIM)

    mean_parameters = symengine.symarray("mean_parameters", 2)

    mean = symengine.Matrix(
        (
            symengine.exp(
                -1 / 4 * variable**2 * (mean_parameters[0] - mean_parameters[1])
                - 1 / 2 * variable * mean_parameters[1]
            )
            * initial_data
        ).tolist()
    )

    covariance_parameters = symengine.symarray("covariance_parameters", 2)

    covariance = (
        1
        - symengine.exp(
            -1 / 2 * variable**2 * (covariance_parameters[0] - covariance_parameters[1])
            - variable * covariance_parameters[1]
        )
    ) ** 2 * symengine.diag(*[1] * DIM)

    inputs = {
        "mean": {"initial_mean": initial_data, "parameters": mean_parameters},
        "covariance": {"parameters": covariance_parameters},
    }
    return variable, mean, covariance, inputs


# todo write this function for testing sde, test cov_i_j = t**(polynomial + 1) + epsilon
def test_stochastic_reconstruction_from_noise_and_perturbed_data(sde, sde_parameters, module, DIM, SEED=0, final_time=1.0, initial_time=0.0, num_steps=1000, logger=get_logger()):
    #variable, mean, covariance, inputs = get_baseline_sde_parameters(DIM)

    
    mean_parameters = sde_parameters["mean_parameters"]
    covariance_parameters = sde_parameters["covariance_parameters"]
    if module == "torch":
        import torch
        time = torch.tensor(final_time)
        initial_data = torch.tensor([1.0] * DIM)
        noise = torch.randn_like(initial_data)
        timespace = torch.linspace(time, initial_time, num_steps)
    elif module == "jax":
        import jax
        import jax.numpy as jnp
        time = jnp.array(final_time)
        initial_data = jnp.array([1.0] * DIM)
        key = jax.random.PRNGKey(SEED)
        key, subkey = jax.random.split(key)

        noise = jax.random.normal(shape=initial_data.shape, key=subkey) 
        timespace = jnp.linspace(time, initial_time, num_steps)

    sample = sde.perturbed_data(
        time, initial_data, mean_parameters, covariance_parameters, noise)

    delta_time = timespace[1] - timespace[0]


    xts = []

    xt = sample

    for t in timespace:
        xts.append(xt)
        score = sde.score(t, initial_data, mean_parameters, covariance_parameters, xt)
        if module == "torch":
            noise = torch.randn_like(xt)
        elif module == "jax":
            key, subkey = jax.random.split(key)
            noise = jax.random.normal(shape=xt.shape, key=subkey)

        dxdt = sde.stochastic_reverse_time_derivative(t, mean_parameters, covariance_parameters, score, xt, noise)
        xt = xt + delta_time * dxdt

    #print(xts[:10], xts[-10:])
    print(xts[0], xts[-1])
    #print(xt)

    if module == "torch":
        if torch.any(torch.isnan(xt)):
            logger.warn(f"The final states at initial time {initial_time} contain NAN values")
            logger.info("Evaluating at the time before the initial time")
        
            assert torch.allclose(xts[-1], initial_data, atol=1e-3, equal_nan=False), "Perturbed data: Almost final states are not close to initial data"
        else:
            assert torch.allclose(xt, initial_data, atol=1e-3, equal_nan=False), "Perturbed data: Final states are not close to initial data"
    elif module == "jax":
        if jnp.any(jnp.isnan(xt)):
            logger.warn(f"The final states at initial time {initial_time} contain NAN values")
            logger.info("Evaluating at the time before the initial time")
        
            assert jnp.allclose(xts[-1], initial_data, atol=1e-3, equal_nan=False), "Perturbed data: Almost final states are not close to initial data"
        else:
            assert jnp.allclose(xt, initial_data, atol=1e-3, equal_nan=False), "Perturbed data: Final states are not close to initial data"



    if module == "torch":
        noise = torch.randn_like(initial_data)
    elif module == "jax":
        key, subkey = jax.random.split(key)
        noise = jax.random.normal(shape=initial_data.shape, key=subkey)


    # Test with random noise
    xts = []
    xt = noise
    for t in timespace:
        xts.append(xt)
        score = sde.score(t, initial_data, mean_parameters, covariance_parameters, xt)
        if module == "torch":
            noise = torch.randn_like(xt)
        elif module == "jax":
            key, subkey = jax.random.split(key)
            noise = jax.random.normal(shape=xt.shape, key=subkey)

        dxdt = sde.stochastic_reverse_time_derivative(t, mean_parameters, covariance_parameters, score, xt, noise)
        xt = xt + delta_time * dxdt

    #print(xts[:10], xts[-10:])
    print(xts[0], xts[-1])    
    #print(xt)

    if module == "torch":
        if torch.any(torch.isnan(xt)):
            logger.warn(f"The final states at initial time {initial_time} contain NAN values")
            logger.info("Evaluating at the time before the initial time")
        
            assert torch.allclose(xts[-1], initial_data, atol=1e-3, equal_nan=False), "Random noise: Almost final states are not close to initial data"
        else: 
            assert torch.allclose(xt, initial_data, atol=1e-3, equal_nan=False), "Random noise: Final states are not close to initial data"
    elif module == "jax":
        if jnp.any(jnp.isnan(xt)):
            logger.warn(f"The final states at initial time {initial_time} contain NAN values")
            logger.info("Evaluating at the time before the initial time")
            assert jnp.allclose(xts[-1], initial_data, atol=1e-3, equal_nan=False), "Random noise: Almost final states are not close to initial data"
        else:
            assert jnp.allclose(xt, initial_data, atol=1e-3, equal_nan=False), "Random noise: Final states are not close to initial data"


def test_deterministic_reconstruction_from_noise_and_perturbed_data(sde, sde_parameters, module, DIM, SEED=0, final_time=1.0, initial_time=0.0, num_steps=1000, logger=get_logger()):
    #variable, mean, covariance, inputs = get_baseline_sde_parameters(DIM)

    
    mean_parameters = sde_parameters["mean_parameters"]
    covariance_parameters = sde_parameters["covariance_parameters"]
    if module == "torch":
        import torch
        time = torch.tensor(final_time)
        initial_data = torch.tensor([1.0] * DIM)
        noise = torch.randn_like(initial_data)
        timespace = torch.linspace(time, initial_time, num_steps)
    elif module == "jax":
        import jax
        import jax.numpy as jnp
        time = jnp.array(final_time)
        initial_data = jnp.array([1.0] * DIM)
        key = jax.random.PRNGKey(SEED)
        key, subkey = jax.random.split(key)

        noise = jax.random.normal(shape=initial_data.shape, key=subkey) 
        timespace = jnp.linspace(time, initial_time, num_steps)

    sample = sde.perturbed_data(
        time, initial_data, mean_parameters, covariance_parameters, noise)

    delta_time = timespace[1] - timespace[0]


    xts = []

    xt = sample

    for t in timespace:
        xts.append(xt)
        score = sde.score(t, initial_data, mean_parameters, covariance_parameters, xt)
        dxdt = sde.deterministic_reverse_time_derivative(t, mean_parameters, covariance_parameters, score, xt)
        xt = xt + delta_time * dxdt

    #print(xts[:10], xts[-10:])
    print(xts[0], xts[-1])
    #print(xt)

    if module == "torch":
        if torch.any(torch.isnan(xt)):
            logger.warn(f"The final states at initial time {initial_time} contain NAN values")
            logger.info("Evaluating at the time before the initial time")
        
            assert torch.allclose(xts[-1], initial_data, atol=1e-3, equal_nan=False), "Perturbed data: Almost final states are not close to initial data"
        else:
            assert torch.allclose(xt, initial_data, atol=1e-3, equal_nan=False), "Perturbed data: Final states are not close to initial data"
    elif module == "jax":
        if jnp.any(jnp.isnan(xt)):
            logger.warn(f"The final states at initial time {initial_time} contain NAN values")
            logger.info("Evaluating at the time before the initial time")
        
            assert jnp.allclose(xts[-1], initial_data, atol=1e-3, equal_nan=False), "Perturbed data: Almost final states are not close to initial data"
        else:
            assert jnp.allclose(xt, initial_data, atol=1e-3, equal_nan=False), "Perturbed data: Final states are not close to initial data"



    if module == "torch":
        noise = torch.randn_like(initial_data)
    elif module == "jax":
        key, subkey = jax.random.split(key)
        noise = jax.random.normal(shape=initial_data.shape, key=subkey)


    # Test with random noise
    xts = []
    xt = noise
    for t in timespace:
        xts.append(xt)
        score = sde.score(t, initial_data, mean_parameters, covariance_parameters, xt)

        dxdt = sde.deterministic_reverse_time_derivative(t, mean_parameters, covariance_parameters, score, xt)
        xt = xt + delta_time * dxdt

    #print(xts[:10], xts[-10:])
    print(xts[0], xts[-1])    
    #print(xt)

    if module == "torch":
        if torch.any(torch.isnan(xt)):
            logger.warn(f"The final states at initial time {initial_time} contain NAN values")
            logger.info("Evaluating at the time before the initial time")
        
            assert torch.allclose(xts[-1], initial_data, atol=1e-3, equal_nan=False), "Random noise: Almost final states are not close to initial data"
        else: 
            assert torch.allclose(xt, initial_data, atol=1e-3, equal_nan=False), "Random noise: Final states are not close to initial data"
    elif module == "jax":
        if jnp.any(jnp.isnan(xt)):
            logger.warn(f"The final states at initial time {initial_time} contain NAN values")
            logger.info("Evaluating at the time before the initial time")
            assert jnp.allclose(xts[-1], initial_data, atol=1e-3, equal_nan=False), "Random noise: Almost final states are not close to initial data"
        else:
            assert jnp.allclose(xt, initial_data, atol=1e-3, equal_nan=False), "Random noise: Final states are not close to initial data"