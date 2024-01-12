import z3
import networkx
import argparse
import yaml
import pathlib
import logging
import hashlib

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

    log.info("Reading task graph from [bold magenta]%s[/]...", args.model)

    log.info(
        "Task graph MD5 sum is [bold green]%s[/]",
        hashlib.md5(open(args.model, "rb").read()).hexdigest(),
    )

    with open(args.model, "r") as f:
        model = lipstick.schema.TaskGraph(**yaml.safe_load(f))

    log.info("Reifying task graph from model...")

    graph = lipstick.graph.reify(model)

    log.info(
        "Created model with [bold yellow]%d[/] nodes and [bold yellow]%d[/] edges",
        len(graph.nodes()),
        len(graph.edges()),
    )

    networkx.draw_networkx(graph)
    matplotlib.pyplot.show()

    log.info("Attempting to solve model...")

    sol = lipstick.solve.optimize_task_graph(graph)

    if sol:
        log.info("Problem is satisfiable!")
        (f, m) = sol

        log.info(
            "Maximum achievable throughput is [bold yellow]%.2f Hz[/]",
            float(f.as_fraction()),
        )
        # log.info("Model specification: %s", str(m))

        print(m)

        for i in m:
            print(i, float(m[i].as_fraction()))
    else:
        log.error("Problem is not satisfiable!")
