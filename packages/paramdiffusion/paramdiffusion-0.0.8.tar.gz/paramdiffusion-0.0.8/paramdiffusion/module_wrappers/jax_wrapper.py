import jax
from paramdiffusion.sde.paramsymbolic_mean_cov import SDE_PARAM_SYMBOLIC
from typing import Callable, Tuple

def jax_sde_wrapper(sde: SDE_PARAM_SYMBOLIC) -> Tuple[Callable, Callable, Callable]:
    """
    Wraps a symbolic Stochastic Differential Equation (SDE) using JAX for efficient computation.

    This function provides JAX-compatible versions of three key operations associated with the SDE: generating perturbed data, calculating the sample loss, and computing the reverse time derivative. Each of these operations is jitted (JAX Just-In-Time compilation) and vectorized for performance.

    The `perturbed_data` function generates data with perturbations based on the SDE. The `sample_loss_l2` computes an L2 loss for approximating the SDE's score. The `reverse_time_derivative` calculates the reverse time derivative as part of the SDE's characteristics.

    Args:
        sde (SDE_PARAM_SYMBOLIC): An instance of a symbolic SDE class, initialized with JAX specific configurations. This SDE should provide the methods `perturbed_data`, `sample_loss_l2`, and `reverse_time_derivative` which are wrapped by this function.

    Returns:
        Tuple[Callable, Callable, Callable]: A tuple containing three JAX-jitted and vectorized functions:
            - perturbed_data: Callable for generating perturbed data based on the SDE.
            - sample_loss_l2: Callable for computing the L2 loss to approximate the SDE's score.
            - reverse_time_derivative: Callable for calculating the reverse time derivative of the SDE.

    Example Usage:
        >>> from paramdiffusion._utils import get_baseline_sde_no_parameters
        >>> from paramdiffusion import SDE_PARAM_SYMBOLIC
        >>> sde = SDE_PARAM_SYMBOLIC(*get_baseline_sde_no_parameters(dim=10),module='jax')
        >>> perturbed_data, sample_loss, reverse_derivative = jax_sde_wrapper(sde)
        >>> # Now you can use these functions with JAX's efficient computation.
    """

    perturbed_data = jax.jit(
        jax.vmap(sde.perturbed_data, in_axes=(0, 0, None, None, 0))
    )

    sample_loss_l2 = jax.jit(
        jax.vmap(sde.sample_loss_l2, in_axes=(0, None, None, 0, 0))
    )

    reverse_time_derivative = jax.jit(
        jax.vmap(sde.stochastic_reverse_time_derivative, in_axes=(0, None, None, 0, 0, 0))
    )

    return perturbed_data, sample_loss_l2, reverse_time_derivative
