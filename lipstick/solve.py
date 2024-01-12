import z3
import networkx
import collections


def optimize_task_graph(tg: networkx.Graph):
    opt = z3.Optimize()

    resource_variables = {}

    for s, d, i in tg.edges(data=True):
        if "resource" in i:
            v = z3.Real("%s:%s:%s" % (str(s), str(d), str(i["resource"])))
            resource_variables[(s, d, i["resource"])] = v
            opt.add(v >= 0.0)

    for r in set(
        j
        for j in [i[2].get("resource", None) for i in tg.edges(data=True)]
        if j is not None
    ):
        v = sum(i for ((_, _, s), i) in resource_variables.items() if s == r)
        opt.add(v >= 0.0)
        opt.add(v <= 1.0)

    flow_variables = {}

    for s, d, i in tg.edges(data=True):
        if "resource" in i:
            flow_variables[(s, d)] = (
                resource_variables[(s, d, i["resource"])] * i["ratio"]
            )
        else:
            flow_variables[(s, d)] = z3.Real("%s->%s" % (str(s), str(d)))

    flow_variablies_in = collections.defaultdict(list)
    flow_variablies_out = collections.defaultdict(list)

    for s, d in tg.edges():
        flow_variablies_in[d].append(flow_variables[(s, d)])
        flow_variablies_out[s].append(flow_variables[(s, d)])

    for n in set(flow_variablies_in.keys()).union(set(flow_variablies_out.keys())):
        if n != "sink" and n != "source":
            opt.add(sum(flow_variablies_in[n]) == sum(flow_variablies_out[n]))

    flow = sum(flow_variablies_in["sink"])

    h = opt.maximize(flow)

    if opt.check() == z3.sat:
        return (opt.upper(h), opt.model())
    else:
        return None
