# Project Overview

**foundry-transforms-api-csv** is a Python library that provides a local testing and execution environment for Palantir Foundry data pipelines. It mocks the Foundry `transforms.api` by mapping Foundry dataset paths/RIDs to local CSV files, allowing developers to test and run PySpark `transform_df` pipelines cross-platform without needing Foundry infrastructure. 

It accomplishes this by overriding the `Input` and `Output` classes to read from and write to local CSV files using a local PySpark session, driven by a global `TRANSFORMS_CSV_MAP` dictionary.

## Building and Running

The project relies entirely on **pixi** for dependency management, environment isolation, and task running.

### Environment Setup
To install all necessary dependencies (including PySpark, pytest, and the base transforms library):
```bash
pixi install
```

### Testing
To run the test suite via pytest:
```bash
pixi run test
```
*(This task automatically sets the appropriate working directory and `PYTHONPATH` for testing).*

## Development Conventions

- **Global CSV Mapping**: When mocking inputs and outputs locally, you must import and populate the global `TRANSFORMS_CSV_MAP` dictionary with the mapping from the Foundry dataset path/RID to your local CSV file path.
- **Transforms**: Use `@transform_df` from `transforms.api` alongside `Input` and `Output` classes.
- **Testing Transforms**: When writing a pipeline, testing code can be co-located with official templates and run in parallel since the local mock is not run by Foundry infrastructure.
- **Warning**: As noted in the documentation, Palantir maintains an open-source fork of Spark. You may encounter inconsistencies if attempting to use both `transforms-api-csv` and Foundry's Spark simultaneously. This project is not officially supported software.
