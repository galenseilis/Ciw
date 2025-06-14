import tqdm
import copy
from decimal import getcontext
from .auxiliary import *
from .node import Node
from .exactnode import ExactNode, ExactArrivalNode
from .arrival_node import ArrivalNode
from .exit_node import ExitNode
from .individual import Individual
from .server import Server
from .data_record import DataRecord
from ciw import trackers
from ciw import deadlock


class Simulation(object):
    """
    The Simulation class, that is the engine of the simulation.
    """

    def __init__(
        self,
        network,
        exact=False,
        name="Simulation",
        tracker=None,
        deadlock_detector=None,
        node_class=None,
        arrival_node_class=None,
        exit_node_class=None,
        individual_class=None,
        server_class=None,
    ):
        """
        Initialise an instance of the simualation.
        """
        self.current_time = 0.0
        self.network = network
        self.set_classes(node_class, arrival_node_class, exit_node_class, individual_class, server_class)
        if exact:
            self.NodeTypes = [ExactNode for _ in range(network.number_of_nodes)]
            self.ArrivalNodeType = ExactArrivalNode
            getcontext().prec = exact

        self.name = name
        self.deadlock_detector = deadlock.NoDetection() if deadlock_detector is None else deadlock_detector
        self.inter_arrival_times = self.find_arrival_dists()
        self.service_times = self.find_service_dists()
        self.batch_sizes = self.find_batching_dists()
        self.show_simulation_to_distributions()
        self.number_of_priority_classes = self.network.number_of_priority_classes
        self.transitive_nodes = [node_type(i + 1, self) for i, node_type in enumerate(self.NodeTypes)]
        self.nodes = [self.ArrivalNodeType(self)] + self.transitive_nodes + [self.ExitNodeType()]
        self.active_nodes = self.nodes[:-1]
        self.routers = self.find_and_initialise_routers()
        self.nodes[0].initialise()
        if tracker is None:
            self.statetracker = trackers.StateTracker()
        else:
            self.statetracker = tracker
        self.statetracker.initialise(self)
        self.times_dictionary = {self.statetracker.hash_state(): 0.0}
        self.times_to_deadlock = {}
        self.unchecked_blockage = False

    def __repr__(self):
        """
        Representation of the simulation.
        """
        return self.name

    @property    
    def number_of_individuals(self):
        """
        The number of individuals currently in the system.
        """
        return (self.nodes[0].number_of_individuals - 1) - self.nodes[-1].number_of_individuals

    def find_arrival_dists(self):
        """
        Create the dictionary of arrival time distribution
        objects for each node for each customer class.
        """
        return {
            node + 1: {
                clss: copy.deepcopy(self.network.customer_classes[clss].arrival_distributions[node])
                for clss in self.network.customer_class_names
            } for node in range(self.network.number_of_nodes)
        }

    def find_service_dists(self):
        """
        Create the dictionary of service time distribution
        objects for each node for each customer class.
        """
        return {
            node + 1: {
                clss: copy.deepcopy(self.network.customer_classes[clss].service_distributions[node])
                for clss in self.network.customer_class_names
            } for node in range(self.network.number_of_nodes)
        }

    def find_batching_dists(self):
        """
        Create the dictionary of batch size distribution
        objects for each node for each class.
        """
        return {
            node + 1: {
                clss: copy.deepcopy(self.network.customer_classes[clss].batching_distributions[node])
                for clss in self.network.customer_class_names
            } for node in range(self.network.number_of_nodes)
        }

    def show_simulation_to_distributions(self):
        """
        Adds the simulation object as an attribute of the distribution objects
        """
        for clss in self.network.customer_class_names:
            for nd in range(self.network.number_of_nodes):
                if self.inter_arrival_times[nd + 1][clss] is not None:
                    self.inter_arrival_times[nd + 1][clss].simulation = self
                    self.service_times[nd + 1][clss].simulation = self
                    self.batch_sizes[nd + 1][clss].simulation = self

    def find_and_initialise_routers(self):
        """
        Initialises the routing objects.
        """
        routers_dict = {}
        for clss in self.network.customer_class_names:
            routers_dict[clss] = self.network.customer_classes[clss].routing
            routers_dict[clss].initialise(self)
        return routers_dict

    def find_next_active_node(self):
        """
        Returns the next active node, the node whose next_event_date is next:
        """
        mindate = float("Inf")
        next_active_nodes = []
        for nd in self.active_nodes:
            if nd.next_event_date < mindate:
                mindate = nd.next_event_date
                next_active_nodes = [nd]
            elif nd.next_event_date == mindate:
                next_active_nodes.append(nd)
        if len(next_active_nodes) > 1:
            return random_choice(next_active_nodes)
        return next_active_nodes[0]

    def get_all_individuals(self):
        """
        Returns list of all individuals with at least one data record.
        """
        return [
            individual
            for node in self.nodes[1:]
            for individual in node.all_individuals
        ]

    def get_all_records(
        self, only=["service", "baulk", "rejection", "renege", "interrupted service"], include_incomplete=False
    ):
        """
        Gets all data records from all individuals.
        """
        records = []
        for individual in self.get_all_individuals():
            for record in individual.data_records:
                if record.record_type in only:
                    records.append(record)
            if include_incomplete:
                if individual.node != -1:
                    incomplete_record = self.nodes[individual.node].write_incomplete_record(individual)
                    records.append(incomplete_record)
        self.all_records = records
        return records

    def set_classes(
        self, node_class, arrival_node_class, exit_node_class, individual_class, server_class
    ):
        """
        Sets the type of ArrivalNode, Node, Exit Node, Individual,
        and Server classes being used in the Simulation model.
        """
        if arrival_node_class is not None:
            self.ArrivalNodeType = arrival_node_class
        else:
            self.ArrivalNodeType = ArrivalNode

        if exit_node_class is not None:
            self.ExitNodeType = exit_node_class
        else:
            self.ExitNodeType = ExitNode

        if node_class is not None:
            if not isinstance(node_class, list):
                self.NodeTypes = [node_class for _ in range(self.network.number_of_nodes)]
            else:
                if len(node_class) != self.network.number_of_nodes:
                    raise ValueError("Ensure consistant number of nodes is used throughout.")
                self.NodeTypes = node_class
        else:
            self.NodeTypes = [Node for _ in range(self.network.number_of_nodes)]

        if individual_class is not None:
            self.IndividualType = individual_class
        else:
            self.IndividualType = Individual

        if server_class is not None:
            self.ServerType = server_class
        else:
            self.ServerType = Server

    def event_and_return_nextnode(self, next_active_node):
        """
        Carries out the event of current next_active_node,
        and returns the next next_active_node
        """
        next_active_node.have_event()
        for node in self.transitive_nodes:
            node.update_next_event_date()
        return self.find_next_active_node()

    def simulate_until_deadlock(self):
        """
        Runs the simulation until deadlock is reached.
        """
        deadlocked = False
        next_active_node = self.find_next_active_node()
        self.current_time = next_active_node.next_event_date
        while not deadlocked:
            next_active_node = self.event_and_return_nextnode(next_active_node)
            current_state = self.statetracker.hash_state()
            if current_state not in self.times_dictionary:
                self.times_dictionary[current_state] = self.current_time
            if self.unchecked_blockage:
                deadlocked = self.deadlock_detector.detect_deadlock()
                self.unchecked_blockage = False
            if deadlocked:
                time_of_deadlock = self.current_time
            self.current_time = next_active_node.next_event_date

        self.wrap_up_servers(time_of_deadlock)
        self.times_to_deadlock = {
            state: time_of_deadlock - self.times_dictionary[state]
            for state in self.times_dictionary.keys()
        }

    def simulate_until_max_time(self, max_simulation_time, progress_bar=False):
        """
        Runs the simulation until max_simulation_time is reached.
        """
        next_active_node = self.find_next_active_node()
        self.current_time = next_active_node.next_event_date

        if progress_bar:
            self.progress_bar = tqdm.tqdm(total=max_simulation_time)

        while self.current_time < max_simulation_time:
            next_active_node = self.event_and_return_nextnode(next_active_node)
            self.statetracker.timestamp()

            if progress_bar:
                remaining_time = max_simulation_time - self.progress_bar.n
                time_increment = next_active_node.next_event_date - self.current_time
                self.progress_bar.update(min(time_increment, remaining_time))

            self.current_time = next_active_node.next_event_date
        self.current_time = max_simulation_time

        self.wrap_up_servers(max_simulation_time)
        if progress_bar:
            remaining_time = max(max_simulation_time - self.progress_bar.n, 0)
            self.progress_bar.update(remaining_time)
            self.progress_bar.close()

    def simulate_until_max_customers(
        self, max_customers, progress_bar=False, method="Complete"
    ):
        """
        Runs the simulation until max_customers is reached:

            - Method: Complete
                Simulates until max_customers has reached the Exit Node after
                completing their journey
            - Method: Finish
                Simulates until max_customers has reached the Exit Node whether
                they have completed their journey or not (included baulkers and
                renegers)
            - Method: Arrive
                Simulates until max_customers have spawned at the Arrival Node
            - Method: Accept
                Simulates until max_customers have been spawned and accepted
                (not rejected) at the Arrival Node
        """
        next_active_node = self.find_next_active_node()
        self.current_time = next_active_node.next_event_date

        if progress_bar:
            self.progress_bar = tqdm.tqdm(total=max_customers)

        if method == "Complete":
            check = lambda: self.nodes[-1].number_of_completed_individuals
        elif method == "Finish":
            check = lambda: self.nodes[-1].number_of_individuals
        elif method == "Arrive":
            check = lambda: self.nodes[0].number_of_individuals
        elif method == "Accept":
            check = lambda: self.nodes[0].number_accepted_individuals
        else:
            raise ValueError("Invalid 'method' for 'simulate_until_max_customers'.")

        while check() < max_customers:
            old_check = check()
            next_active_node = self.event_and_return_nextnode(next_active_node)
            self.statetracker.timestamp()

            if progress_bar:
                remaining_time = max_customers - self.progress_bar.n
                time_increment = check() - old_check
                self.progress_bar.update(min(time_increment, remaining_time))

            previous_time = self.current_time
            self.current_time = next_active_node.next_event_date
        self.current_time = previous_time

        self.wrap_up_servers(self.current_time)

        if progress_bar:
            remaining_time = max(max_customers - self.progress_bar.n, 0)
            self.progress_bar.update(remaining_time)
            self.progress_bar.close()

    def wrap_up_servers(self, current_time):
        """
        Updates the servers' total_time and busy_time as
        the end of the simulation run. Finds the overall
        server utilisation for each node.
        """
        for nd in self.transitive_nodes:
            nd.wrap_up_servers(current_time)
            nd.find_server_utilisation()
