# stochasticclock

![](example_figures/Example_illustration.png)

A module calculating the stochastic deviations in timepoints for atomic clocks. 

The code is an application of the theory presented in Galleani et al. (2003), doi:10.1088/0026-1394/40/3/305.

The module's current functionality calculates stochastic deviations using

- The exact iterative solution to the SDE `Galleani_exact()`

Stochastic deviations can be visualised using `clock_error()`, and their distributions simulated with `deviation_distribution()`.

Please consult the Jupyter notebook for instructions.

