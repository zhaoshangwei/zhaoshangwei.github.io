---
title: Matlab实现多层神经网络的算例汇总
date: '2020/10/21 20:46:25'
tags: MATLAB 神经网络
mathjax: true
abbrlink: 20fa35b4
---

使用MATLAB实现多层神经网络的算例，包括扭摆系统、仿射非线性算例以及“质量-弹簧-阻尼”系统。

<!-- more -->

# Matlab实现多层神经网络的算例汇总

1. 扭摆系统 (torsional pendulum system)

   文献出处：
   
   【1】Liu D , Wei Q . Policy Iteration Adaptive Dynamic Programming Algorithm for Discrete-Time Nonlinear Systems[J]. IEEE Trans Neural Netw Learn Syst, 2014, 25(3):621-634.
   
   【2】Mu C , Wang D , He H . Novel iterative neural dynamic programming for data-based approximate optimal control design[J]. Automatica, 2017, 81:240-252.

Dynamic:
$$
\begin{equation}
\begin{split}
   &\frac{d \theta}{d t}=\omega \\
   &J \frac{d \omega}{d t}=u-M g l \sin \theta-f_{d} \frac{d \theta}{d t}
   \end{split}
   \end{equation}
$$
   where $M=1 / 3 \mathrm{kg}$ and $l=2 / 3 \mathrm{m}$ are the mass and length of the pendulum bar, respectively. The system states are the current angle $\theta$ and the angular velocity $\omega .$ Let $J=4 / 3 M l^{2}$ and $f_{d}=0.2$ be the rotary inertia and frictional factor, respectively. Let $g=9.8 \mathrm{m} / \mathrm{s}^{2}$ be the gravity. Discretization of the system function and performance index function using Euler and trapezoidal methods with the sampling interval $\Delta t=0.1 \mathrm{s}$ leads to
$$
\begin{equation}
   {\left[\begin{array}{c}
   x_{1(k+1)} \\
   x_{2(k+1)}
   \end{array}\right]=\left[\begin{array}{c}
   0.1 x_{2 k}+x_{1 k} \\
   -0.49 \times \sin \left(x_{1 k}\right)-0.1 \times f_{d} \times x_{2 k}+x_{2 k}
   \end{array}\right]} 
   +\left[\begin{array}{c}
   0 \\
   0.1
   \end{array}\right] u_{k}
   \end{equation}
$$
   或者
$$
\begin{equation}
x_{t+1}=\left[\begin{array}{c}
   x_{1 t}+0.1 x_{2 t} \\
   0.2\left(-0.49 \sin \left(x_{1 t}\right)-0.2 x_{2 t}+x_{2 t}\right)
   \end{array}\right]+\left[\begin{array}{c}
   0 \\
   0.02
   \end{array}\right] u_{t}
\end{equation}
$$
   The initial state is $x_{0}=[1,-1]^{T}$



仿真结果：`ResultsCollation1.m`


2. 非线性算例

   文献出处：

   【1】Wang F Y , Jin N , Liu D , et al. Adaptive dynamic programming for finite-horizon optimal control of discrete-time nonlinear systems with ε-error bound.[J]. IEEE Trans Neural Netw, 2011, 22(1):24-36.

   【2】Zhang H , Wei Q , Luo Y . A Novel Infinite-Time Optimal Tracking Control Scheme for a Class of Discrete-Time Nonlinear Systems via the Greedy HDP Iteration Algorithm[J]. IEEE Transactions on Systems Man & Cybernetics Part B, 2008, 38(4):937-942.

   【3】Liu D , Wei Q . Policy Iteration Adaptive Dynamic Programming Algorithm for Discrete-Time Nonlinear Systems[J]. IEEE Trans Neural Netw Learn Syst, 2014, 25(3):621-634.

   We consider the following nonlinear system:
   $$
   \begin{align*}
   x_{k+1}=f\left(x_{k}\right)+g\left(x_{k}\right) u_{k}
   \end{align*}
   $$
   variables, respectively. The system functions are given as
   $$
   \begin{align*}
   f\left(x_{k}\right)=\left[\begin{array}{c}
   0.2 x_{1 k} \exp \left(x_{2 k}^{2}\right) \\
   0.3 x_{2 k}^{3}
   \end{array}\right], \quad g\left(x_{k}\right)=\left[\begin{array}{c}
   0 \\
   -0.2
   \end{array}\right]
   \end{align*}
   $$
   The initial state is $ x_{0}=[2,-1]^{T}$

   仿真结果：`ResultsCollation2.m`

3. “质量-弹簧-阻尼”系统（Mass-Spring-Damper System）

   文献出处：

   Winston Alexander Baker. Observer incorporated neoclassical controller design: A discrete perspective[J]. Dissertations & Theses - Gradworks, 2010.
   $$
   \left[\begin{array}{l}
   x_{1}(k+1) \\
   x_{2}(k+1)
   \end{array}\right]=\left[\begin{array}{c}
   0.0099 x_{2 k}+0.9996 x_{1 k} \\
   -0.0887 x_{1 k}+0.97 x_{2 k}
   \end{array}\right]+\left[\begin{array}{c}
   0 \\
   0.0099
   \end{array}\right] u(k)
   $$
    The initial state vector is set as $x_{0}=[-1,1]^{T}$.

   仿真结果：`ResultsCollation3.m`

