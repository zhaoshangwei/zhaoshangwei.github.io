---
layout: project
lang: zh
permalink: /projects/wafer-scheduling/
alternate: /en/projects/wafer-scheduling/
title: "晶圆调度与设备数字孪生"
category: "Engineering / Scheduling"
project_status: "Research theme"
summary: "利用离散事件仿真描述设备资源与晶圆流转，研究节拍、产能瓶颈和约束下的调度决策。"
description: "利用离散事件仿真描述设备资源与晶圆流转，研究节拍、产能瓶颈和约束下的调度决策。"
hero_image: /img/portfolio/scheduling.svg
hero_alt: "Abstract concept illustration"
keywords: ["Discrete-event Simulation", "Scheduling", "Digital Twin"]
---
## 背景与问题

复杂集束设备通常包含多腔室、机械手和装载模块。晶圆转运不仅受工艺路径约束，还受到资源互锁、模块容量与驻留时间限制。局部看似更快的动作，并不一定带来系统层面的最大产能。

## 方法思路

以离散事件仿真描述资源状态与晶圆流转过程，把设备动作、加工流程、并行关系和安全约束转化为可执行的调度模型。在模型验证的基础上，分析瓶颈资源，并比较不同调度策略的产能表现。

## 可探索的问题

- 如何同时考虑加工时序、转运冲突与晶圆驻留约束？
- 如何识别真正影响产能的资源瓶颈，而不是只关注单个腔室工艺时间？
- 如何结合启发式搜索、数学优化或强化学习提出可行的调度方案？

## 公开展示说明

此页面仅介绍通用技术框架。后续计划使用公开或合成数据提供动态甘特图与资源占用可视化，不公开具体设备配置或客户配方。
