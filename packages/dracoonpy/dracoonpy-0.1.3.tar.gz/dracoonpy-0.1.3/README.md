# _DRaCOoN_: Differential Regulation and CO-expression Networks
<p align="center">
  <img src="https://github.com/fmdelgado/DRACOONpy/raw/master/img/dracoon_logo.png" width="300"/>
</p>

## Introduction
_DRaCOoN_ offers a powerful, data-driven approach to uncover differential gene relationships across conditions, efficiently handling large datasets through various analysis modes. It generates networks by identifying gene pairs with changing associations.




<p align="center">
  <img src="https://github.com/fmdelgado/DRACOONpy/blob/master/img/graphical_abstract.jpg?raw=true" />
</p>

## Features

- Computes differential association and differential regulatory networks.
- Optimized for large datasets.
- Supports multiple working modes based on available data and analysis goals.
- Internal parallelization for faster computation.
- Utilizes Numba for just-in-time (JIT) compilation, accelerating the analysis process.

## Requirements

- Python 3.x
- Additional Python libraries as specified in `requirements.txt`

## Installation

### Using pip
```bash
pip install -i https://test.pypi.org/simple/dracoon
```

### From source

```bash
git clone https://github.com/fmdelgado/DRaCOoNpy.git
cd DRaCOoN/app
pip install -r requirements.txt
```

### Imports

```python
# if installed from pip
import dracoon

# if installed from source
from app.dracoon import dracoon
```

## Algorithmic Overview

The algorithm operates in several major steps:

1. **Data Input**: Accepts an expression dataset (microarray or RNA-Seq) with multiple samples across two conditions. A minimum of 20 samples per condition is recommended for meaningful results.
  
2. **Background Model Estimation**: Computes a permutation test-based background model for significance estimation.

3. **Differential Metrics Calculation**: Calculates two differential metrics, absolute difference \(_Δr_\) and shift difference \(_s_\), for network edges.

4. **Significance Testing**: Assigns p-values based on the background model and adjusts for multiple testing.


### Algorithmic Details

_DRaCOoN_ assesses the change in condition-specific correlations between pairs of genes. It utilizes different association metrics like, Pearson's _r_ and Spearman's _ρ_ correlation coefficients or an entropy-based metric. 
Then it computes differential metrics based on these values.

#### Differential Metrics
- **absdiff**: Absolute difference in the association between two genes across two conditions, estimated as:
 <p align="center">
<img src="https://latex.codecogs.com/svg.image?{\color{Gray}\Delta&space;r(absdiff)=|r_{A}-r_{B}|}"/>
</p>

- **shift**: The relative change in association between two genes across two conditions with respect to their condition-agnostic association, estimated as:
 <p align="center">
<img src="https://latex.codecogs.com/svg.image?{\color{Gray}s(shift)=\frac{r_{A}&plus;r_{B}}{2}-r"/>
</p>

#### P-value Estimation (`pval_method`)

- **permutation**: Only available when `matrixform = False`. For each evaluated gene pair, shuffles their values to create a distribution of \( n \) random values for both _absdiff_ and _shift_.

- **background**: Uses a background distribution estimated from \( n \) random pairs of genes that have been shuffled randomly.

- **fitted_background**: Fits a set of known distribution to the previous background model and uses the best-fitting distribution to estimate p-values analytically.

Then, p-values for both _absdiff_ and _shift_ are adjusted using one of the multiple methods available at [statmodels](https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.multipletests.html). By default,. p-value adjustment method is Benjamini/Hochberg (_fdr_bh_).
The final output of `DRaCOoN` includes those relationships whose  _absdiff_ or _shift_ is lower than a significance threshold, 0.05 by default.


### Working Modes

- **Mode 1**: Differential Co-expression (DC) for all possible gene-gene associations. Produces an undirected network.
  
- **Mode 2**: User-defined associations for differential examination (Pathway-level DC or Differential Regulation). Produces a directed network.

For more detailed information on the algorithm, please refer to the academic paper (citation needed).

### Parameters

- **cond_data**: The condition data frame.
- **biom_data**: The gene expression data frame.
- **DRaCOoN_program**: Either `DR` for differential regulation, `DC` for differential correlation.
- **associations_df**: Only for `DR` mode. In `DR` associations_df is a dataframe containing the set of source-target interactions to evaluate, containing columns _source_ and _target_. 
- **significance**: The significance level to use as a threshold for adjusted p-values, 0.05 by default.
- **association_measure**: The association measure to use, either `entropy`, `pearson` or `spearman`. By default `entropy`.
- **pval_method**: Either `permutation`, `background` or `fitted_background`. By default `fitted_background`.
- **distributions_to_fit**: If using `fitted_background`, the distributions to fit. By default:
  - best_dists_absdiff = ['expon', 'logistic', 'rayleigh', 'norm', 'gumbel_r', 'pareto', 'laplace', 'kstwobign',
                                    'moyal', 'halfnorm']
  - best_dists_shift = ['logistic', 'norm', 'laplace', 'gumbel_l', 'gumbel_r', 'uniform', 'expon', 'rayleigh',
                                  'hypsecant']
  - See other available distributions at the [fitter documentation](https://fitter.readthedocs.io/en/latest/faqs.html#what-are-the-distributions-available).
- **timeout_fitter**: If using `fitted_background`, the maximum time to fit a distribution, by default 60 seconds.
- **pvalue_adjustment_method**: `fdr_bh` by default.
- **iters**: If running permutation tests, the number of iterations, by default 10 000.
- **association_pvalue_filter**: (Optional) filters conditional relationships based on the adjusted p-value of the condition-specific associations.
- **matrixform**: Recommended for small datasets (<1000 genes, <1000 samples). Default `True`.
- **verbose**: If `True`, shows the algorithmic progress. By default `False`.

### Methods

The main method of _DRaCOoN_ is `run()`. This method sequentially runs the following methods:

- `preprocessing()`
- `estimate_background_model()`
- `calculate_correlations()`
- `threshold_results()`

For more detailed information on the algorithm, please refer to the academic paper (citation needed).

## Contributing

If you find any bugs or wish to propose new features, please let us know.

