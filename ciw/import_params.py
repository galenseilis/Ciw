import copy
import types
import ciw.dists
from .network import *


def create_network(
    arrival_distributions=None,
    baulking_functions=None,
    class_change_matrices=None,
    class_change_time_distributions=None,
    number_of_servers=None,
    priority_classes=None,
    queue_capacities=None,
    service_distributions=None,
    routing=None,
    batching_distributions=None,
    ps_thresholds=None,
    server_priority_functions=None,
    reneging_time_distributions=None,
    reneging_destinations=None,
    service_disciplines=None,
):
    """
    Takes in kwargs, creates dictionary.
    """
    if (
        arrival_distributions == None
        or number_of_servers == None
        or service_distributions == None
    ):
        raise ValueError(
            "arrival_distributions, service_distributions and number_of_servers are required arguments."
        )

    params = {
        "arrival_distributions": arrival_distributions,
        "number_of_servers": number_of_servers,
        "service_distributions": service_distributions,
    }

    if baulking_functions != None:
        params["baulking_functions"] = baulking_functions
    if class_change_matrices != None:
        params["class_change_matrices"] = class_change_matrices
    if class_change_time_distributions is not None:
        params["class_change_time_distributions"] = class_change_time_distributions
    if priority_classes != None:
        params["priority_classes"] = priority_classes
    if queue_capacities != None:
        params["queue_capacities"] = queue_capacities
    if routing != None:
        params["routing"] = routing
    if batching_distributions != None:
        params["batching_distributions"] = batching_distributions
    if ps_thresholds != None:
        params["ps_thresholds"] = ps_thresholds
    if server_priority_functions != None:
        params["server_priority_functions"] = server_priority_functions
    if reneging_time_distributions is not None:
        params["reneging_time_distributions"] = reneging_time_distributions
    if reneging_destinations is not None:
        params["reneging_destinations"] = reneging_destinations
    if service_disciplines is not None:
        params["service_disciplines"] = service_disciplines

    return create_network_from_dictionary(params)


def create_network_from_dictionary(params_input):
    """
    Creates a Network object from a parameters dictionary.
    """
    params = fill_out_dictionary(params_input)
    validify_dictionary(params)
    # Then make the Network object
    number_of_classes = params["number_of_classes"]
    number_of_nodes = params["number_of_nodes"]
    arrivals = [
        params["arrival_distributions"]["Class " + str(clss)]
        for clss in range(len(params["arrival_distributions"]))
    ]
    services = [
        params["service_distributions"]["Class " + str(clss)]
        for clss in range(len(params["service_distributions"]))
    ]
    if all(isinstance(f, types.FunctionType) for f in params["routing"]):
        routing = params["routing"]
    else:
        routing = [
            params["routing"]["Class " + str(clss)]
            for clss in range(len(params["routing"]))
        ]
    if isinstance(params["priority_classes"], dict):
        priorities = [
            params["priority_classes"]["Class " + str(clss)]
            for clss in range(len(params["priority_classes"]))
        ]
        preempt_priorities = [False for _ in range(number_of_nodes)]
    if isinstance(params["priority_classes"], tuple):
        priorities = [
            params["priority_classes"][0]["Class " + str(clss)]
            for clss in range(len(params["priority_classes"][0]))
        ]
        preempt_priorities = params["priority_classes"][1]
    baulking_functions = [
        params["baulking_functions"]["Class " + str(clss)]
        for clss in range(len(params["baulking_functions"]))
    ]
    batches = [
        params["batching_distributions"]["Class " + str(clss)]
        for clss in range(len(params["batching_distributions"]))
    ]
    queueing_capacities = [
        float(i) if i == "Inf" else i for i in params["queue_capacities"]
    ]
    class_change_matrices = params.get(
        "class_change_matrices",
        {"Node " + str(nd + 1): None for nd in range(number_of_nodes)},
    )
    class_change_time_distributions = params.get(
        "class_change_time_distributions",
        [
            [None for clss1 in range(number_of_classes)]
            for clss2 in range(number_of_classes)
        ],
    )
    number_of_servers, schedules, nodes, classes, preempts = [], [], [], [], []
    for c in params["number_of_servers"]:
        if isinstance(c, (tuple, list)):
            if isinstance(c, tuple):
                s = c[0]
                p = c[1]
            if isinstance(c, list):
                s = c
                p = False
            number_of_servers.append("schedule")
            schedules.append(s)
            preempts.append(p)
        else:
            number_of_servers.append(c)
            schedules.append(None)
            preempts.append(False)
    for nd in range(number_of_nodes):
        nodes.append(
            ServiceCentre(
                number_of_servers[nd],
                queueing_capacities[nd],
                class_change_matrices["Node " + str(nd + 1)],
                schedules[nd],
                preempts[nd],
                preempt_priorities[nd],
                params["ps_thresholds"][nd],
                params["server_priority_functions"][nd],
                params["service_disciplines"][nd],
            )
        )
    for clss in range(number_of_classes):
        if all(isinstance(f, types.FunctionType) for f in params["routing"]):
            classes.append(
                CustomerClass(
                    arrivals[clss],
                    services[clss],
                    routing,
                    priorities[clss],
                    baulking_functions[clss],
                    batches[clss],
                    params["reneging_time_distributions"]["Class " + str(clss)],
                    params["reneging_destinations"]["Class " + str(clss)],
                    class_change_time_distributions[clss],
                )
            )
        else:
            classes.append(
                CustomerClass(
                    arrivals[clss],
                    services[clss],
                    routing[clss],
                    priorities[clss],
                    baulking_functions[clss],
                    batches[clss],
                    params["reneging_time_distributions"]["Class " + str(clss)],
                    params["reneging_destinations"]["Class " + str(clss)],
                    class_change_time_distributions[clss],
                )
            )

    n = Network(nodes, classes)
    if all(isinstance(f, types.FunctionType) for f in params["routing"]):
        n.process_based = True
    else:
        n.process_based = False
    return n


def fill_out_dictionary(params_input):
    """
    Fills out the parameters dictionary with the
    default values of the optional arguments.
    """
    params = copy.deepcopy(params_input)
    if isinstance(params["arrival_distributions"], list):
        arr_dists = params["arrival_distributions"]
        params["arrival_distributions"] = {"Class 0": arr_dists}
    if isinstance(params["service_distributions"], list):
        srv_dists = params["service_distributions"]
        params["service_distributions"] = {"Class 0": srv_dists}
    if "routing" in params:
        if all(isinstance(f, list) for f in params["routing"]):
            rtng_mat = params["routing"]
            params["routing"] = {"Class 0": rtng_mat}
    if "baulking_functions" in params:
        if isinstance(params["baulking_functions"], list):
            blk_fncs = params["baulking_functions"]
            params["baulking_functions"] = {"Class 0": blk_fncs}
    if "batching_distributions" in params:
        if isinstance(params["batching_distributions"], list):
            btch_dists = params["batching_distributions"]
            params["batching_distributions"] = {"Class 0": btch_dists}
    if "reneging_time_distributions" in params:
        if isinstance(params["reneging_time_distributions"], list):
            reneging_dists = params["reneging_time_distributions"]
            params["reneging_time_distributions"] = {"Class 0": reneging_dists}
    if "reneging_destinations" in params:
        if isinstance(params["reneging_destinations"], list):
            reneging_dests = params["reneging_destinations"]
            params["reneging_destinations"] = {"Class 0": reneging_dests}

    default_dict = {
        "name": "Simulation",
        "routing": {
            "Class " + str(i): [[0.0]]
            for i in range(len(params["arrival_distributions"]))
        },
        "number_of_nodes": len(params["number_of_servers"]),
        "number_of_classes": len(params["arrival_distributions"]),
        "queue_capacities": [
            float("inf") for _ in range(len(params["number_of_servers"]))
        ],
        "priority_classes": {
            "Class " + str(i): 0 for i in range(len(params["arrival_distributions"]))
        },
        "baulking_functions": {
            "Class " + str(i): [None for _ in range(len(params["number_of_servers"]))]
            for i in range(len(params["arrival_distributions"]))
        },
        "batching_distributions": {
            "Class "
            + str(i): [
                ciw.dists.Deterministic(1)
                for _ in range(len(params["number_of_servers"]))
            ]
            for i in range(len(params["arrival_distributions"]))
        },
        "ps_thresholds": [1 for _ in range(len(params["number_of_servers"]))],
        "server_priority_functions": [
            None for _ in range(len(params["number_of_servers"]))
        ],
        "reneging_time_distributions": {
            "Class " + str(i): [None for _ in range(len(params["number_of_servers"]))]
            for i in range(len(params["arrival_distributions"]))
        },
        "reneging_destinations": {
            "Class " + str(i): [-1 for _ in range(len(params["number_of_servers"]))]
            for i in range(len(params["arrival_distributions"]))
        },
        "service_disciplines": [
            ciw.disciplines.FIFO for _ in range(len(params["number_of_servers"]))
        ],
    }

    for a in default_dict:
        params[a] = params.get(a, default_dict[a])
    return params


def validify_dictionary(params):
    """
    Raises errors if there is something wrong with the
    parameters dictionary.
    """
    if all(isinstance(f, types.FunctionType) for f in params["routing"]):
        consistant_num_classes = (
            params["number_of_classes"]
            == len(params["arrival_distributions"])
            == len(params["service_distributions"])
            == len(params["batching_distributions"])
            == len(params["reneging_time_distributions"])
            == len(params["reneging_destinations"])
        )
    else:
        consistant_num_classes = (
            params["number_of_classes"]
            == len(params["arrival_distributions"])
            == len(params["service_distributions"])
            == len(params["routing"])
            == len(params["batching_distributions"])
            == len(params["reneging_time_distributions"])
            == len(params["reneging_destinations"])
        )
    if not consistant_num_classes:
        raise ValueError("Ensure consistant number of classes is used throughout.")
    if all(isinstance(f, types.FunctionType) for f in params["routing"]):
        consistant_class_names = (
            set(params["arrival_distributions"])
            == set(params["service_distributions"])
            == set(params["batching_distributions"])
            == set(params["reneging_time_distributions"])
            == set(params["reneging_destinations"])
            == set(["Class " + str(i) for i in range(params["number_of_classes"])])
        )
    else:
        consistant_class_names = (
            set(params["arrival_distributions"])
            == set(params["service_distributions"])
            == set(params["routing"])
            == set(params["batching_distributions"])
            == set(params["reneging_time_distributions"])
            == set(params["reneging_destinations"])
            == set(["Class " + str(i) for i in range(params["number_of_classes"])])
        )
    if not consistant_class_names:
        raise ValueError("Ensure correct names for customer classes.")
    if all(isinstance(f, types.FunctionType) for f in params["routing"]):
        num_nodes_count = (
            [params["number_of_nodes"]]
            + [len(obs) for obs in params["arrival_distributions"].values()]
            + [len(obs) for obs in params["service_distributions"].values()]
            + [len(obs) for obs in params["batching_distributions"].values()]
            + [len(obs) for obs in params["reneging_time_distributions"].values()]
            + [len(obs) for obs in params["reneging_destinations"].values()]
            + [len(params["routing"])]
            + [len(params["number_of_servers"])]
            + [len(params["server_priority_functions"])]
            + [len(params["queue_capacities"])]
        )
    else:
        num_nodes_count = (
            [params["number_of_nodes"]]
            + [len(obs) for obs in params["arrival_distributions"].values()]
            + [len(obs) for obs in params["service_distributions"].values()]
            + [len(obs) for obs in params["routing"].values()]
            + [len(obs) for obs in params["batching_distributions"].values()]
            + [len(obs) for obs in params["reneging_time_distributions"].values()]
            + [len(obs) for obs in params["reneging_destinations"].values()]
            + [len(row) for row in [obs for obs in params["routing"].values()][0]]
            + [len(params["number_of_servers"])]
            + [len(params["server_priority_functions"])]
            + [len(params["queue_capacities"])]
            + [len(params["service_disciplines"])]
        )
    if len(set(num_nodes_count)) != 1:
        raise ValueError("Ensure consistant number of nodes is used throughout.")
    if not all(isinstance(f, types.FunctionType) for f in params["routing"]):
        for clss in params["routing"].values():
            for row in clss:
                if sum(row) > 1.0 or min(row) < 0.0 or max(row) > 1.0:
                    raise ValueError("Ensure that routing matrix is valid.")
    neg_numservers = any(
        [(isinstance(obs, int) and obs < 0) for obs in params["number_of_servers"]]
    )
    valid_capacities = all(
        [
            ((isinstance(obs, int) and obs >= 0) or obs == float("inf") or obs == "Inf")
            for obs in params["queue_capacities"]
        ]
    )
    if neg_numservers:
        raise ValueError("Number of servers must be positive integers.")
    if not valid_capacities:
        raise ValueError("Queue capacities must be positive integers or zero.")
    if "class_change_matrices" in params:
        num_nodes = len(params["class_change_matrices"]) == params["number_of_nodes"]
        node_names = set(params["class_change_matrices"]) == set(
            ["Node " + str(i + 1) for i in range(params["number_of_nodes"])]
        )
        if not (num_nodes and node_names):
            raise ValueError("Ensure correct nodes used in class_change_matrices.")
        for nd in params["class_change_matrices"].values():
            for row in nd:
                if sum(row) > 1.0 or min(row) < 0.0 or max(row) > 1.0:
                    raise ValueError("Ensure that class change matrix is valid.")
    if "class_change_time_distributions" in params:
        wrong_num_classes = any(
            len(row) != params["number_of_classes"]
            for row in params["class_change_time_distributions"]
        ) or (
            len(params["class_change_time_distributions"])
            != params["number_of_classes"]
        )
        if wrong_num_classes:
            raise ValueError(
                "Ensure correct number of customer classes used in class_change_time_distributions."
            )
    for n in params["number_of_servers"]:
        if isinstance(n, str) and n != "Inf":
            if n not in params:
                raise ValueError("No schedule " + str(n) + " defined.")
    possible_destinations = list(range(1, params["number_of_nodes"] + 1)) + [-1]
    for dests in params["reneging_destinations"]:
        correct_destinations = all(
            d in possible_destinations for d in params["reneging_destinations"][dests]
        )
        if not correct_destinations:
            raise ValueError("Ensure all reneging destinations are possible.")
