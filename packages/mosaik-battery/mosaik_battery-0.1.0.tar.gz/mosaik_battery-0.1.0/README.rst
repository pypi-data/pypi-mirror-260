==============
mosaik-battery
==============

The adapter was initially developed by Tobias Janke and adjusted for the
mosaik-project by Malte Trauernicht.

Installation
============
* To use this project, you have to install at least version 3.2.0 of `mosaik <https://mosaik.offis.de/>`_
* It is recommended, to use the Mosaik-CSV Library to import battery data

You can install this project through pip with the following command::

    pip install mosaik-battery

How to Use
==========
This demonstartion uses the mosaik-powerplant simulator to charge the batteries. Specify simulators configurations within your scenario script::

    sim_config = {
        'CSV': {
            'python': 'mosaik_csv:CSV',
        },
        'Battery': {
            'python': 'mosaik_components.battery:Simulator'
        },
        'PowerPlant': {
            'python': 'mosaik_components.powerplant:Simulator'
        },
        ...
    }

Initialize the simulators::

    battery_simulator = world.start('Battery',
                                step_size=1800,
                                number_of_schedules=3,
                                charge_power=100,
                                discharge_power=50,
                                battery_capacity=5000,
                                start_soc=0.1,
                                interval_size=2)

    powerplantData = world.start("CSV",
                             sim_start=SIM_START,
                             datafile=POWERPLANT_DATA)

    powerplant_simulator = world.start('PowerPlant',
                                   step_size=1800,
                                   number_of_schedules=3,
                                   ramp_behavior=[2, 2],
                                   min_power=0.5,
                                   max_power=3,
                                   interval_size=2)

Instantiate model entities::

    battery_sim_model = battery_simulator.Battery()
    powerplant_data = powerplantData.NaturalGas()
    powerplant_sim_model = powerplant_simulator.Powerplant()

Connect battery- with powerplant-simulator::

    world.connect(powerplant_data, powerplant_sim_model, 'p_mw')
    world.connect(powerplant_sim_model, battery_sim_model, 'schedules')

