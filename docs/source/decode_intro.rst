FTC 2025~2026 Decode: The Automation Roadmap
============================================

Welcome to the breakdown of the FTC 2025~2026 season: **Decode**. This year, the bridge between manual control and high-efficiency scoring is built on **automation**.

The Game Flow
-------------

The match is divided into three critical phases. Automation is the key to maximizing points in the transitions.

.. mermaid::

   graph TD
       Start((Start)) --> Auto[Autonomous - 30s]
       Auto --> TeleOp[TeleOp - 120s]
       TeleOp --> Endgame[Endgame - Last 30s]
       Endgame --> End((End))
       
       subgraph "Automation Peaks"
       Auto
       TeleOp
       Endgame
       end

Scoring Calculus
----------------

To decide which tasks to prioritize, teams should calculate their **Cycle Efficiency** ($E$).

.. math::

   E = \frac{P_{total}}{T_{cycle}}

Where:
* $P_{total}$ is the total points scored in one cycle.
* $T_{cycle}$ is the time in seconds taken to complete the cycle.

The path to "Auto-Drive"
------------------------

For rookie and medium teams, the goal is to move from pure manual driving to **assisted driving**. This includes:

1. **Auto-Aim:** Using vision sensors to align with goals automatically.
2. **Path Correction:** Using IMUs to maintain heading despite collisions.
3. **Smart Intake:** Automating motor speeds based on distance sensors.

By mastering these "illegal" (highly efficient) techniques, teams can outperform even the fastest manual drivers.
