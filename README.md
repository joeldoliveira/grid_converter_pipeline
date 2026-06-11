# Grid Converter and Validation Pipeline

A framework for modelling, converting, and analysing power systems with increasing penetration of converter-based renewable generation.

## Overview

The transition towards renewable energy sources is leading to a progressive replacement of conventional synchronous generation by converter-interfaced resources. This transformation introduces new challenges for power system planning, operation, and analysis, requiring appropriate models and tools to assess the impact of converter-based technologies on network behaviour.

This repository was developed as part of an internship at **INESC TEC** and aims to provide a structured environment for the study of converter-dominated power systems. The project combines network modelling, data extraction, automated conversion processes, and external analysis tools to facilitate the evaluation of different power system configurations.

The repository contains benchmark transmission network models developed in **DIgSILENT PowerFactory**, together with scripts and tools that support the conversion and analysis workflow.

## Software Requirements

The network models included in this repository were developed using **DIgSILENT PowerFactory**.

Before using the models, PowerFactory must be installed. The software can be obtained from the official website:

https://www.digsilent.de/en/

Depending on the version used, a valid license may be required.

## Repository Structure

```text
grid_converter_pipeline/
│
├── powerfactory/    PowerFactory network models
├── python/          Automation and conversion scripts
├── matlab/          MATLAB and MATPOWER analysis tools
├── docs/            Documentation and figures
└── README.md
```

## Available Models

The repository currently includes several benchmark transmission systems frequently used in power system studies:

- IEEE 39-Bus (Classical configuration)
- IEEE 39-Bus (Fully converted configuration)
- IEEE 118-Bus
- IEEE 240-Bus
- IEEE 300-Bus

These models provide different levels of complexity and converter penetration, enabling comparative studies between conventional and converter-dominated systems.

## Methodology

The workflow adopted in this project is based on the integration of multiple software environments.

### 1. Power System Modelling

The first stage consists of developing and adapting transmission network models in DIgSILENT PowerFactory.

This includes:

- Network validation.
- Generator modelling.
- Converter-based generation integration.
- Parameter adjustment.
- Power flow verification.

Different levels of converter penetration can be implemented by replacing conventional synchronous generators with renewable converter-based generation while maintaining system operability.

### 2. Data Extraction and Conversion

Once the network model is validated in PowerFactory, Python scripts are used to automatically extract the relevant electrical data.

The extraction process includes:

- Bus information.
- Generator parameters.
- Transmission line data.
- Transformer parameters.
- Network topology information.

The extracted data is then processed and converted into structures compatible with MATLAB and MATPOWER.

This automation significantly reduces manual work and ensures consistency between the original PowerFactory model and the exported network representation.

### 3. MATLAB / MATPOWER Representation

After conversion, the network is reconstructed in MATLAB using the MATPOWER case format.

The conversion process generates the main matrices required by MATPOWER:

- **Bus matrix (`bus`)**
- **Generator matrix (`gen`)**
- **Branch matrix (`branch`)**

These matrices contain all the electrical information necessary to reproduce the network behaviour outside the PowerFactory environment.

Once imported into MATLAB, standard power flow studies can be executed using MATPOWER functions, allowing rapid analysis of different operating conditions and network configurations.

### 4. Validation and Comparison

A key objective of the project is to ensure that the converted MATLAB model accurately represents the original PowerFactory network.

To achieve this, the results obtained from both environments are compared.

The validation process includes:

- Bus voltage magnitudes.
- Voltage angles.
- Active power injections.
- Reactive power injections.
- Line power flows.
- System losses.

By comparing the results obtained in PowerFactory and MATLAB, it is possible to verify the correctness of the conversion process and identify any discrepancies between the two representations.

The Python pipeline therefore acts as a bridge between both software environments, ensuring that network data is transferred accurately and consistently.

## Project Objectives

- Study the impact of converter-based generation on transmission systems.
- Develop benchmark networks with different converter penetration levels.
- Automate network data extraction from PowerFactory.
- Generate MATLAB/MATPOWER-compatible network models.
- Validate converted networks through result comparison.
- Improve reproducibility and efficiency in power system studies.
- Provide a foundation for future research involving converter-dominated power systems.

## Workflow

```text
DIgSILENT PowerFactory
            │
            ▼
     Network Modelling
            │
            ▼
      Python Pipeline
            │
            ▼
     Data Extraction
            │
            ▼
     MATPOWER Conversion
            │
            ▼
   MATLAB/MATPOWER Model
            │
            ▼
      Power Flow Studies
            │
            ▼
  Comparison & Validation
            │
            ▼
      Performance Analysis
```

## Author

**Joel Domingues Oliveira**  
**Institution:** INESC TEC  
**Date:** June 2026
