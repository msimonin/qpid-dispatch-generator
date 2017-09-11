def get_conf(graph, machines, distribution):
    ntm, mtn = distribution(graph, machines)
    confs = {}
    router_idx = 0
    for node, nbrdict in graph.adjacency_iter():
        confs.setdefault(node, {})
        machine = ntm[node]
        idx = mtn[machine].index(node)
        router_id = "router%s" % router_idx
        confs[node].update({
            'machine': machine,
            'router_id': router_id})
        confs[node].update({
                'listeners': [{'host': machine,
                                'port': 6000 + idx,
                                'role': 'inter-router'},
                              {
                                'host': machine,
                                'port': 5000 + idx,
                                'role': 'normal',
                                # use an extra field for the remaining options
                                'authenticatePeer': 'no',
                                'saslMechanisms': 'ANONYMOUS'}]})
        # outgoing links
        connectors = []
        for out in nbrdict.keys():
            out_machine = ntm[out]
            out_idx = mtn[out_machine].index(out)
            connectors.append({
                'host': out_machine,
                'port': 6000 + out_idx, # same rule as above
                'role': 'inter-router'
            })
        confs[node].update({'connectors': connectors})
        router_idx = router_idx + 1

    return confs
