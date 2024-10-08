# KHARBOUCHE BILAL MIAAD
bilal.kharbouche99@gmail.com

## Flexible Job Shop Scheduling Problem (FJSSP) Optimization

### Description
This project focuses on solving the **Flexible Job Shop Scheduling Problem (FJSSP)** using a combination of **Genetic Algorithms** and **Reinforcement Learning** techniques such as **SARSA**, **Q-learning**, and **Double Q-learning**. It is developed as part of my Master's thesis in Artificial Intelligence and Data Science.

The FJSSP is an NP-hard problem where jobs need to be scheduled on machines with flexibility in job routing. The goal is to optimize the allocation and sequencing of jobs to minimize makespan (total time) or other performance metrics.

### Technologies Used
- **Python** for the implementation of algorithms.
- **Genetic Algorithms (GA)** for generating near-optimal schedules.
- **Reinforcement Learning** techniques such as **SARSA**, **Q-learning**, and **Double Q-learning** to enhance the scheduling process dynamically.
- **Matplotlib** for visualizing results (Gantt charts, convergence plots, etc.).

### Features
- **Flexible job and machine assignment:** Jobs can be processed on different machines, and the algorithm selects the best machine dynamically.
- **Optimization:** Combines the exploration-exploitation strategies of reinforcement learning with the genetic algorithm's ability to search the solution space.
- **Comparison of Algorithms:** Allows comparing the performance of SARSA, Q-learning, and Double Q-learning in optimizing FJSSP.
- **Visualizations:** Displays Gantt charts and convergence graphs of the optimization process.

### Setup and Installation

#### Prerequisites
- **Python 3.9** or later
- **Numpy**, **Matplotlib**, and other required libraries (see `requirements.txt`)

#### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/username/FJSSP-Optimization-Genetic-Reinforcement.git
    cd FJSSP-Optimization-Genetic-Reinforcement
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Project
To run the optimization, use the following command:
```bash
python main.py data.txt
