Constants
=========

All tunable/config values live under ``src/constants/`` and
``src/pedroPathing/Constants.java``. None of the subsystem or OpMode code
hardcodes hardware names, PIDF gains, or field positions directly — everything
routes through one of the four classes below.

RobotConfig
-----------

``src/constants/RobotConfig.java`` holds the hardware map device names. These
strings must exactly match the names entered in the Driver Station's
*Configure Robot* menu — this is the only place they're defined, so a rename
on the Driver Station only requires editing this file.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Constant
     - Value
     - Device
   * - ``LEFT_FRONT`` / ``LEFT_BACK``
     - ``"lf"`` / ``"lb"``
     - Drivetrain motors (left side)
   * - ``RIGHT_FRONT`` / ``RIGHT_BACK``
     - ``"rf"`` / ``"rb"``
     - Drivetrain motors (right side)
   * - ``PIN_POINT``
     - ``"pp"``
     - goBILDA Pinpoint odometry computer
   * - ``LEFT_SHOOTER`` / ``RIGHT_SHOOTER``
     - ``"ls"`` / ``"rs"``
     - Flywheel motors
   * - ``INTAKE``
     - ``"intake"``
     - Intake motor
   * - ``SHOOTER_PANEL``
     - ``"panel"``
     - Hood/panel servo (adjusts shot arc)
   * - ``LEFT_GATE`` / ``RIGHT_GATE``
     - ``"lg"`` / ``"rg"``
     - Gate servos that release balls into the flywheels
   * - ``LEFT_TURRET`` / ``RIGHT_TURRET``
     - ``"lt"`` / ``"rt"``
     - Turret aiming servos
   * - ``LEFT_TURRET_SWITCH`` / ``RIGHT_TURRET_SWITCH``
     - ``"lts"`` / ``"rts"``
     - Turret limit switches
   * - ``TRIGGER_SERVO`` / ``TRIGGER_MOTOR``
     - ``"ts"`` / ``"tm"``
     - Declared but unused by any current subsystem

RobotConstants
--------------

``src/constants/RobotConstants.java`` is annotated ``@Configurable``, so every
public ``static`` field is live-editable from FTC Dashboard/Panels while the
robot runs — useful for tuning shot velocity or PIDF gains without
redeploying code.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field(s)
     - Purpose
   * - ``teleOpTargetXR/YR``, ``teleOpTargetXB/YB``
     - Fixed goal coordinates for the Red and Blue alliances.
   * - ``teleOpTargetX``, ``teleOpTargetY``
     - The *active* target, copied from the alliance-specific pair above at
       the start of each OpMode. ``Shooter.smartTurretTracking`` and
       ``Drivetrain``'s aiming helpers read these.
   * - ``MANUAL_POS``
     - Pose used to re-zero odometry mid-match (bound to a d-pad press in
       most TeleOps), copied from ``AutoConstants.BLUE_MANUAL_POS`` /
       ``RED_MANUAL_POS``.
   * - ``FAST_RECOVERY_P/I/D/F``
     - Flywheel velocity PIDF gains passed to
       ``DcMotorEx.setVelocityPIDFCoefficients``. See
       :doc:`shooter_tuning` for how to tune these.
   * - ``autoEndX/Y/H``
     - Robot pose at the end of autonomous, written by each ``auto.*``
       OpMode's ``init_loop()`` and read by TeleOp to seed odometry so the
       driver doesn't have to re-zero at the start of the match.
   * - ``SHOOT_VELOCITY_NER_1/2``, ``SHOOT_VELOCITY_FAR``
     - TeleOp flywheel target velocities (ticks/s) for near and far shots.
   * - ``SHOOT_VELOCITY_NER_AUTO``, ``SHOOT_VELOCITY_FAR_AUTO(_2)``
     - Equivalent velocities used inside autonomous routines.
   * - ``PANEL_NER_1/2``, ``PANEL_FAR``, ``PANEL_NER_AUTO(_FAR)``
     - Hood/panel servo positions paired with the velocities above.
   * - ``website``
     - URL printed to telemetry for the FTC Dashboard webserver.

AutoConstants
-------------

``src/constants/AutoConstants.java`` defines every named field ``Pose`` used
by the autonomous routines, as ``(x, y, headingRadians)`` in inches on a
144x144 in field.

Blue and Red are mirror images across the field's center line: every Red
``Pose`` is the corresponding Blue ``Pose`` with ``x`` replaced by
``144 - x``, and heading reflected accordingly. Only Blue's coordinates are
listed below — read the corresponding ``RED_*`` constant as
``(144 - x, y, ...)``.

.. list-table:: Near-side route (used by ``AutoBlueNear15``)
   :header-rows: 1
   :widths: 30 15 15 15 25

   * - Constant
     - X
     - Y
     - Heading
     - Role
   * - ``BLUE_NER_START``
     - 20
     - 121
     - 135°
     - Starting pose
   * - ``BLUE_NER_SHOOT_0/1/2``
     - 55 / 50 / 55
     - 95 / 96 / 95
     - 140° / 180° / 180°
     - Shooting spots
   * - ``BLUE_NER_INTAKE_PRE_1/2/3``, ``BLUE_NER_INTAKE_1/2/3``
     - 49→13, 49→10, 49→10
     - 82, 59, 35
     - 180°
     - Approach + pickup for the three near game-piece stacks
   * - ``BLUE_NER_GATE``, ``BLUE_NER_GATE_MID``, ``BLUE_NER_GATE_MID_2``
     - 10 / 53 / 58
     - 65 / 64 / 60
     - 90° / — / —
     - Waypoints toward the human-player gate
   * - ``BLUE_NER_SUCK_MID``, ``BLUE_NER_SUCK_1/2/3``
     - 24, 10, 13, 10
     - 63, 57, 55, 52
     - — / 160°
     - Pickup near the gate
   * - ``BLUE_NER_PARK``
     - 33
     - 67
     - 90°
     - End-of-auto parking spot

.. list-table:: Far-side route (used by ``AutoBlueFar``)
   :header-rows: 1
   :widths: 30 15 15 15 25

   * - Constant
     - X
     - Y
     - Heading
     - Role
   * - ``BLUE_FAR_START``
     - 56
     - 7
     - 90°
     - Starting pose
   * - ``BLUE_FAR_SHOOT``
     - 63
     - 24
     - 90°
     - Single shooting spot, revisited each cycle
   * - ``BLUE_FAR_INTAKE_1/2/3/4``, ``BLUE_FAR_INTAKE_2_MID``
     - 11 / 19 / 12 / 12 / 24
     - 17 / 23 / 7 / 20 / 9
     - ~190-200°
     - Pickup spots for the far game-piece stack, visited across three
       intake cycles
   * - ``BLUE_FAR_PARK``
     - 35
     - 10
     - 90°
     - End-of-auto parking spot

``BLUE_MANUAL_POS`` / ``RED_MANUAL_POS`` are also defined here — see
``RobotConstants.MANUAL_POS`` above.

pedroPathing.Constants
-----------------------

``src/pedroPathing/Constants.java`` configures the Pedro Pathing
``Follower`` used for autonomous path following: robot mass, drivetrain
motor names/directions, wheel velocities, the localizer (a Pinpoint at the
same hardware name as ``Drivetrain``'s own copy), and the translational /
heading / drive PIDF loops that keep the robot on its planned path.

.. code-block:: java

   public static FollowerConstants followerConstants = new FollowerConstants()
           .mass(11.4)
           .forwardZeroPowerAcceleration(-31.82)
           .lateralZeroPowerAcceleration(-46.87)
           .translationalPIDFCoefficients(new PIDFCoefficients(0.1, 0.0, 0.008, 0))
           .headingPIDFCoefficients(new PIDFCoefficients(1.0, 0.0, 0.1, 0.0))
           .drivePIDFCoefficients(new FilteredPIDFCoefficients(0.008, 0.0, 0.0005, 0.6, 0.0))
           .centripetalScaling(0.0005);

``createFollower(HardwareMap)`` assembles these into a ``Follower`` via
``FollowerBuilder`` — this is what ``subsystems.Follower``'s constructor
calls.

``src/pedroPathing/Tuning.java`` is the Pedro Pathing library's own
selectable-OpMode tuning menu (localization, velocity, and PIDF tuners) —
it isn't team-specific code, and is used by driving the physical robot
through each tuner and reading the results back into the constants above.
