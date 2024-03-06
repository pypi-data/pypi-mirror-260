from typing import Any, TypeAlias, Collection

Module: TypeAlias = Any


def diag_indices(dim: int, ndim: int, module: Module) -> Collection:
    """Returns the indices for the diagonal elements of an array.

    Args:
        dim (int): The length of the diagonal
        ndim (int, optional): The number of dimensions to index over. Defaults to 2.
        module (Module, optional): A module which implements arange. Defaults to torch.

    Returns:
        Collection: The indices of the diagonal elements with the type depending on the module
    """
    idx = module.arange(dim)
    return (idx,) * ndim
