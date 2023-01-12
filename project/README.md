# Network Visualizer using Panda3D
This project was done for the Visual Computing class for my Masters degree in Computer and Telematics Engineering at University of Aveiro.


## Install requirements
In the repository directory run:
`pip3 install -r requirements.txt`

## Extra Software necessary
The following software must also be installed:
* [GNS3](https://gns3.com/)
* [Wireshark](https://www.wireshark.org/)

# Steps
* [Draw the network in DrawIO](#draw-network-in-drawio)
* [Simulate in GNS3](#simulate-in-gns3)
* [Simulate in Panda3D](#simulate-in-panda3d)

## Draw network in DrawIO
First start by drawing the network in DrawIO following the next rules:
* Only use rectangles in represent pcs, switches and routers;
* Use lines to connect the figures and connect the start point of the line(left point) to the computer that it connects to;
* Don't "bend" the line between figures, always use straight or curved lines between them;
* Name all pcs using the following format: "Name ip", the white space is necessary and the same name must be used in naming the lines, example: "PC1 192.168.0.1";
* Name all Switches using the following format: "SWNumber" where number is any number and name all Routers using the following format: "RNumber" where Number is again any number, example "SW1" ou "R1";
* The lines must be named following the next format: "Name PCName", example: "link1 PC1";

After the network was created select Extra->Edit Diagram and copy all and save to a local file all of xml in the textbox, this file must be saved in the utils folder of the project and be named "diagram.xml". An example of a diagram can be found in the examples folder.

## Simulate in GNS3
Create and configure the network in GNS3 as represented in DrawIO and capture all traffic between each link. After the simulation ends save all captures as .pcap and name them using the name of the link (e.g. link1 PC1) and save this files to the demo folder.

## Simulate in Panda3D
In the project directory just run `python3 main.py` to run the simulation.
