---
layout:     post
title:      Python for finance 学习记录（1）
subtitle:   学习Numpy/Scipy等Python的科学计算模块
date:       2024-04-08
author:     Charles
header-img: img/post-bg-ios10.jpg
catalog: true
tags:
    - Python for finance
    - Python
---

# Python for finance 学习记录（1）


## NumPy
NumPy, which stands for Numerical Python, is one of the fundamental  libraries for numerical computing in Python. It provides support for  large, multi-dimensional arrays and matrices, along with a collection of mathematical functions to operate on these arrays efficiently. NumPy forms the foundation for many other libraries in the Python scientific ecosystem.

**An array in NumPy is like a matrix in MATLAB.** 

#### Help 查看modules的用法

After issuing `dir(np)`, the `std()` function appears, among others. To seek more information about
this function, `help(np.std)` is used. 

```python
>import numpy as np
>help(np.std)
Help on function std in module numpy.core.fromnumeric:
std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False)
Compute the standard deviation along the specified axis.
```

## SciPy

SciPy is a powerful open-source Python library used for scientific and  technical computing. It builds upon the NumPy library and provides  additional functionality for optimization, integration, interpolation,  linear algebra, signal processing, statistics, and much more. SciPy is  widely used in various scientific fields, including physics,  engineering, biology, finance, and machine learning.

```python
>import scipy as sp
>cashflows=[-100,50,40,20,10,50]
>x=sp.npv(0.1,cashflows)
>round(x,2)
31.41
```

