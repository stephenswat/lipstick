# Lipstick

_Lipstick_ is a tool for generating optimistic upper bounds for the throughput
of tasks graphs running on heterogeneous systems. It works by treating the task
graph as a flow problem, adding constraints about resource usage (in
particular, the usage of compute devices and interconnects). _Lipstick_ then
optimizes using a linear programming solver. Thus, _Lipstick_ achieves an
optimistic upper bound by treating data as a fluid, continuous resource rather
than as discrete objects, which makes scheduling difficult.

## Usage

First, make sure that _poetry_ is installed, and then use that to install
_Lipstick_'s dependencies:

```bash
poetry install
```

Then run _Lipstick_ on a model file:

```bash
poetry run lipstick models/traccc.yaml
```
