import networkx

import lipstick.schema


def reify(tg: lipstick.schema.TaskGraph) -> networkx.DiGraph:
    g = networkx.DiGraph()

    g.add_node("source")
    g.add_node("sink")

    for t, tv in tg.datatypes.items():
        for d in tg.devices:
            g.add_node((t, d))

            if t == tg.sink:
                g.add_edge((t, d), "sink", **{"goal": True})

            if t == tg.source:
                g.add_edge("source", (t, d))

        for i in tg.interconnects:
            res = "i:%s->%s" % (i.source, i.destination)

            g.add_edge(
                (t, i.source),
                (t, i.destination),
                **{"resource": res, "ratio": i.bandwidth / (tv.size * tv.count)}
            )

            if i.bidirectional:
                g.add_edge(
                    (t, i.destination),
                    (t, i.source),
                    **{"resource": res, "ratio": i.bandwidth / (tv.size * tv.count)}
                )

    for a in tg.algorithms.values():
        for i in a.implementations:
            g.add_edge(
                (a.in_type, i.device),
                (a.out_type, i.device),
                **{"resource": "d:%s" % i.device, "ratio": i.throughput}
            )

    return g
