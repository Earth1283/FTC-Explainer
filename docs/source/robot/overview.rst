Overview
========

Package layout
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Package
     - Contents
   * - ``constants``
     - Hardware device names (:doc:`constants`), dashboard-tunable values, and
       field positions used by autonomous.
   * - ``pedroPathing``
     - Pedro Pathing library configuration (``Constants``) and the
       library-provided tuning menu OpMode (``Tuning``).
   * - ``subsystems``
     - One class per physical mechanism: ``Drivetrain``, ``Shooter``,
       ``Intake``, plus ``Robot`` (composition root), ``Follower`` (Pedro
       Pathing wrapper) and ``Drawing`` (FTC Dashboard field visualization).
   * - ``commands``
     - FTCLib ``Command`` implementations built on top of the subsystems.
       Currently just ``DrivePointToPoint``.
   * - ``auto``
     - Four ``Autonomous`` OpModes (alliance x start position), built as
       command sequences.
   * - ``teleOp``
     - Seven ``TeleOp`` OpModes, from a minimal two-gamepad baseline up to
       field-oriented driving with auto-aim.

Composition
-----------

Every OpMode owns one ``Robot`` instance, which owns the three hardware
subsystems. Autonomous OpModes additionally own a ``Follower`` (Pedro
Pathing) to drive between named field positions, and use
``DrivePointToPoint`` commands scheduled through FTCLib's
``CommandScheduler``.

.. mermaid::

   graph TD
       subgraph Constants
           RobotConfig["RobotConfig<br/>(hardware map names)"]
           RobotConstants["RobotConstants<br/>(dashboard-tunable values)"]
           AutoConstants["AutoConstants<br/>(field Poses)"]
           PedroConstants["pedroPathing.Constants<br/>(Follower/PIDF setup)"]
       end

       subgraph Subsystems
           Robot --> Drivetrain
           Robot --> Intake
           Robot --> Shooter
       end

       Follower -->|built from| PedroConstants
       Drivetrain -->|reads| RobotConfig
       Shooter -->|reads| RobotConfig
       Shooter -->|reads PIDF/velocities| RobotConstants
       Intake -->|reads| RobotConfig

       DrivePointToPoint -->|drives| Follower

       AutoOpModes["auto.* OpModes"] --> Robot
       AutoOpModes --> Follower
       AutoOpModes --> DrivePointToPoint
       AutoOpModes -->|reads start/via Poses| AutoConstants

       TeleOpModes["teleOp.* OpModes"] --> Robot
       TeleOpModes -->|reads targets/velocities| RobotConstants

       Drawing["Drawing<br/>(FTC Dashboard field)"] --> Follower

OpMode lifecycle
-----------------

Autonomous OpModes extend the iterative ``OpMode`` base class. The
command sequence is built once in ``start()`` and then driven forward one
tick at a time from ``loop()`` via ``CommandScheduler``.

.. mermaid::

   sequenceDiagram
       participant DS as Driver Station
       participant OM as Auto OpMode
       participant CS as CommandScheduler
       participant F as Follower

       DS->>OM: init()
       OM->>F: new Follower(hardwareMap)
       OM->>F: setStartingPose(...)
       loop init_loop() (until Start pressed)
           OM->>F: follower.update()
           OM->>OM: draw robot on dashboard field
       end
       DS->>OM: start()
       OM->>CS: schedule(SequentialCommandGroup)
       loop loop() (every cycle)
           OM->>CS: run()
           CS->>F: DrivePointToPoint.execute() / isFinished()
           OM->>F: follower.update()
           OM->>OM: draw debug overlay
       end
       DS->>OM: stop()
       OM->>CS: reset()

TeleOp OpModes extend ``LinearOpMode`` instead, and drive the subsystems
directly from a ``while (opModeIsActive())`` loop each frame — there is no
command scheduler involved on the driver-control side.

Where to go next
-----------------

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Constants
      :link: constants
      :link-type: doc

      Hardware device names, dashboard-tunable values, and the field
      ``Pose`` library used by autonomous.

   .. grid-item-card:: Subsystems
      :link: subsystems
      :link-type: doc

      ``Drivetrain``, ``Shooter``, ``Intake`` and the supporting
      ``Robot``, ``Follower`` and ``Drawing`` classes.

   .. grid-item-card:: Autonomous
      :link: autonomous
      :link-type: doc

      How the four ``auto.*`` OpModes chain ``DrivePointToPoint`` commands
      into full scoring routines.

   .. grid-item-card:: TeleOp
      :link: teleop
      :link-type: doc

      Gamepad mappings across the seven driver-control OpModes.
