import argparse
import hashlib
import logging
import pathlib

import matplotlib.pyplot
import networkx
import yaml

import z3

import lipstick
import lipstick.graph
import lipstick.logging
import lipstick.schema
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

    parser.add_argument(
        "-g",
        "--graph",
        help="display model graph",
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

    if args.graph:
        log.info("Attempting to visualise graph...")
        networkx.draw_networkx(graph)
        matplotlib.pyplot.show()

    log.info("Attempting to solve model...")

    sol = lipstick.solve.optimize_task_graph(graph)

    if sol:
        log.info("Problem is [bold green]satisfiable[/]!")
        (f, m) = sol

        if isinstance(f, z3.IntNumRef):
            throughput = float(f.as_long())
        elif isinstance(f, z3.RatNumRef):
            throughput = float(f.as_fraction())
        else:
            raise ValueError("Unknown Z3 type %s!" % str(type(t)))

        log.info(
            "Maximum achievable throughput is [bold yellow]%.2f Hz[/]",
            throughput,
        )
        # log.info("Model specification: %s", str(m))

        # print(m)

        # for i in m:
        # print(i, float(m[i].as_fraction()))
    else:
        log.error("Problem is [bold red]not satisfiable[/]!")
