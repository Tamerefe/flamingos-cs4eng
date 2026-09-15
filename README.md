# Factoryflow

OEE (Overall Equipment Effectiveness) reporting tool for production line A.

This project reads and cleans raw sensor data (CSV) from the production line, calculates Availability, Performance, and Quality metrics per machine, and produces the final OEE value.

## Requirements

* Python >= 3.12
* [uv](https://github.com/astral-sh/uv) (For environment and package management)

## Setup

After cloning the repository, you can run the project in an isolated environment using `uv` without affecting your system's global Python installation. Dependencies are managed automatically via `pyproject.toml` and `uv.lock`.

```powershell
# Clone the repository
git clone https://github.com/Tamerefe/flamingos-cs4eng
cd factoryflow-course/s1-4-clean-code/start

# Run the project with uv (installs required packages automatically)
uv run python -m factoryflow oee
