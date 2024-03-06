from paramdiffusion.sde.paramsymbolic_mean_cov import SDE_PARAM_SYMBOLIC
import torch


class PytorchSDEWrapper:
    """
    Wraps a symbolic Stochastic Differential Equation (SDE) for PyTorch-based computation.

    This class provides PyTorch-compatible versions of three key operations associated with the SDE: generating perturbed data, calculating the sample loss, and computing the reverse time derivative. Each of these operations is vectorized using PyTorch's vectorization capabilities for enhanced performance.

    The `perturbed_data` method generates data with perturbations based on the SDE. The `sample_loss_l2` method computes an L2 loss for approximating the SDE's score. The `reverse_time_derivative` method calculates the reverse time derivative as part of the SDE's characteristics.

    Args:
        sde (SDE_PARAM_SYMBOLIC): An instance of a symbolic SDE class, initialized with PyTorch specific configurations. This SDE should provide the methods `perturbed_data`, `sample_loss_l2`, and `reverse_time_derivative` which are wrapped by this class.

    Attributes:
        perturbed_data (Callable): A method for generating perturbed data based on the SDE, vectorized for PyTorch.
        sample_loss_l2 (Callable): A method for computing the L2 loss to approximate the SDE's score, vectorized for PyTorch.
        reverse_time_derivative (Callable): A method for calculating the reverse time derivative of the SDE, vectorized for PyTorch.

    Example Usage:
        >>> from paramdiffusion._utils import get_baseline_sde_no_parameters
        >>> from paramdiffusion import SDE_PARAM_SYMBOLIC
        >>> sde = SDE_PARAM_SYMBOLIC(*get_baseline_sde_no_parameters(dim=10), module='torch')
        >>> sde_wrapper = PytorchSDEWrapper(sde)
        >>> # Use the methods like sde_wrapper.perturbed_data(...)
        >>> # for PyTorch-optimized SDE operations.
    """

    def __init__(self, sde: SDE_PARAM_SYMBOLIC):

        self.perturbed_data = torch.compile(torch.vmap(
            sde.perturbed_data, in_dims=(0, 0, None, None, 0)
        ))

        self.sample_loss_l2 = torch.compile(torch.vmap(
            sde.sample_loss_l2, in_dims=(0, None, None, 0, 0)
        ))

        self.reverse_time_derivative = torch.compile(torch.vmap(
            sde.stochastic_reverse_time_derivative, in_dims=(0, None, None, 0, 0, 0)
        ))
