# RobotRaconteur object type and value type Example
Each folder contains a simple service with service definition and a simple client, demonstrating how each object/value type works in RR
## device_info
how to load device metadata from yaml into RR service

## event
how to use RR event to generate interrupts given certain condition

## generator
A similar way to python Generators, to keep process running with continuous function call for safety

## map
RR representation of a dictionary

## pipe
Data streaming method, triggers function call back when new data comes in

## wire
Data streaming method, able to access anytime, also could trigger callback with `WireValueChanged`

## async
Async function examples to be used as non-blocking