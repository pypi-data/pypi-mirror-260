# Py-SPMF
Python Wrapper for [SPMF Java library](http://www.philippe-fournier-viger.com/spmf).

## Information
This module contains python wrappers for pattern mining algorithms implemented in SPMF Java library. Each algorithm is implemented as a standalone Python class with fully descriptive and tested APIs. It also provides native support for Pandas dataframes.

Why? If you're in a Python pipeline, it might be cumbersome to use Java as an intermediate step. Using `Py-SPMF` you can stay in your pipeline as though Java is never used at all.

## Installation
[`pip install pyspmf`](https://pypi.org/project/spmf/)

Ensure Java Runtime Environment is also installed. Follow instructions [`here`](https://www.java.com/en/download/help/download_options.html). Test installation by running the following command on the terminal:

```
> java -version
java version "1.8.0_391"
Java(TM) SE Runtime Environment (build 1.8.0_391-b13)
Java HotSpot(TM) 64-Bit Server VM (build 25.391-b13, mixed mode)
```

## Usage
Example:
```python
from spmf.episode import EMMA

emma = EMMA(min_support=2, max_window=2, timestamp_present=True, transform=True)
output = emma.run_pandas(input_df)
```

Input:

| | Time points | Itemset
| ---- | ------ | -------
| 0	| 1	| a
| 1	| 2	| a
| 2	| 3	| a
| 3	| 3	| b
| 4	| 6	| a
| 5	| 7	| a
| 6	| 7	| b
| 7	| 8	| c
| 8	| 9	| b
| 9	| 11 | d

Output:

|	| Frequent episode | Support
| --- | ---------------- | -------
|0    |	a     |	5
|1    |	b	|     3
|2    |	a b	|     2
|3	|     a-> a |	3
|4	|     a -> b |	2
|5	|     a -> a b |  2

See [examples]('https://github.com/AakashVasudevan/Py-SPMF/tree/main/examples') for more details.

For a detailed explanation of the algorithm and parameters, refer to the corresponding webpage in the SPMF [documentation](http://www.philippe-fournier-viger.com/spmf/index.php?link=documentation.php).


### SPMF Executable

Download it from the [SPMF Website](http://www.philippe-fournier-viger.com/spmf/index.php?link=download.php).
It is assumed that the SPMF binary `spmf.jar` is located in the `binaries` directory inside `Py-SPMF`. If it is not, either symlink it, or use the `executable_path` parameter.


## Implementation Checklist

### Sequential Pattern Mining

| Algorithm| Type | Implemented
| -------- | ------- | ---------
| PrefixSpan | Frequent Sequential Pattern | &check;
| GSP | Frequent Sequential Pattern |
| SPADE | Frequent Sequential Pattern | &check;
| CM-SPADE | Frequent Sequential Pattern | &check;
| SPAM | Frequent Sequential Pattern | &check;
| CM-SPAM | Frequent Sequential Pattern |
| FAST | Frequent Sequential Pattern |
| LAPIN | Frequent Sequential Pattern |
| ClaSP | Frequent Closed Sequential Pattern | &check;
| CM-ClaSP | Frequent Closed Sequential Pattern | &check;
| CloFAST | Frequent Closed Sequential Pattern |
| CloSpan | Frequent Closed Sequential Pattern |
| BIDE+ | Frequent Closed Sequential Pattern |
| Post Processing SPAM or PrefixSpan | Frequent Closed Sequential Pattern |
| MaxSP | Frequent Maximal Sequential Pattern |
| VMSP | Frequent Maximal Sequential Pattern | &check;
| FEAT | Frequent Sequential Generator Pattern |
| FSGP | Frequent Sequential Generator Pattern |
| VGEN | Frequent Sequential Generator Pattern | &check;
| NOSEP | Non-overlapping Sequential Pattern | &check;
| GoKrimp | Compressing Sequential Pattern |
| TKS | Top-k Frequent Sequential Pattern | &check;
| TSP | Top-k Frequent Sequential Pattern |

### Episode Mining

| Algorithm| Type | Implemented
| -------- | ------- | ---------
| EMMA  | Frequent Episode | &check;
| AFEM | Frequent Episode | &check;
| MINEPI | Frequent Episode |
| MINEPI+ | Frequent Episode | &check;
| TKE | Top-k Frequent Episodes | &check;
| MaxFEM | Maximal Frequent Episodes | &check;
| POERM | Episode Rules |
| POERM-ALL | Episode Rules |
| POERMH | Episode Rules |
| NONEPI | Episode Rules | &check;
| TKE-Rules | Episode Rules | &check;
| AFEM-Rules | Episode Rules | &check;
| EMMA-Rules | Epsiode Rules | &check;
| MINEPI+-Rules | Episode Rules |
| HUE-SPAN | High Utility Episodes |
| US-SPAN | High Utility Episodes |
| TUP | Top-K High Utility Episodes |


## Bibliography
```
Fournier-Viger, P., Lin, C.W., Gomariz, A., Gueniche, T., Soltani, A., Deng, Z., Lam, H. T. (2016).
The SPMF Open-Source Data Mining Library Version 2.
Proc. 19th European Conference on Principles of Data Mining and Knowledge Discovery (PKDD 2016) Part III, Springer LNCS 9853,  pp. 36-40.
```
