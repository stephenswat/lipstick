import z3
import networkx
import argparse
import yaml
import pathlib
import logging

import matplotlib.pyplot

import lipstick
import lipstick.graph
import lipstick.schema
import lipstick.logging
import lipstick.solve


log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "model",
        type=pathlib.Path,
        help="task graph YAML file to load",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="enable verbose output",
        action="store_true",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if (args.verbose or False) else logging.INFO,
        format="%(message)s",
        handlers=[lipstick.logging.LogHandler()],
    )

    log.info(
        "Welcome to [bold]Lipstick[/] version [bold yellow]%s[/]", lipstick.__version__
    )

    with open(args.model, "r") as f:
        model = lipstick.schema.TaskGraph(**yaml.safe_load(f))

    graph = lipstick.graph.reify(model)

    print(graph)

    # networkx.draw_networkx(graph)
    # matplotlib.pyplot.show()

    sol = lipstick.solve.optimize_task_graph(graph)

    print(type(sol))
    print(sol)
