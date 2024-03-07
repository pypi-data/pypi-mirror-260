=================
mosaik-powerplant
=================

Simulator for Powerplants in mosaik. The adapter was initially developed by Konstantin Meyer
and adjusted for the mosaik-project by Malte Trauernicht.

Installation
============
* To use this project, you have to install at least version 3.2.0 of `mosaik <https://mosaik.offis.de/>`_
* It is recommended, to use the Mosaik-CSV Library to import powerplant data

You can install this project through pip with the following command::

    pip install mosaik-powerplant

How to Use
==========
Specify simulators configurations within your scenario script::

    sim_config = {
        'CSV': {
            'python': 'mosaik_csv:CSV',
        },
        'PowerPlant': {
            'python': 'mosaik_components.powerplant:Simulator'
    },
        ...
    }

Initialize the powerplant- and csv-simulator::

    powerplantData = world.start("CSV",
                             sim_start=SIM_START,
                             datafile=POWERPLANT_DATA)

    powerplant_simulator = world.start('PowerPlant',
                                   step_size=18000,
                                   number_of_schedules=3,
                                   ramp_behavior=[2, 2],
                                   min_power=0.5,
                                   max_power=3,
                                   interval_size=1)

Instantiate model entities::

    powerplant_data = powerplantData.NaturalGas()
    powerplant_sim_model = powerplant_simulator.Powerplant()

Connect wind- with csv-simulator::

    world.connect(powerplant_data, powerplant_sim_model, 'p_mw')


CSV-Formatting
==============

For the simulator to work correctly, both .csv files have to be specifically formatted!

The csv-data is formatted accordingly to the conventions of the `mosaik_csv <https://gitlab.com/mosaik/components/data/mosaik-csv>`_ simulator::

    Name
    Date,p_mw
    YYYY-MM-DD HH:mm:ss,v1
    YYYY-MM-DD HH:mm:ss,v2
    ...

* Each entry in the .csv needs a Date in the YYYY-MM-DD HH:mm:ss format and a data value v.
