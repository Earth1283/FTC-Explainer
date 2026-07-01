Autonomous
==========

There are four ``@Autonomous`` OpModes in ``src/auto/``, one per
alliance/start-position combination:

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - OpMode
     - Driver Station name
     - Route
   * - ``AutoBlueNear15``
     - "BLUE \| Near \| 15"
     - Near-side start, 3 intake/shoot cycles plus a human-player gate pickup
   * - ``AutoRedNear15``
     - "RED \| Near \| 15"
     - Mirror of the above (see :doc:`constants`)
   * - ``AutoBlueFar``
     - "BLUE \| Far"
     - Far-side start, 3 intake/shoot cycles from one shooting spot
   * - ``AutoRedFar``
     - "RED \| Far"
     - Mirror of the above

All four share the same structure: ``init()`` builds a ``Follower`` and
sets its starting pose; ``init_loop()`` continuously updates the odometry
and dashboard field view while waiting for Start, and also writes
``RobotConstants.autoEndX/Y/H`` from the route's park pose so TeleOp can
seed its odometry from wherever autonomous parked; ``start()`` schedules
one long ``SequentialCommandGroup`` of ``DrivePointToPoint`` /
``InstantCommand`` / ``WaitCommand`` steps; ``loop()`` just pumps
``CommandScheduler`` and the follower/dashboard each tick. See
:doc:`overview` for the full lifecycle sequence diagram.

Near route
----------

Preload shot, then three cycles of *drive to a stack → intake → drive to
shoot → fire*, plus one extra pickup via the human-player gate between the
first and second stack. Node names below are the ``AutoConstants`` fields
used by ``AutoBlueNear15``; drop the ``BLUE_NER_`` prefix to read them.

.. mermaid::

   flowchart TD
       START(["START\n(20,121,135°)"]) --> SHOOT0["SHOOT_0\nfire preload"]
       SHOOT0 --> IPRE2["INTAKE_PRE_2"] --> I2["INTAKE_2\nintake"]
       I2 --> GMID["GATE_MID"] --> SHOOT2A["SHOOT_2\nfire"]
       SHOOT2A --> GMID2["GATE_MID_2"] --> GATE["GATE"]
       GATE --> SMID["SUCK_MID"] --> S3["SUCK_3\nintake"]
       S3 --> GMID2b["GATE_MID"] --> SHOOT2B["SHOOT_2\nfire"]
       SHOOT2B --> IPRE1["INTAKE_PRE_1"] --> I1["INTAKE_1\nintake"]
       I1 --> SHOOT2C["SHOOT_2\nfire"]
       SHOOT2C --> IPRE3["INTAKE_PRE_3"] --> I3["INTAKE_3\nintake"]
       I3 --> SHOOT2D["SHOOT_2\nfire"]
       SHOOT2D --> PARK(["PARK\n(33,67,90°)"])

The turret is preset with ``turnTurretToDeg`` before each drive-to-shoot
leg rather than tracked live (``AutoBlueNear15`` uses 0° for the preload
and -43° afterward; ``AutoRedNear15`` mirrors these to 0° / 38°) — auto
doesn't call ``smartTurretTracking``.

Far route
---------

Preload shot, then three intake cycles that all return to the *same*
shooting spot (``FAR_SHOOT``) rather than a sequence of different ones.

.. mermaid::

   flowchart TD
       START(["START\n(56,7,90°)"]) --> SHOOT["FAR_SHOOT\nfire preload"]
       SHOOT --> I1["INTAKE_1"] --> I2["INTAKE_2"] --> I2M["INTAKE_2_MID"] --> I3["INTAKE_3\nintake"]
       I3 --> SHOOT2["FAR_SHOOT\nfire"]
       SHOOT2 --> I1b["INTAKE_1"] --> I2b["INTAKE_2"] --> I4a["INTAKE_4\nintake"]
       I4a --> SHOOT3["FAR_SHOOT\nfire"]
       SHOOT3 --> I1c["INTAKE_1"] --> I2c["INTAKE_2"] --> I4b["INTAKE_4\nintake"]
       I4b --> SHOOT4["FAR_SHOOT\nfire"]
       SHOOT4 --> PARK(["PARK\n(35,10,90°)"])

Each intake leg to ``INTAKE_1``/``INTAKE_2`` is wrapped in a
``ParallelRaceGroup`` against a 1000 ms ``WaitCommand`` — the drive is cut
short at 1 second even if the path hasn't finished, keeping cycle time
predictable if a pickup is slightly off.

Shoot/fire timing
------------------

Every "fire" step in both routes follows the same three-command pattern:

.. code-block:: java

   new InstantCommand(() -> robot.intake.intakeIn(0.6)), // feed a ball toward the gate
   new WaitCommand(200 /* or 300, 800, 1000 */),          // let the flywheel settle
   new InstantCommand(() -> robot.shooter.triggerFire()), // open the gate
   new WaitCommand(1000),
   new InstantCommand(() -> robot.shooter.triggerHold()), // close the gate

Flywheel velocity is set once per route with
``robot.shooter.setShooterVelocity(SHOOT_VELOCITY_*_AUTO)`` before the
first drive leg, and bumped to a second value
(``SHOOT_VELOCITY_FAR_AUTO_2``) partway through the Far route.
