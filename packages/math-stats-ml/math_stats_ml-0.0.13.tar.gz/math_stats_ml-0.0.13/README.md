# Utility functions for ["Mathematical Statistics with a View Toward Machine Learning"](https://mml.johnmyersmath.com/stats-book/index.html), by John Myers

A Python package for all utility functions used in the book and programming assignments. To install, do the usual:

```
pip install math_stats_ml
```

All other materials are contained [here](https://github.com/jmyers7/stats-book-materials).

**Table of contents**:

1. [`gd` submodule: Gradient descent utilities](#gd-submodule-gradient-descent-utilities)
    * [`GD_output` class: Container class for output of algorithms](#gd_output-class-container-class-for-output-of-algorithms)
    * [`GD` function: Gradient descent](#gd-function-gradient-descent)
    * [`SGD` function: Stochastic gradient descent](#sgd-function-stochastic-gradient-descent)
    * [`plot_gd` function: plot the output of gradient descent](#plot_gd-function-plot-the-output-of-gradient-descent)
    * [`plot_sgd` function: plot the output of stochastic gradient descent](#plot_sgd-function-plot-the-output-of-stochastic-gradient-descent)

## `gd` submodule: Gradient descent utilities

Contains all utilities for the gradient descent algorithms used in [the book](https://mml.johnmyersmath.com/stats-book/chapters/11-optim.html).

### `GD_output` class: Container class for output of algorithms

```python 
class GD_output
```

A class holding the outputs of both the gradient descent ([`GD`](#gradient-descent-gd)) and stochastic gradient descent ([`SGD`](#stochastic-gradient-descent-sgd)) algorithms. All attributes below are optional and default to `None`.

#### Attributes

Name | Type | Description
| :- | :- | :- |
|`parameters`| `dict` | A dictionary containing the parameters of the objective function passed to either [`GD`](#gradient-descent-gd) or [`SGD`](#stochastic-gradient-descent-sgd). Each value in the dictionary is a tensor whose zero-th dimension indexes the number of gradient steps.
| `per_step_objectives` | `torch.Tensor` | A tensor containing the running objective values, per gradient step.
| `per_epoch_objectives` | `torch.Tensor`| A tensor containing the running mean objective values, per epoch.
| `epoch_step_nums` | `torch.Tensor` | A tensor containing the number of each gradient step on which an epoch begins/ends.
| `grad_steps` | `iter` | An iterable ranging from $0$ to one less than the total number of gradient steps. (This is convenient for plotting purposes.)
| `lr` | `float` | Learning rate.
| `num_steps` | `int` | Number of gradient steps to run the gradient descent ([`GD`](#gradient-descent-gd)) algorithm.
| `decay_rate` | `float` | Learning rate decay.
| `batch_size` | `int` |Mini-batch size for the stochastic gradient descent ([`SGD`](#stochastic-gradient-descent-sgd)) algorithm.
| `num_epochs` | `int` | Number of epochs for the stochastic gradient descent ([`SGD`](#stochastic-gradient-descent-sgd)) algorithm.
| `max_steps` | `int` | Maximum number of gradient steps after which we terminate the stochastic gradient descent ([`SGD`](#stochastic-gradient-descent-sgd)) algorithm.
| `type_flag` | `str` | Either `None` or `gd`. In the latter case, indicates whether the `GD_output` object was obtained from the gradient descent ([`GD`](#gradient-descent-gd)) algorithm.

### `GD` function: Gradient descent

```python
GD(J, init_parameters, lr, num_steps, decay_rate=0)
```

Implementation of gradient descent. The notation below is intended to match the notation in the description in [the book](https://mml.johnmyersmath.com/stats-book/chapters/11-optim.html#gd-alg).

#### Output

The output type is an object of the [`GD_output` class](#container-class-for-output-of-algorithms-gd_output).

#### Parameters

Name | Type | Description
| :- | :- | :- |
| `J` | function | Objective function to be minimized. The parameters of the function are either a single tensor or a dictionary of tensors (in the case that the parameters fall into natural groups, e.g., weights and biases).
| `init_parameters` | `torch.Tensor` or `dict` | Initial parameters.
| `lr` | `float` | Learning rate, corresponding to $\alpha$ in the book.
| `num_steps` | `int` | The number of gradient steps after which the algorithm should halt, corresponding to $N$ in the book.
| `decay_rate` | `float` | Learning rate decay, corresponding to $\beta$ in the book. Defaults to `0`.


### `SGD` function: Stochastic gradient descent

```python
SGD(L, init_parameters, X, lr, batch_size, num_epochs, y=None, decay_rate=0, max_steps=-1, shuffle=True, random_state=None)
```

Implementation of stochastic gradient descent. The notation and terminology below is intended to match [the book](https://mml.johnmyersmath.com/stats-book/chapters/11-optim.html#sgd-alg).

#### Output

The output type is an object of the [`GD_output` class](#container-class-for-output-of-algorithms-gd_output).

#### Parameters

Name | Type | Description
| :- | :- | :- |
| `L` | function | Loss function for the algorithm. The call signature of the function is of the form `L(parameters, x)` or `L(parameters, x, y)`, where `x` is a feature vector and `y` is an (optional) ground truth label of a single instance in the dataset, and `parameters` is either a single parameter tensor or a dictionary of parameter tensors (in the case that the parameters fall into natural groups, e.g., weights and biases). We assume that `L` is "vectorized," so that it may accept a design matrix `X` in place of `x` and an entire vector of ground truth labels for `y`.
| `init_parameters` | `torch.Tensor` or `dict` | Initial parameters.
| `X` | `torch.Tensor` | Design matrix. The rows are the feature vectors that are fed into the loss function `L`.
| `lr` | `float` | Learning rate, corresponding to $\alpha$ in the book.
| `batch_size` | `int` | Mini-batch size, corresponding to $k$ in the book.
| `num_epochs` | `int` | The number of epochs after which the algorithm should halt, corresponding to $N$ in the book.
| `y` | `torch.Tensor` | Vector of ground truth labels for the data in the design matrix `X`. Optional, defaults to `None`.
| `decay_rate` | `float` | Learning rate decay, corresponding to $\beta$ in the book. Defaults to `0`.
| `max_steps` | `int` | Maximum number of gradient steps after which the algorithm should halt. Defaults to `-1`, in which case the algorithm will complete all `num_epochs` many epochs.
| `shuffle` | `bool` | Determines whether to shuffle the dataset before looping through an epoch. Defaults to `True`.
| `random_state` | `int` | If not `None` and `shuffle=True`, random seed to be passed to `torch.manual_seed`. Defaults to `None`.

### `plot_gd` function: plot the output of gradient descent

```python
plot_gd(gd_output, log=False, w=5, h=4, plot_title=True, plot_title_string='gradient descent',
        parameter_title=True, show_xlabel=True, xlabel='gradient steps', show_ylabel=True,
        ylabel='objective', alpha=1, color=None, ax=None)
```

Descriptions coming later...

### `plot_sgd` function: plot the output of stochastic gradient descent

```python
plot_sgd(sgd_output, log=False, w=5, h=4, plot_title=True, plot_title_string='stochastic gradient descent',
         parameter_title=True, show_step=True, show_epoch=True, show_xlabel=True, xlabel='gradient steps',
         show_ylabel=True, ylabel='objective', legend=False, per_step_alpha=0.25, per_step_color=None,
         per_step_label=None, per_epoch_color=None, per_epoch_label=None, s=50, ax=None)
```

Description coming later...
