# Project Overview
This project is a collaboration between users: @Antheagao and @danmrt. This project was created for our ***Project in CS: Artificial Intelligent Systems***. 

Our project entails a program, ran on an IDE, that provides the optimal order of operations to *onload*/*offload* and *balance* shipping containers on a ship. 

The program takes a manifest file as input, which is set to a specific format that contains the *(X,Y) coordinates*, *weight (kg)*, and *container label*/*status*. 

The program is meant to be used for shipping container movements at shipping docks, thus it comes featured with 
* **user sign-in/sign-out**
* **optimal order of operations list for the crane operator**
* **estimated time of completion to move all shipping containers**
* **ASCII text-art to illustrate the ship's dock, and illustrate which coordinate the container should be moved to**
* **option to add comments to the log file, which is keeping track of user's actions (to be sent to management of whomever wishes to use the program)**
* **ability to balance the weight of the ship, following Maritime Law, in a reasonable and optimal amount of time**
* **ability to offload a specific shipping container, given the container's label, using an optimal order of operations**

# Inputs
The program takes user inputs such as **ASCII text-inputs**, **user-typed comments**, and **a manifest file** (shown in the format seen below). 

![image](https://github.com/Antheagao/Shipping_Container_Project/assets/91440304/9baa42ed-92f1-4087-80f2-7bf88b6c72de)

The image above describes how the manifest file format looks, this is the input taken by the program. The grid is a visual represenation of what the manifest represents.

# Offloading

test

# Onloading
The program handles **onloading** by calculating an optimal path to onload the shipping container requested from the shipping dock to the nearest available ship coordinate.

We have an example of the ***Onloading*** feature below:

## Onloading : Example

Upon compilation of the program, it will ask for *user sign-in*, and then request the manifest .txt file

Once entered, the program (in ASCII text art) visualizes the manifest .txt file into a visual representation of the ship's containers on-board. 

![image](https://github.com/Antheagao/Shipping_Container_Project/assets/91440304/271d131c-3113-4e82-b3aa-32e84acfa7f1)

The ASCII text art illustrates the empty possible coordinates on the ship where containers can be onloaded, and illustrates the spots where NO CONTAINER can be placed (visualized as +++).

The program will ask for user-input to choose either the *Balancing* or the *Unload/load* option. We will choose the second option here.

![image](https://github.com/Antheagao/Shipping_Container_Project/assets/91440304/9c09d49e-6259-4437-84d4-a4c85b8a0c58)

The user is met with text by the console, indicating what should be typed into the console. For this instance, since we are not *unloading*, we ignore and follow the *load* options.

The user can enter the name of the label we want to input, and its respective weight. The user can enter as many containers as necessary until they are done or until max capacity is met.

Following submission of containers to be *loaded*, the program completes an optimal pathing for *loading*, and estimates the time of completion. 

The program will ask for user input each container movement, giving potential options to **confirm the move**, **switch user**, or **write an issue to log file**.  

The program gives a visual representation of where the shipping container with its respective label should be placed shown by the **ASCII text art** and ship's coordinates. 

![image](https://github.com/Antheagao/Shipping_Container_Project/assets/91440304/5741da76-e5a8-4241-b9ed-6a0f8b0507f9)

The program asks for the user to send the *newly created manifest file* to admin for further use.

The program will continue to display **ASCII text art** to illustrate where the specific container should be placed, and ask the user whether they want to work on a *different ship*.
















