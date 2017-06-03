# Files explanation
--------
method.json     : methods

operator.json   : operators

realState.json  : simulate the initial real environment

state.json      : simulate the initial belief state

example_v2.dia  : a graph view of the knowledge base

========================================


# knowledge base check list

Operator:
---------

 - use_soap
 - rinse_hand
 - turn_on_faucet1
 - turn_off_faucet1
 - dry_hand
 - switch_on_kettle_1
 - switch_off_kettle_1
 - add_water_kettle_1
 - get_cup_1
	 

Method
-----------
 - clean_hand
 - wash_hand
 - kettle_1_heat_water
 - kettle_1_add_water
 - prepare_hot_water
 - add_tea
 - add_coffee
 - mix_coffee_water
 - mix_tea_water
 - make_coffee
 - make_tea

Object
-----------

 - hand_1
 - faucet_1
 - person_1
 - kettle_1
 - cup_1
 - tea_box_1

Sensor
---------------
 - hand_1-soapy
 - hand_1-dirty
 - hand_1-dry
 - faucet_1-state
 - faucet_1-location
 - person_1-location
 - kettle_1-has_water
 - kettle_1-switch
 - kettle_1-water_hot
 - cup_1-location
 - cup_1-has_water
 - cup_1-has_tea
 - cup_1-has_coffee
 - tea_box_1-location
 - tea_box_1-open

> Written with [StackEdit](https://stackedit.io/).
