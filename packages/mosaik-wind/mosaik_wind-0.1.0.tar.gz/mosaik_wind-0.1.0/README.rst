===========
mosaik-wind
===========

This program allows to simulate wind-turbines inside mosaik. Original from Fernando Penaherrera, modified by
Christoph Stucke and adapted into the mosaik library by Malte Trauernicht.

Installation
============
* To use this project, you have to install at least version 3.2.0 of `mosaik <https://mosaik.offis.de/>`_
* It is recommended, to use the Mosaik-CSV Library to import wind data

You can install this project through pip with the following command::

    pip install mosaik-wind

How to Use
==========
Specify simulators configurations within your scenario script::

    sim_config = {
        'CSV': {
            'python': 'mosaik_csv:CSV',
        },
        'Wind': {
            'python': 'mosaik_components.wind:Simulator'
        },
        ...
    }

Initialize the wind- and csv-simulator::

    windData = world.start("CSV",
                       sim_start='YYYY-MM-DD HH:mm:ss',
                       datafile='path/to/wind/data.csv')

    wind_simulator = world.start('Wind',
                                 power_curve_csv='path/to/power_curve/data.csv',
                                 step_size=60000
                                 gen_neg=True)

Instantiate model entities::

    wind_speed = windData.Wind()
    wind_sim_model = wind_simulator.WT()

Connect wind- with csv-simulator::

    world.connect(wind_speed, wind_sim_model, 'wind_speed')


CSV-Formatting
==============

For the simulator to work correctly, both .csv files have to be specifically formatted!

wind-data
---------
The wind_data.csv is formatted accordingly to the conventions of the `mosaik_csv <https://gitlab.com/mosaik/components/data/mosaik-csv>`_ simulator::

    Wind
    Date,wind_speed
    YYYY-MM-DD HH:mm:ss,v1
    YYYY-MM-DD HH:mm:ss,v2
    ...

* Each entry in the .csv needs a Date in the YYYY-MM-DD HH:mm:ss format and a wind_speed value v, measured in meters per second.

power-curve
-----------
The power_curve.csv does not need the formatting, of the mosaik_csv simulator::

    wind_speed,power_factor
    a1,b1
    a2,b2
    ...

* The Entries for each data point require the wind_speed a in the Beaufort wind force scale, as well as a corresponding power-factor b in megawatt.
