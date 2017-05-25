.. _api:

API Documentation
=================

This part of the documentation covers all the interfaces of Travian Legends API.

Account
-------

**class travianapi.Account(url, name, password, headers=None)**

To access your account, you can use Account object. Travian API parses Travian Browser Game's pages for you and gives you access to it through pythonic api. Internally Travian API makes sure that you always get the correct data.

Account gives for you list of villages which are instances of Village class.

You can create many instances of Account class in the same programm.

Account use instance of `Login`_ class.

Parameters:
    * url - url of your server. Example: https://ts70.travian.ru/
    * name - your nickname in travian game
    * password - your password in travian game
    * headers - 

Properties:
    * server_time - time on travian server
    * rank - game rank in travian
    * alliance - your alliance
    * villages_amount - amount of villages
    * pupulation - summary population of account
    * nation_id - nation number
    * nation - nation string name
    * villages - list with all villages
    * villages_names - list with all village names
    * gold - gold number of account
    * silver - silver number of account


**get_village_by_id(id)**

Parameters:
    * id - integer identeficator of village

**get_village_by_name(name)**

Parameters:
    * name - string name of village

Login
-----

Village
-------

Building
--------

Map
---
