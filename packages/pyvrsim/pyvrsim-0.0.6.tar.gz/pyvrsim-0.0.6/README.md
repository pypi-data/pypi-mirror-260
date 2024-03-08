# PyVRSim: Vehicle Routing Data Simulator in Python

[Pyvrsim](https://pypi.org/project/pyvrsim) is an open-source, user-friendly Python 3 library designed for simulating
data related to vehicle routing, capacitated vehicle routing, and drone routing problems. Utilizing the Google API,
Pyrosim extracts real distances and estimated times between locations, enhancing the accuracy and realism of
simulations.


<p align="center">
  <img src="https://github.com/benmhamed-a/pyvrsim/blob/main/docs/logo/pyvrsim-logo.png" alt="My Logo" width="400" height="200">
</p>

# Installation

To install [Pyvrsim](https://pypi.org/project/pyvrsim), simply use pip to download and install the library
from [PyPI](https://pypi.org/project/pyvrsim) (Python Package Index). The library is at PyPI at this
page https://pypi.org/project/pyvrsim.

Install Pyrosim with the following command:

```python
pip install pyvrsim
```

# Features

## Geographical Realism

- Integrate with geographical data sources or APIs to retrieve real-world maps, roads, and locations.
- Allow users to specify regions of interest, and generate routing problems based on actual geographical data.

## Customizable Parameters:

- Provide a wide range of parameters for users to customize, such as the number of locations, distribution of customers,
  vehicle capacities, time windows, and drone capabilities.
- Allow users to set constraints and preferences for their specific scenarios.

## Seasonal Variations:

- Introduce the concept of seasonal variations, where the characteristics of the routing problem (e.g., demand, road
  conditions) change based on seasons.
- Enable users to simulate how routing problems may differ during different times of the year.

## Traffic Conditions:

- Incorporate options to simulate varying traffic conditions throughout the day.
- Allow users to set peak hours, road closures, or traffic congestion parameters to make the generated data more
  dynamic.

## Dynamic Customer Behavior:

- Model dynamic customer behavior, such as changing demand patterns, cancellations, or urgency levels.
- Introduce randomness in customer behavior to simulate real-world uncertainties.

## Integration with External APIs:

- Allow users to integrate external APIs for additional data, such as weather conditions, special events, or road
  closures, that can impact routing decisions.

## Drone-Specific Parameters:

- Extend the data generation for Drone Routing Problems by including parameters specific to drones, such as flight
  range, recharge time, and restrictions on flying over certain areas.

## Data Validation:

- Implement mechanisms to validate generated data for consistency and realism.
- Provide feedback to users if the specified parameters result in unrealistic or impractical routing problems.

## Exporting to Standard Formats:

- Provide a visual preview of the generated data, allowing users to inspect the distribution of customers, road
  networks, and other relevant details before exporting.

## Documentation and Examples:

- Include comprehensive documentation with examples demonstrating how to use the data generation features effectively.
- Provide guidance on how users can incorporate the generated data into their own projects.

# VRP Variants

## Classical VRP (CVRP):

- Involves a fleet of vehicles delivering goods from a central depot to a set of customers.
- Objective is to minimize the total distance traveled or the number of vehicles used while satisfying customer demand
  and capacity constraints.

## VRP with Time Windows (VRPTW):

- Adds time windows to the CVRP, where each customer has a specified time frame during which deliveries must be made.

## VRP with Pickup and Delivery (VRPPD):

- Includes both delivery and pickup locations, where vehicles must pick up and deliver goods.

## VRP with Split Deliveries:

- Permits the splitting of a customer's demand across multiple vehicles.

## Stochastic VRP (SVRP):

- Incorporates uncertainty in parameters such as travel times or customer demand.

## Periodic VRP (PVRP):

- Addresses situations where customers must be visited periodically, rather than just once.

## Capacitated VRP (CVRP):

- Introduces capacity constraints on the vehicles, ensuring that the total demand served by each vehicle does not exceed
  its capacity.

## VRP with Multiple Depots (MDVRP):

- Involves multiple depots from which vehicles must start and end their routes.

## VRP with Time-dependent Travel Times (VRPTD):

- Considers varying travel times based on the time of day or traffic conditions.

# VRP variants with drones:

## VRP with Drones (VRPD):

- Integrates drones into the delivery process, allowing them to transport goods between the depot and customers or
  between customers.

## VRP with Hybrid Fleet (VRPHF):

- Involves a combination of traditional vehicles and drones in the fleet.

## VRP with Drone Recharging (VRPDR):

- Considers the need for drones to recharge their batteries during the delivery process.

## VRP with Drones and Time Windows (VRPDTW):

- Combines the time window constraints with the integration of drones.

## VRP with Drones and Split Deliveries:

- Incorporates both the capability of drones and the option to split deliveries.

## VRP with Drones and Pickup-Delivery (VRPDPD):

- Extends the VRPPD to include drones in the pickup and delivery operations.

# Usage

Examples here.

# Documentation

Documentation sources here.

# License

My license here.