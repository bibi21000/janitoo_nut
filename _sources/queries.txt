=======
Queries
=======


.. code:: bash

    $ jnt_query node --hadd 0120/0000 --host=192.168.14.65 --vuuid=all

.. code:: bash

    request_info_nodes
    ----------
    hadd       uuid                           name                      location             product_type
    0120/0000  nut                            Default bus name controller Default location     Default product type
    0120/0001  nut__ups1                      UPS                       Default location     3B1006X72726

.. code:: bash

    request_info_users
    ----------
    0120/0001  nut__ups1                 status                         0    OL                        None       8     2     49       The status of the UPS
    0120/0001  nut__ups1                 ip_ping                        0    1                         None       1     2     48       Ping the nut server
    0120/0001  nut__ups1                 battery_chemistry              0    PbAc                      None       8     2     49       The chemistry of the battery
    0120/0001  nut__ups1                 battery_voltage                0    13.6                      V          3     2     49       The voltage of the battery
    0120/0001  nut__ups1                 battery_charge                 0    100                       %          3     2     49       The charge of the battery
    0120/0001  nut__ups1                 battery_runtime                0    637                       Seconds    4     2     49       The left runtime of the battery

.. code:: bash

    request_info_configs
    ----------
    0120/0001  nut__ups1                 username                       0    monuser                   None       8     3     112      Username to connect the nut server
    0120/0001  nut__ups1                 name                           0    UPS                       None       8     3     112      The name of the node
    0120/0001  nut__ups1                 battery_voltage_poll           0    90                        seconds    4     3     112      The poll delay of the value
    0120/0001  nut__ups1                 upsname                        0    UPS                       None       8     3     112      Ups name on the nut server
    0120/0001  nut__ups1                 battery_charge_poll            0    90                        seconds    4     3     112      The poll delay of the value
    0120/0001  nut__ups1                 status_poll                    0    60                        seconds    4     3     112      The poll delay of the value
    0120/0001  nut__ups1                 battery_runtime_poll           0    90                        seconds    4     3     112      The poll delay of the value
    0120/0001  nut__ups1                 location                       0    Default location          None       8     3     112      The location of the node
    0120/0001  nut__ups1                 ip_ping_poll                   0    30                        seconds    4     3     112      The poll delay of the value
    0120/0001  nut__ups1                 ip_ping_config                 0    192.168.14.5              None       33    3     112      The IP of the NUT server
    0120/0001  nut__ups1                 battery_chemistry_poll         0    1800                      seconds    4     3     112      The poll delay of the value
    0120/0001  nut__ups1                 password                       0    pass                      None       20    3     112      Password to connect the nut server
    0120/0001  nut__ups1                 port                           0    3493                      None       4     3     112      Port to connect the nut server
    0120/0000  nut                       location                       0    Default location          None       8     3     112      The location of the node
    0120/0000  nut                       name                           0    Default bus name controller None       8     3     112      The name of the node

.. code:: bash

    request_info_systems
    ----------
    0120/0001  nut__ups1                 heartbeat                      0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0120/0001  nut__ups1                 config_timeout                 0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0120/0001  nut__ups1                 hadd                           0    0120/0001                            32    4     112      The Janitoo Home address
    0120/0000  nut                       heartbeat                      0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0120/0000  nut                       config_timeout                 0    5.0                       seconds    4     4     112      The config timeout before applying configuration and rebooting
    0120/0000  nut                       hadd                           0    0120/0000                            32    4     112      The Janitoo Home address

.. code:: bash

    request_info_basics
    ----------

.. code:: bash

    request_info_commands
    ----------
