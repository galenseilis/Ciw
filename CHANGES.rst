History
-------

+ **3.2.6 (2025-06-13)**
    + Add the `include_incomplete` keyword tot he `get_all_records` method to allow for collection of incomplete data records.

+ **3.2.5 (2025-03-25)**
    + Fixes bug in PoissonIntervals distribution where if the last rate is zero or so small there is no samples, the cycle begins again too early.

+ **3.2.4 (2024-12-04)**
    + Adds a new method for the `simulate_until_max_customers`: "Complete" simulates until a specific number of completed customer journeys; while "Finish" simulates until a specific number of customers have reached the exit node (through bailking or reneging).

+ **3.2.3 (2024-10-15)**
    + Allow some numerical imprecision in the PMF probability sums. This allows for very large arrays of probabilities and use of Pandas and Numpy to define probabilities.

+ **3.2.2 (2024-07-05)**
    + Allow custom exit node classes.

+ **3.2.1 (2024-06-19)**
    + Remove `reneging_destinations`, move to a jockeying routing option within the routing objects.

+ **3.2.0 (2024-05-07)**
    + System capacity implemented.
    + Server schedules objects now take `numbers_of_servers` and `shift_end_dates` keywards, instead of `schedule`.
    + Server schedules and slotted services can be `offset`.
    + Added a GroupedNodePopulation tracker.
    + Restructures documentation, adds more guides, and updates reference pages.
    + Routing objects implemented: TransitionMatrix object, ProcessBased object, FlexibleProcessBased object, NetworkRouting object, Direct object, Leave object, Probabilistic object, JoinShortestQueue object, LoadBalancing object
    + Added `reroute` as an option for interrupted preemptive services.

+ **3.1.4 (2024-04-09)**
    + Fix bug where Individual's server isn't reset after a slotted service.

+ **3.1.3 (2024-04-08)**
    + Allows class methods as generator functions for process-based routing.

+ **3.1.2 (2024-04-08)**
    + Fix bug when using Mixture distribution.

+ **3.1.1 (2024-04-04)**
    + Add a MixtureDistrubution that probabilistically chooses from a number of other distributions to sample from.
    + Baulking functions now take the simulation, current node, and current individual.
    + Service disciplines now take the current time.
    + Service disciplines now called when a customer arrives (allowing for lingering customers).
    + Distributions have parameters in their reprs.
    + Adding type hints and better doctrings.

+ **v3.1.0 (2023-12-03)**
    + Server schedules now defined with objects.
    + Slotted services feature added, with capacitated and non-capacitated slots, and pre-emption options.
    + Rename 'continue' pre-emption option to 'resume'.
    + Allows simultaneous renegeing customers.
    + Internal refactoring.

+ **v3.0.2 (2023-11-14)**
    + Fix bug where simulation errors if fist event of a node is a shift change.
    + Minor docstring and documentation changes.
    + Default statetracker is now None.

+ **v3.0.1 (2023-10-31)**
    + Fix bug where class change individual not reset after preemption.

+ **v3.0.0 (2023-08-22)**
    + Adds service disciplines - FIFO, LIFO, SIRO and ability for custom disciplines.
    + Removes baulking and rejection dictionaries, these are recorded as DataRecords.
    + Adds an optional filter to `Q.get_all_records` to filter only records of given types.
    + Removes `ciw.dists.NoArrivals`, can just use `None`.
    + Removes ability to write to file and read from file.
    + Allows any string to represent customer classes.
    + Api changes to `class_change_matrices` and `class_change_distributions`
    + `ciw.trackers.NodeClassMatrix` now required a `class_ordering` keyword to ordet the arbitrary customer class string names.
    + Performance improvements.

+ **v2.3.7 (2023-04-06)**
    + Adds Poisson, Geometric, and Binomial distributions for batching.

+ **v2.3.6 (2023-02-16)**
    + Writes a data record for interrupted services caused by server schedules.
    + Raises an error when an inconsistant number of custom node classes are used.

+ **v2.3.5 (2023-02-07)**
    + Fixes bug caused when implementing preemptive priority classes and server schedules that take all servers off duty.

+ **v2.3.4 (2022-12-07)**
    + PoissonIntervals distribution now allows rates of zero

+ **v2.3.2 (2022-10-07)**
    + Add PoissonIntervals distribution
    + Add numpy random generator, ciw.seed now also creates new random generator
    + Documentation on parallelising trials
    + Remove support for Python 3.6

+ **v2.3.1 (2022-07-25)**
    + Fixes bug where blocked customers were candidates for `finish_service` when more than one customer finishes service simultaneously
    + Correctly writes csv's in Windows
    + Support for Python 3.9 by updating tqdm requirement

+ **v2.3.0 (2022-05-10)**
    + Reneging customers implemented
    + Customer class changes while waiting implemented
    + Preemptive interruption options implemented
    + New record_type field added to DataRecords

+ **v2.2.4 (2022-03-02)**
    + Improve docs on pausing simulations and server priorities
    + Record server ID in the DataRecords
    + Move CI to GitHub Actions

+ **v2.2.3 (2022-01-27)**
    + Server priority functions implemented.

+ **v2.2.2 (2021-12-17)**
    + State trackers now take objects not indices
    + Servers are attached to individuals before sampling service times
    + Docs on sever-dependant distributions
    + Docs on DES+SD hybrid simulations

+ **v2.2.1 (2021-11-04)**
    + PhaseType distributions implemented
    + Classes for specific PhaseType distributions: Erlang, HyperExponential, HyperErlang, and Coxian

+ **v2.2.0 (2021-07-22)**
    + Processor sharing implemented (limited and capacitated)
    + Ability to use a different node_class per node of the network
    + State tracking now works with simulate_until_max_customers
    + Remove testing on Python 3.5

+ **v2.1.3 (2020-10-06)**
    + Small refactor to Node adding new servers, and to Individuals receiving the Simulation object.
    + Add a library of custom behaviour to docs
    + Support Python 3.8, update hypothesis

+ **v2.1.2 (2020-09-26)**
    + Ability to incorporate customer behaviour Server and Individual classes.

+ **v2.1.1 (2020-05-27)**
    + State Trackers slightly more efficent, they do not record any state changes that result in the same state as before.
    + Add the NodePopulationSubset tracker.
    + Distribution objects can now see the Simulation object, for true state dependent distributions.

+ **v2.1.0 (2020-04-23)**
    + State Trackers now track history
    + State Trackers give state probabilities
    + A number of performance improvements
    + Fix some documentation
    + Test on PyPy3.6 and Python 3.7 too

+ **v2.0.1 (2019-07-17)**
    + setup.py now finds packages to fix pip install bug

+ **v2.0.0 (2019-07-10)**
    + Large refactor:
    + Drop support for Python 2.7, Python 3.4.
    + Update networkx and pyyaml requirements.
    + Refactor time so that `Simulation` has `current_time` attribute.
    + Change Transition_matrices keyword to routing.
    + routing can take a process-based routing function.
    + Refactor distributions to be objects: ['Exponential', 0.5] -> ciw.dists.Exponential(0.5).
    + Distribution objects can be manipulated with +, -, * and /.
    + All keywords lower case to conform to Pep8.
    + deadlock_detector keyword takes object, not string.
    + tracker keyword takes object, not string.
    + Add tests and docs to show how objects can be used for state-dependent distributions.
    + All user facing api now takes float('inf') not 'Inf', expect for .yml files.
    + Reference Ciw paper in docs.
    + Add AUTHORS.rst to docs.

+ **v1.1.6 (2018-10-22)**
    + Fixed bug in which preemptively iterrupted individuals remained blocked once service resampled.
    + Fixed bug in which interrupted individuals not removed from interrupted list when restarting service.
    + Some performance improvements.
    + Improve deadlock detection to check for knots less often.


+ **v1.1.5 (2018-01-11)**
    + Fixed bug calculating the utilisation of servers.

+ **v1.1.4 (2017-12-12)**
    + Time dependent batching distributions
    + Hard pin requirements versions

+ **v1.1.3 (2017-08-18)**
    + Replace DataRecord object with namedtuple.
    + Number of minor tweaks for speed improvements.

+ **v1.1.2 (2017-07-05)**
    + Batch arrivals.

+ **v1.1.1 (2017-06-23)**
    + Server utilisation & overtime.
    + Small fixes to docs.
    + Testing on Python 3.6.

+ **v1.1.0 (2017-04-26)**
    + Replace kwargs with actual keyword arguments in ciw.create_network.
    + Refactor server schedule inputs (schedules placed inside Number_of_servers instead of as their own keyword).

+ **v1.0.0 (2017-04-04)**
    + ciw.create_network takes in kwargs, not dictionary.
    + Add Sequential distribution.
    + Add truncated Normal distribution.
    + Refactor inputs for custom PDF.
    + Refactor inputs for server schedules.
    + Transition matrix now optional for 1 node networks.
    + Overhaul of documentation.
    + Add CONTRIBUTING.rst.
    + Slight improvement of ciw.random_choice.

+ **v0.2.11 (2017-03-13)**
    + Add ability to simulate until max number of customers have passed arrived/been accepted/passed through the system.

+ **v0.2.10 (2017-03-10)**
    + Performance improvements.
    + Drop dependency on numpy.

+ **v0.2.9 (2017-02-24)**
    + Allow zero servers.

+ **v0.2.8 (2016-11-10)**
    + Add option for time dependent distributions.

+ **v0.2.7 (2016-10-26)**
    + Run tests on Appveyor.
    + Check docs build and pip installable on Travis.
    + Remove hypothesis cache.

+ **v0.2.6 (2016-10-17)**
    + Add AUTHORS.rst.
    + Add progress bar option.

+ **v0.2.5 (2016-10-06)**
    + Fix bug that didn't include .rst files in MANIFEST.in.

+ **v0.2.4 (2016-09-27)**
    + Fixed bug in which priority classes and dynamic classes didn't work together.
    + New feature: preemptive interruptions for server schedules.

+ **v0.2.3 (2016-07-27)**
    + Ability to set seed. More docs. Fixes to tests.

+ **v0.2.2 (2016-07-06)**
    + Baulking implemented, and minor fixes to order of unblocking.

+ **v0.2.1 (2016-06-29)**
    + Priority classes implemented.

+ **v0.2.0 (2016-06-20)**
    + Python 3.4 and 3.5 compatible along with 2.7.
    + Data records now kept in list.

+ **v0.1.1 (2016-06-06)**
    + Ability to incorporate behaviour nodes.
    + Data records are now named tuples.

+ **v0.1.0 (2016-04-25)**
    + Re-factor inputs.
    + Simulation takes in a Network object.
    + Helper functions to import yml and dictionary to a Network object.
    + Simulation object takes optional arguments: deadlock_detector, exact, tracker.
    + simulate_until_max_time() takes argument max_simulation_time.

+ **v0.0.6 (2016-04-04)**
    + Exactness implemented.
    + Restructure some features e.g. times_to_deadlock.
    + Custom simulation names.

+ **v0.0.5 (2016-03-18)**
    + State space tracker plug-and-playable.
    + Add rejection dictionary.

+ **v0.0.4 (2016-02-20)**
    + Empirical and UserDefined distributions added.
    + Tidy ups.

+ **v0.0.3 (2016-02-09)**
    + Arrival distributions.
    + MMC options removed.
    + Fix server schedule bugs.

+ **v0.0.2 (2016-01-06)**
    + Some kwargs optional.
    + Hypothesis tests.
    + Minor enhancements.

+ **v0.0.1 (2015-12-14)**
    + Initial release.

+ **v0.0.1dev (2015-12-14)**
    + Initial release (dev).
