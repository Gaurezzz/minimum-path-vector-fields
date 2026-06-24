# Minimum Distance Path on Vector Fields

**InspiraSTEM 2026 Internship**

*   **Author:** Gabriela Rodriguez
*   **Mentor:** Dr. Manuel Diaz

## Description

This project implements an A* algorithm to find the minimum distance path across a vector field. It calculates the optimal route by taking into account the constant velocity of a particle and the underlying flow velocities of the vector field. It includes mathematical formulations and visualizations using the Manim engine to demonstrate the pathfinding across different flow scenarios.

## Execution

This project uses `uv` for dependency management. Ensure your dependencies are installed by running:

```bash
uv sync
```

### Run the Algorithm

To test the algorithm independently and print the calculated path coordinates and times, run:

```bash
uv run python minimum_path_algorithm.py
```

### Run the Animations

The project uses Manim to visualize the minimum distance paths on different vector fields. You can render these animations by executing the following commands.

**Trigonometric Field Simulation:**
```bash
uv run manim -pql track_simulation.py Trigonometric_field_simulation
```

**Cavity Flow Simulation:**
```bash
uv run manim -pql track_simulation.py Cavity_flow_simulation
```

**Channel Flow Simulation:**
```bash
uv run manim -pql track_simulation.py Channel_flow_simulation
```

*Note: You can add `_x2` to the class name in the command to run the simulation with double velocity (e.g., `Trigonometric_field_simulation_x2`).*
