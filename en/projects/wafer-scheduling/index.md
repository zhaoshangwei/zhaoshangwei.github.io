---
layout: project
lang: en
permalink: /en/projects/wafer-scheduling/
alternate: /projects/wafer-scheduling/
title: "Wafer Scheduling & Digital Twins"
category: "Engineering / Scheduling"
project_status: "Research theme"
summary: "Modeling equipment resources and wafer flow with discrete-event simulation to explore bottlenecks, throughput and feasible scheduling."
description: "Modeling equipment resources and wafer flow with discrete-event simulation to explore bottlenecks, throughput and feasible scheduling."
hero_image: /img/portfolio/scheduling.svg
hero_alt: "Abstract concept illustration"
keywords: ["Discrete-event Simulation", "Scheduling", "Digital Twin"]
---
## The problem

Cluster tools combine process chambers, transfer robots and load modules. Wafer movement is subject to route constraints, shared resources, module capacities and residence-time limits. Faster local actions do not always produce greater system throughput.

## Approach

A discrete-event model captures resource states and wafer movement. Process sequences, parallel actions, timing and safety constraints are represented explicitly. After validation, the model supports bottleneck reasoning and comparison of scheduling policies.

## Questions worth exploring

- How can timing, transfer conflicts and residence constraints be enforced together?
- Which shared resource truly limits throughput?
- How might heuristic search, mathematical optimization or reinforcement learning improve feasible schedules?

## Public scope

Only the general methodology is described here. An interactive Gantt demonstration may be added using synthetic data. No customer recipes or equipment-specific confidential settings are shared.
