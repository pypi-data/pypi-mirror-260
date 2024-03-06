import sys
import numpy as _np
import symengine
import sympy
from typing import Callable, Any, TypeAlias
from paramdiffusion._utils.test_utils import SanityChecker
import psutil
from multiprocessing import Pool
from collections.abc import Iterable
from sympy.printing.printer import Printer

__all__ = ['SDE_PARAM_SYMBOLIC']

Parameter: TypeAlias = Any


def l2(x):
    return x.T @ x

def symengine_simplify(expr):
    return expr.simplify()

def compute_diff(f, variable):
    # Assuming `variable` needs to be accessible here, you might need to adjust how it's passed
    return f.diff(variable)


def multiply_AB_symengine(A, B):
    # Ensure A is a diagonal matrix
    if not A.is_diagonal:
        raise ValueError("Matrix A must be diagonal.")

    if B.is_diagonal:
        return multiply_diag_matricies(A, B)
    # Diagonal elements of A as a matrix for element-wise multiplication
    diagonal_A = [A[i, i] for i in range(A.rows)]
    return symengine.Matrix([B[j, :] * diagonal_A[j] for j in range(B.rows)])

def multiply_diag_matricies(A,B):
    return symengine.diag(*[A[i, i] * B[i, i] for i in range(A.rows)])

def multiply_BA_symengine(B, A):
    # Ensure A is a diagonal matrix
    if not A.is_diagonal:
        raise ValueError("Matrix A must be diagonal.")

    if B.is_diagonal:
        return multiply_diag_matricies(B, A)
    # Diagonal elements of A as a matrix for element-wise multiplication
    return symengine.Matrix([B[:, j].T * A[j, j] for j in range(B.cols)]).T


def matrix_inverse(A):
    if A.is_diagonal:
        return symengine.diag(*[1 / A[i, i] for i in range(A.rows)])

    return A.inv()


def cholesky_decomposition(expr):
    if expr.is_diagonal:
        print("diagonal")

        return symengine.diag(*[symengine.sqrt(expr[i, i]) for i in range(expr.rows)])
    else:
        return expr.cholesky()


class SDE_PARAM_SYMBOLIC(SanityChecker):
    """
    Symbolic representation of a Stochastic Differential Equation (SDE) with time-dependent mean and covariance. 
    This class is designed for use with computational frameworks such as PyTorch, NumPy, JAX, etc. It facilitates 
    the symbolic computation of various SDE-related quantities, with an emphasis on using its lambdified functions 
    through appropriate wrappers for efficient computation.

    The class abstracts an SDE by deriving its drift and diffusion coefficients from the provided mean and 
    covariance functions. Key operations related to the SDE (such as computing perturbed data, sample loss, 
    and reverse time derivative) are provided in a symbolic form and are intended to be accessed through 
    lambdified functions.

    The mean function is assumed to be a linear transformation of the data, which simplifies the derivation 
    of the drift coefficient. The covariance function provides the diffusion characteristics of the SDE.

    The class is designed to work seamlessly with different computational frameworks, and it's strongly recommended 
    to use the lambdified functions through a wrapper specific to the desired framework (e.g., PyTorch or JAX). 
    These wrappers provide an optimized and user-friendly interface to the complex symbolic operations defined 
    within the class.

    Key Attributes (For Internal Use):
        - symbolic_mean: Symbolic representation of the SDE's mean.
        - symbolic_covariance: Symbolic representation of the SDE's covariance.
        - symbolic_drift: Derived symbolic drift coefficient.
        - symbolic_diffusion_L: Derived symbolic diffusion under the assumption of an identity diffusion matrix. Cholesky decomposition of the diffusion term.
        - Various other symbolic functions related to the SDE.

    Important Methods (Intended for End-User Access Through Wrappers):
        - perturbed_data: Lambdified function for generating perturbed data.
        - sample_loss_l2: Lambdified function for computing sample loss.
        - reverse_time_derivative: Lambdified function for calculating the reverse time derivative.

    Args:
        variable (symengine.Symbol): Main variable of the SDE (usually time).
        mean (symengine.Matrix): Symbolic matrix for the mean function of shape (N, 1).
        covariance (symengine.Matrix): Symbolic matrix for the covariance function of shape (N, N).
        inputs (dict[str, dict[str, symengine.Expr | List]]): Dictionary containing input configurations for mean and covariance. 
            The dictionary should be of the form:
            ```python
            {
                "mean": {"initial_mean": initial_mean, "parameters": [...]},
                "covariance": {"parameters": [...]},
            }
            ```
        data (symengine.Matrix | None): Optional symbolic matrix for data.
        sanity_check (bool): Enables sanity checks if set to True.
        module (str): Computational framework to be used.
        printer (Printer | None): Optional printer for symbolic expressions.

    Example Usage:
        >>> from symengine import Symbol, Matrix
        >>> variable = Symbol('t')
        >>> mean = Matrix([[...]]) # Define mean matrix
        >>> covariance = Matrix([[...]]) # Define covariance matrix
        >>> inputs = {...} # Input configurations
        >>> sde = SDE_PARAM_SYMBOLIC(variable, mean, covariance, inputs, module='torch')
        >>> # Use a wrapper to access lambdified functions like sde.perturbed_data, sde.sample_loss, etc.

    Note:
        - The class is optimized for use with wrappers, which abstract away the complexity of directly interacting 
          with symbolic expressions and provide a user-friendly interface.
        - Direct use of the symbolic attributes and methods is possible but not recommended for general use cases.
    """
    def __init__(
        self,
        variable: symengine.Symbol,
        mean: symengine.Matrix,
        covariance: symengine.Matrix,
        inputs: dict[str, dict[str, Any]],
        data: symengine.Matrix | None = None,
        sanity_check=True,
        module: str = "torch",
        printer: Printer | None = None,
    ) -> None:

        super().__init__()

        # Sanity checks
        if sanity_check:
            self.sanity_check_shape("mean", mean.shape, (mean.shape[0], 1))
            self.sanity_check_shape(
                "covariance", covariance.shape, (mean.shape[0], mean.shape[0])
            )
            self.sanity_check_inputs("inputs", inputs, ["mean", "covariance"])

            self.sanity_check_inputs(
                'inputs["mean"]', inputs["mean"], ["initial_mean", "parameters"]
            )
            self.sanity_check_inputs(
                'inputs["covariance"]', inputs["covariance"], ["parameters"]
            )



        # Set the symbolic variables
        self.symbolic_mean = mean
        self.symbolic_covariance = covariance
        self.symbolic_covariance_decomposition = cholesky_decomposition(covariance)


        self.variable = variable

        # Create the symbolic data, model and noise for sampling pertubed data and noise for the reverse time derivative
        self.symbolic_data = (
            symengine.Matrix(symengine.symarray("data", mean.shape).tolist())
            if data is None
            else data
        )
        self.symbolic_model = symengine.Matrix(
            symengine.symarray("model", mean.shape).tolist()
        )
        self.symbolic_noise = symengine.Matrix(
            symengine.symarray("noise", mean.shape).tolist()
        )
        self.symbolic_reconstruction_noise = symengine.Matrix(
            symengine.symarray("recon_noise", mean.shape).tolist()
        )

        # Derive drift and convert it to an N x N matrix
#        self.symbolic_drift = symengine.Matrix(
#            _np.diag(
#                _np.array(
#                    mean.diff(variable).multiply_elementwise(
#                        mean.applyfunc(lambda x: 1 / x)
#                    )
#                ).reshape(-1)
#            ).tolist()
#        )

        self.symbolic_drift = symengine.diag( *(mean.diff(variable).multiply_elementwise( mean.applyfunc(lambda x: 1 / x))))

        self.symbolic_LQL = (
            covariance.diff(variable)
            - multiply_AB_symengine(self.symbolic_drift, covariance)
            - multiply_BA_symengine(covariance, self.symbolic_drift)
        )

        # self.symbolic_diffusion_LDL, self.symbolic_diffusion_matrix_LDL = self.symbolic_LQL.LDL()

        self.symbolic_diffusion_L = cholesky_decomposition(self.symbolic_LQL)

        self.symbolic_score = self._get_symbolic_score()

        self.symbolic_perturbed_data = self._get_perturbed_data()

        if self.symbolic_covariance_decomposition.is_diagonal:
            self.symbolic_sample_loss = multiply_AB_symengine(self.symbolic_covariance_decomposition.T, self.symbolic_model) + self.symbolic_noise
            
        else:
            self.symbolic_sample_loss = (
                self.symbolic_covariance_decomposition.T @ self.symbolic_model
                + self.symbolic_noise
            )
        
        # Original computation
        # self.symbolic_sample_loss = self.symbolic_covariance_decomposition.T @ (self.symbolic_model - self.symbolic_covariance.inv() @ (self.symbolic_mean - self.symbolic_perturbed_data))

        self.symbolic_stochastic_reverse_time_derivative = (
            self._get_symbolic_reverse_time_derivative()
        )

        #self.symbolic_deterministic_reverse_time_derivative = (
        #    self._get_non_ode_reverse_time_derivative()
        #) 
        # Lambdaify the symbolic expressions

        mean_parameters = inputs["mean"]["parameters"]
        initial_mean = inputs["mean"]["initial_mean"]
        covariance_parameters = inputs["covariance"]["parameters"]

        #with Pool(processes=psutil.cpu_count(logical=False)) as pool:

        #    self.symbolic_reverse_time_derivative = self.simplify(expression=self.symbolic_reverse_time_derivative, shape=(mean.shape[0],), pool=pool, conversion_type=sympy.Array)


        #    self.symbolic_perturbed_data = self.simplify(expression=self.symbolic_perturbed_data, shape=(mean.shape[0],), pool=pool, conversion_type=sympy.Array)

        #    self.symbolic_score = self.simplify(expression=self.symbolic_score, shape=(mean.shape[0],), pool=pool, conversion_type=sympy.Array)


        #    self.symbolic_sample_loss = self.simplify(expression=self.symbolic_sample_loss, shape=(mean.shape[0],), pool=pool, conversion_type=sympy.Array)

        self.symbolic_stochastic_reverse_time_derivative = sympy.Array(self.symbolic_stochastic_reverse_time_derivative)
        self.symbolic_perturbed_data = sympy.Array(self.symbolic_perturbed_data)
        self.symbolic_score = sympy.Array(self.symbolic_score)
        self.symbolic_sample_loss = sympy.Array(self.symbolic_sample_loss)
        #self.symbolic_deterministic_reverse_time_derivative = sympy.Array(self.symbolic_deterministic_reverse_time_derivative)



        #self.deterministic_reverse_time_derivative = self.lambdify(
        #        [
        #            variable,
        #            mean_parameters,
        #            covariance_parameters,
        #            self.symbolic_model,
        #            self.symbolic_data,
        #        ],
        #        self.symbolic_deterministic_reverse_time_derivative,
        #        module=module,
        #        printer=printer,
        #    )
        

        self.stochastic_reverse_time_derivative = self.lambdify(
                [
                    variable,
                    mean_parameters,
                    covariance_parameters,
                    self.symbolic_model,
                    self.symbolic_data,
                    self.symbolic_reconstruction_noise,
                ],
                self.symbolic_stochastic_reverse_time_derivative,
                module=module,
                printer=printer,
            )
        

        self.perturbed_data = self.lambdify(
                [
                    variable,
                    initial_mean,
                    mean_parameters,
                    covariance_parameters,
                    self.symbolic_noise,
                ],
                self.symbolic_perturbed_data,
                module=module,
                printer=printer,
            )
        self.score = self.lambdify(
                [
                    variable,
                    initial_mean,
                    mean_parameters,
                    covariance_parameters,
                    self.symbolic_data,
                ],
                self.symbolic_score,
                module=module,
                printer=printer,
            )
        self.sample_loss = self.lambdify(
                [
                    variable,
                    mean_parameters,
                    covariance_parameters,
                    self.symbolic_model,
                    self.symbolic_noise,
                ],
                self.symbolic_sample_loss,
                module=module,
                printer=printer,
            )

        self.sample_loss_l2 = lambda *args: l2(self.sample_loss(*args).reshape(-1))
        if sanity_check:
            # get module dummy inputs
            match module:
                case "torch":
                    import torch

                    dummy_module = torch
                case "numpy" | "scipy":
                    import numpy

                    dummy_module = numpy
                case "jax":
                    import jax

                    dummy_module = jax.numpy
                case "cupy":
                    import cupy

                    dummy_module = cupy
                case "tensorflow":
                    import tensorflow

                    dummy_module = tensorflow
                case _:
                    raise NotImplementedError(
                        f"No sanity check for this module has been implemented yet. Simply remove the sanity check option, but use the {self.__class__.__name__} at your own risk"
                    )
            if module == "tensorflow":
                time = dummy_module.reshape(dummy_module.zeros(1), ())
            else:
                time = dummy_module.zeros(1).reshape(())
            dummy_initial_mean = dummy_module.zeros(mean.shape)
            dummy_mean_parameters = dummy_module.zeros(
                mean_parameters.shape
                if hasattr(mean_parameters, "shape")
                else len(mean_parameters)
            )
            dummy_covariance_parameters = dummy_module.zeros(
                covariance_parameters.shape
                if hasattr(covariance_parameters, "shape")
                else len(covariance_parameters)
            )

            dummy_model = dummy_initial_mean
            dummy_perturbed_data = dummy_initial_mean
            dummy_noise = dummy_initial_mean
            dummy_reconstruction_noise = dummy_initial_mean

            self.sanity_check_shape(
                "perturbed data",
                self.perturbed_data(
                    time,
                    dummy_initial_mean,
                    dummy_mean_parameters,
                    dummy_covariance_parameters,
                    dummy_noise
                ).shape,
                mean.shape,
            )

            self.sanity_check_shape(
                "sample loss",
                self.sample_loss(
                    time,
                    dummy_mean_parameters,
                    dummy_covariance_parameters,
                    dummy_model,
                    dummy_noise,
                ).shape,
                mean.shape,
            )

            self.sanity_check_shape(
                "sample loss l2 loss",
                self.sample_loss_l2(
                    time,
                    dummy_mean_parameters,
                    dummy_covariance_parameters,
                    dummy_model,
                    dummy_noise,
                ).shape,
                (),
            )

            self.sanity_check_shape(
                "reverse_time_derivative",
                self.stochastic_reverse_time_derivative(
                    time,
                    dummy_mean_parameters,
                    dummy_covariance_parameters,
                    dummy_model,
                    dummy_perturbed_data,
                    dummy_reconstruction_noise,
                ).shape,
                mean.shape,
            )

            self.sanity_check_shape(
                "score",
                self.score(
                    time,
                    dummy_initial_mean,
                    dummy_mean_parameters,
                    dummy_covariance_parameters,
                    dummy_perturbed_data,
                ).shape,
                mean.shape,
            )


    def _get_symbolic_score(self):
        """
        (Internal Method) Calculates the symbolic score of the Stochastic Differential Equation (SDE).

        This method is used internally to compute the symbolic representation of the SDE's score.
        Users should access the `self.symbolic_score` attribute to view the computed.

        The score is defined as the gradient w.r.t the data of the log-likelihood of the SDE's 
        probability density function. It is given by:
        s(x(t), t) = Sigma^-1 (m(x(t), t) - x(t))

        Returns:
            symengine.Matrix: Symbolic representation of the SDE's score function.

        Example Usage:
            >>> sde = SDE_PARAM_SYMBOLIC(...)
            >>> symbolic_score = sde.symbolic_score # Use cached computation.
            >>> symbolic_score = sde.get_symbolic_score() # Recompute the score.
        """
        term1 = self.symbolic_mean - self.symbolic_data
        term2 = matrix_inverse(self.symbolic_covariance)
        if term2.is_diagonal:
            return multiply_AB_symengine(term2, term1)

        return term2 @ term1

    def _get_symbolic_loss(self):
        """
        (Internal Method) Computes the symbolic loss function for the SDE.

        This method is used internally to compute the symbolic representation of the SDE's loss function.
        Users should access the `self.symbolic_sample_loss` attribute to view the computed loss.

        The loss function is used to quantify the difference between the model output and the 
        expected behavior of the SDE. It is defined as:
        Loss = A(t)^T (model_output - s(x(t), t)) = A(t)^T model_output + z 
        where A(t) is the Cholesky decomposition of the covariance matrix, and s(x(t), t) is the score function.

        Returns:
            symengine.Matrix: Symbolic representation of the SDE's loss function.

        Example Usage:
            >>> sde = SDE_PARAM_SYMBOLIC(...)
            >>> symbolic_loss = sde.symbolic_sample_loss # Cached version
            >>> symbolic_loss = sde.get_symbolic_loss() # Recompute the sample loss
        """
        return self.symbolic_covariance_decomposition.T @ (
            self.symbolic_model - self.symbolic_score
        )

    def _get_perturbed_data(self):
        """
        (Internal Method) Generates symbolic representation of perturbed data for the SDE.

        This method is used internally to compute the symbolic representation of perturbed data.
        Users should access the `self.symbolic_perturbed_data` attribute to view the perturbed data.

        The perturbed data are used in SDE simulation and are given by:
        x(t) = m(x(t), t) + A(t) @ z
        where A(t) is the Cholesky decomposition of the covariance matrix, and z is a noise term.

        Returns:
            symengine.Matrix: Symbolic representation of perturbed data.

        Example Usage:
            >>> sde = SDE_PARAM_SYMBOLIC(...)
            >>> symbolic_perturbed_data = sde.symbolic_perturbed_data # Cached computation
            >>> symbolic_perturbed_data = sde.get_perturbed_data() # Recompute the perturbed data
        """
        if self.symbolic_covariance_decomposition.is_diagonal:
            term1 = multiply_AB_symengine(self.symbolic_covariance_decomposition, self.symbolic_noise)
        else:
            term1 = self.symbolic_covariance_decomposition @ self.symbolic_noise
        return self.symbolic_mean + term1
        return (
            self.symbolic_mean
            + self.symbolic_covariance_decomposition @ self.symbolic_noise
        )

    def _get_non_ode_reverse_time_derivative(self):
        term1 = multiply_AB_symengine(self.symbolic_drift, self.symbolic_data)
        term2 = multiply_AB_symengine(self.symbolic_LQL, self.symbolic_model)
        return term1 - 1/2 * term2

    def _get_symbolic_reverse_time_derivative(self):
        """
        (Internal Method) Calculates the symbolic reverse time derivative for the SDE.

        This function is used internally for the backward computation in the SDE context.
        Users should access the `self.symbolic_reverse_time_derivative` attribute to view this derivative.

        Returns:
            symengine.Matrix: Symbolic representation of the SDE's reverse time derivative.

        Example Usage:
            >>> sde = SDE_PARAM_SYMBOLIC(...)
            >>> symbolic_reverse_time_derivative = sde.symbolic_reverse_time_derivative # Cached computation
            >>> symbolic_reverse_time_derivative = sde.get_symbolic_reverse_time_derivative() # Recompute the reverse time derivative.
        """
        term1 = multiply_AB_symengine(self.symbolic_drift, self.symbolic_data)
        if self.symbolic_LQL.is_diagonal:
            term2 = multiply_AB_symengine(self.symbolic_LQL, self.symbolic_model)
            term3 = multiply_AB_symengine(self.symbolic_diffusion_L, self.symbolic_reconstruction_noise)
        else:
            term2 = self.symbolic_LQL @ self.symbolic_model
            term3 = self.symbolic_diffusion_L @ self.symbolic_reconstruction_noise
        
        return term1 - term2 + term3
        
        
        
        return (
            self.symbolic_drift @ self.symbolic_data
            - self.symbolic_LQL @ self.symbolic_model
            + self.symbolic_diffusion_L @ self.symbolic_reconstruction_noise
        )

    @staticmethod
    def symbolify(
        parameters,
        expression,
        shape=None,
        module=None,
        printer=None,
        pool=None,
        conversion_type=None,
    ):
        """
        Converts a symbolic expression into a numerical function using the `lambdify` method. 
        Prior to lambdification, the expression is simplified for numerical efficiency.

        Args:
            parameters (list): A list of parameters that the expression depends on.
            expression (sympy.Expr | symengine.Expr): The symbolic expression to be converted.
            shape (tuple | None): Optional. The shape of the output if the expression represents a matrix or vector.
            module (str | None): The computational module to be used for lambdification (e.g., 'numpy', 'torch').
            printer (sympy.printing.Printer | None): Optional printer for converting expressions to strings.
            pool (multiprocessing.Pool | None): Optional multiprocessing pool for parallel simplification.
            conversion_type (type | None): The desired type for the output of the simplification process.

        Returns:
            function: A numerical function equivalent to the symbolic expression.

        Example Usage:
            >>> parameters = [x, y]
            >>> expression = x**2 + y**2
            >>> numerical_function = SDE_PARAM_SYMBOLIC.symbolify(parameters, expression, module='numpy')
            >>> result = numerical_function(2, 3)  # Evaluates the function at x=2, y=3
        """
        expression = SDE_PARAM_SYMBOLIC.simplify(expression, shape, pool, conversion_type)
        # return expression
        return SDE_PARAM_SYMBOLIC.lambdify(
            parameters,
            expression,
            modules=module,
            printer=printer,
        )

    @staticmethod
    def lambdify(
        parameters,
        expression,
        module=None,
        printer=None,
    ):
        """
        Converts a symbolic expression into a numerical function. This method is a wrapper around
        `sympy.lambdify` that allows for additional configuration and optimization.

        Args:
            parameters (list): A list of parameters that the expression depends on.
            expression (sympy.Expr | symengine.Expr): The symbolic expression to be converted.
            module (str | None): The computational module to be used for lambdification (e.g., 'numpy', 'torch').
            printer (sympy.printing.Printer | None): Optional printer for converting expressions to strings.

        Returns:
            function: A numerical function equivalent to the symbolic expression.

        Example Usage:
            >>> parameters = [x, y]
            >>> expression = x**2 + y**2
            >>> numerical_function = SDE_PARAM_SYMBOLIC.lambdify(parameters, expression, module='numpy')
            >>> result = numerical_function(2, 3)  # Evaluates the function at x=2, y=3
        """
        return sympy.lambdify(
            parameters,
            expression,
            modules=module,
            printer=printer,
            cse=True,
            docstring_limit=0,)

    @staticmethod
    def simplify(
        expression,
        shape=None,
        pool=None,
        conversion_type=None,
    ):
        """
        Simplifies a symbolic expression to optimize its numerical evaluation. This method can leverage
        parallel computing for faster processing of large expressions.

        Args:
            expression (sympy.Expr | symengine.Expr | Iterable): The symbolic expression or a collection of expressions to be simplified.
            shape (tuple | None): Optional. The shape of the output if the expression represents a matrix or vector.
            pool (multiprocessing.Pool | None): Optional multiprocessing pool for parallel simplification.
            conversion_type (type | None): The desired type for the output of the simplification process.

        Returns:
            sympy.Expr | Iterable: The simplified expression or collection of expressions.

        Example Usage:
            >>> expression = x**2 + 2*x + 1
            >>> simplified_expression = SDE_PARAM_SYMBOLIC.simplify(expression)
            >>> # simplified_expression will be (x + 1)**2
        """

        cls = type(expression) if conversion_type is None else conversion_type
        if pool is not None:
            if isinstance(expression, Iterable):
                if hasattr(cls, "shape") and hasattr(cls, "reshape"):
                    shape = (
                        expression.shape
                        if shape is None and hasattr(expression, "shape")
                        else shape
                    )
                    #expression = cls(pool.map(symengine_simplify, expression)).reshape(
                    #    *shape
                    #)
                    expression = cls(pool.map(sympy.simplify, expression)).reshape(
                        *shape
                    )
                else:
                    expression = cls(pool.map(sympy.simplify, expression))
            else:
                expression = cls(sympy.simplify(expression))
        else:
            expression = cls(sympy.simplify(expression))

        return expression