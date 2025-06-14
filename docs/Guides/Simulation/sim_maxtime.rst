.. _until-maxtime:

============================================
How to Simulate For a Certain Amount of Time
============================================

Once the simulation object has been created, it can be simulated until a certain amount of simulation-time has passed. This is done with the :code:`simulate_until_max_time` method, which takes in the :code:`max_simulation_time` positional keyword::

    >>> Q.simulate_until_max_time(max_simulation_time=100.0)  # doctest:+SKIP

Notes
~~~~~

Note that the simulation will finish as soon as the time of the next scheduled event is after the :code:`max_simulation_time`. The clock will reach this nect event date, but not carry out the event. E.g. consider the following system with sparce events::

    >>> import ciw
    >>> N = ciw.create_network(
    ...     arrival_distributions=[ciw.dists.Deterministic(value=7.0)],
    ...     service_distributions=[ciw.dists.Deterministic(value=2.0)],
    ...     number_of_servers=[1]
    ... )

    >>> Q = ciw.Simulation(N)
    >>> Q.simulate_until_max_time(22.0)

We will see there there have been three arrivals at dates 7, 14 and 21, but only two completed services at dates 9 and 16, Next scheduled event for the arrival node is at date 28.0, the next scheduled event for the single service node is at date 23.0, and the next scheduled event date for the exit node is set if infinity.::

    >>> recs = Q.get_all_records() # Completed records
    >>> [r.arrival_date for r in recs]
    [7.0, 14.0]
    >>> Q.current_time
    22.0
    >>> [nd.next_event_date for nd in Q.nodes]
    [28.0, 23.0, inf]

