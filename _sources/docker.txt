==========================
Using the docker appliance
==========================

.. jnt-badge::
    :badges: docker


Installing Docker
=================

Install docker using the following documentation https://docs.docker.com/engine/installation/


Initial installation
====================

Pull the image :

.. code:: bash

    $ docker pull bibi21000/janitoo_nut

Create a 'store' container  :

.. code:: bash

    $ docker create -v /root/.ssh/ -v /opt/janitoo/etc/ --name nut_store bibi21000/janitoo_nut /bin/true

Create a 'running' container :

.. code:: bash

    $ docker create --volumes-from nut_store -p 8883:22 --name nut_running bibi21000/janitoo_nut

Yous should now have 2 created containers :

.. code:: bash

    $ docker ps -a

.. code:: bash

    CONTAINER ID        IMAGE                          COMMAND             CREATED             STATUS      PORTS       NAMES
    2f2496fbd885        bibi21000/janitoo_nut          "/root/auto.sh"     9 seconds ago       Created                                    nut_running
    1b6e0270e728        bibi21000/janitoo_nut          "/bin/true"         20 seconds ago      Created                                    nut_store


Start the container
===================

Start it :

.. code:: bash

    $ docker start nut_running

Check that is running :

.. code:: bash

    $ docker ps

.. code:: bash

    CONTAINER ID        IMAGE                          COMMAND             CREATED              STATUS          PORTS                  NAMES
    cc1a58b59f7c        bibi21000/janitoo_nut   "/root/auto.sh"     About a minute ago   Up 8 seconds    0.0.0.0:8882->22/tcp   nut_running

And stop it :

.. code:: bash

    $ docker stop nut_running


Customize your installation
===========================

You can find basis customizations tips here : https://bibi21000.github.io/janitoo_docker_appliance/customize.html.

This configuration is saved in the 'store' container.

Configuration
-------------

Update the nut configuration file :

.. code:: bash

    $ ssh root@$127.0.0.1 -p 8883

Default password is janitoo. You can change it but it will be restored on the next running container update. Prefer the key solutions.

Open the configuration file. The docker image contains a nano or vim for editing files :

.. code:: bash

    root@8eafc45f6d09:~# vim /opt/janitoo/etc/janitoo_nut.conf

You must at least update the broker ip. It should match the ip address of your shared "mosquitto" :

.. code:: bash

    broker_ip = 192.168.1.14

If you plan to install more than one janitoo_nut image on your network, you must change the hadd of the bus and components :

.. code:: bash

    hadd = 0120/0000

to

.. code:: bash

    hadd = 0124/0000

And so on for 0120/0001, 0120/0002, ... Keep in mind that hadd must be unique on your network.

Save your updates and restart jnt_nut :

.. code:: bash

    root@8eafc45f6d09:~# killall jnt_nut

Ups
---

Update the ip, upsname, username ans password matching your nut server installation :

.. code:: bash

    [nut__ups1]
    heartbeat = 60
    name = UPS 1
    hadd = 0120/0001
    ip_ping_config_0 = 127.0.0.1
    username_0 = monuser
    upsname_0 = UPS
    password_0 = pass

Save and restart your server to apply.

Performances
============

The top result in the running appliance :

.. code:: bash

    root@7de7e4993b13:~# top

.. code:: bash

    top - 23:48:17 up 1 day,  5:26,  1 user,  load average: 0.30, 0.48, 0.62
    Tasks:   8 total,   1 running,   7 sleeping,   0 stopped,   0 zombie
    %Cpu(s):  3.7 us,  1.6 sy,  0.0 ni, 94.0 id,  0.7 wa,  0.0 hi,  0.0 si,  0.0 st
    KiB Mem:  11661364 total, 11039556 used,   621808 free,  1717756 buffers
    KiB Swap: 19530748 total,    10940 used, 19519808 free.  4097780 cached Mem

      PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
       59 root      20   0  479980  21756   4368 S   2.3  0.2   0:45.43 jnt_nut
      105 root      20   0   21940   1416   1048 R   0.3  0.0   0:00.01 top
        1 root      20   0   21740   1604   1328 S   0.0  0.0   0:00.04 auto.sh
       10 root      20   0   55508  10180   1412 S   0.0  0.1   0:00.22 supervisord
       11 root      39  19   23500   1496   1200 S   0.0  0.0   0:00.42 top
       12 root      20   0   55176   3116   2444 S   0.0  0.0   0:00.02 sshd
       30 root      20   0   82716   3928   3072 S   0.0  0.0   0:00.18 sshd
       32 root      20   0   20244   2020   1528 S   0.0  0.0   0:00.02 bash

Administer your containers
==========================

You can find basis administration tips here : https://bibi21000.github.io/janitoo_docker_appliance/administer.html.
