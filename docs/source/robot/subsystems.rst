Subsystems
==========

Robot
-----

``src/subsystems/Robot.java`` is the composition root. It owns one instance
each of ``Drivetrain``, ``Intake`` and ``Shooter``, and exposes two init
paths:

- ``init(hardwareMap)`` — used by TeleOp, initializes the drivetrain too.
- ``autoInit(hardwareMap)`` — used by autonomous, which manages driving
  through its own ``Follower``/Pedro Pathing instead of ``Drivetrain``, so
  it skips ``drivetrain.init()``.

Both paths start a 5-thread ``ScheduledExecutorService`` (currently unused
by any subsystem, reserved for future scheduled tasks) and eagerly touch
``FtcDashboard.getInstance()`` so the dashboard connection is live before
the match starts.

``getVoltage()`` returns the minimum reading across every voltage sensor on
the robot — a low-battery guard used for telemetry.

Drivetrain
----------

``src/subsystems/Drivetrain.java`` wraps four mecanum motors and a goBILDA
Pinpoint odometry computer, and exposes **four** different drive modes.
Every mode shares the same mecanum mixing formula, just fed different
``(power, turn, theta)`` inputs:

.. math::

   \text{sin} = \sin\left(\theta_{real} \cdot \frac{\pi}{180} - \frac{\pi}{4}\right)
   \qquad
   \text{cos} = \cos\left(\theta_{real} \cdot \frac{\pi}{180} - \frac{\pi}{4}\right)

.. math::

   lf = \frac{power \cdot \cos}{\max(|\sin|,|\cos|)} + turn
   \qquad
   rb = \frac{power \cdot \cos}{\max(|\sin|,|\cos|)} - turn

.. math::

   rf = \frac{power \cdot \sin}{\max(|\sin|,|\cos|)} - turn
   \qquad
   lb = \frac{power \cdot \sin}{\max(|\sin|,|\cos|)} + turn

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Method
     - Orientation
     - Notes
   * - ``drive(gamepad, powerScale)``
     - Robot-centric
     - Plain mecanum mix, no field heading involved. Used by ``AB_Tele``.
   * - ``driveFieldOriented(gamepad, p)``
     - Field-centric
     - ``realTheta`` derived from ``360 - currentHeading``. Declared but not
       currently used by any OpMode.
   * - ``driveConstantOriented(gamepad, chassisAutoAim)``
     - Field-centric, fixed zero
     - Adds input smoothing (``SMOOTHING_FACTOR = 0.95``) and an optional
       heading-lock PD controller (see below) that steers toward
       ``teleOpTargetX/Y`` when ``chassisAutoAim`` is true. Used by
       ``A_Tele``.
   * - ``driveWithSmartTracking(gamepad, shooter, cooperativeAimEnabled, autoAimActive)``
     - Field-centric, fixed zero
     - Delegates aiming to the turret first (``Shooter.smartTurretTracking``);
       only steers the chassis when the turret can't cover the required
       angle and cooperative aiming is enabled. Used by the ``AB_S_*``
       TeleOps.

Heading-lock PD controller
^^^^^^^^^^^^^^^^^^^^^^^^^^

Both ``driveConstantOriented`` and the cooperative-aim path in
``driveWithSmartTracking`` share the same PD loop
(``headingKp = 0.04``, ``headingKd = 0.004``) that turns the chassis to
face ``(teleOpTargetX, teleOpTargetY)``:

.. code-block:: java

   headingError = (currentHeading - targetHeading + 180) % 360 - 180; // wrap to [-180, 180]
   double proportional = headingKp * headingError;
   double derivative = headingKd * ((headingError - headingLastError) / deltaTime);
   turn += (proportional + derivative);

``fixedFieldHeading`` (default 0) is the zero-reference for field-oriented
driving; ``getHeading()`` / ``getPosition()`` read straight from the
Pinpoint.

Shooter
-------

``src/subsystems/Shooter.java`` (``@Configurable``) controls the flywheels,
ball gate, hood panel, and a two-servo turret.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Method(s)
     - Behavior
   * - ``setShooterVelocity(v)``
     - Applies ``RobotConstants.FAST_RECOVERY_P/I/D/F`` to both flywheel
       motors, then commands velocity ``v``. Coefficients are reapplied on
       every call — inexpensive on the Control Hub, and means Dashboard
       edits to the PIDF gains take effect immediately.
   * - ``openGate()`` / ``closeGate()`` / ``triggerFire()`` / ``triggerHold()``
     - The two gate servos move to fixed open/closed positions.
       ``triggerFire``/``triggerHold`` are just semantic aliases for
       ``openGate``/``closeGate``.
   * - ``panelTo(pos)``
     - Sets the hood/panel servo directly (0-1).
   * - ``turnTurretL/R(gamepad)``
     - Manual turret nudge, ±0.03 servo position per call.
   * - ``turnTurretToDeg(angle)`` / ``turnTurretToRad(radians)``
     - Absolute turret aim via ``angleToPos``/``radToPos``:
       ``pos = (50 - degrees) / 100``. Both turret servos are driven
       together (no left/right differential).
   * - ``smartTurretTracking(...)``
     - Auto-aim: computes the world bearing to
       ``(teleOpTargetX, teleOpTargetY)``, converts it to a turret-relative
       angle, and turns the turret if that angle is within the
       servos' ±50° range. Returns whether the turret alone can cover the
       target — the caller (``Drivetrain.driveWithSmartTracking``) falls
       back to chassis rotation when it can't.

.. mermaid::

   flowchart TD
       A["smartTurretTracking(heading, x, y, targetX, targetY)"] --> B{"< 100ms since\nlast update?"}
       B -- yes --> C["compute turretAngle only,\nreturn whether it's in ±50°"]
       B -- no --> D["compute turretAngle,\nrecord update time"]
       D --> E{"turretAngle in ±50°?"}
       E -- yes --> F["turnTurretToDeg(turretAngle)\nreturn true"]
       E -- no --> G["turnTurretToDeg(0)\nreturn false → chassis must help aim"]

The 100 ms throttle (``TURRET_UPDATE_INTERVAL_MS``) avoids commanding the
turret servos every single control loop tick.

Intake
------

``src/subsystems/Intake.java`` is a thin wrapper around one motor:
``intakeIn()`` (full power), ``intakeIn(p)`` (partial power, used while
firing so balls don't jam the gate), ``intakeShoot()`` (0.7 power variant
used by one TeleOp), ``intakeInAuto()`` (velocity-controlled, 1500 ticks/s,
used by autonomous), ``intakeOut()`` (reverse), and ``intakeStop()``.

Follower
--------

``src/subsystems/Follower.java`` wraps ``com.pedropathing.follower.Follower``
(built from :doc:`constants`'s ``pedroPathing.Constants``) as an FTCLib
``SubsystemBase``, so its ``periodic()`` — which calls ``follower.update()``
and pushes ``x``/``y``/``heading`` to telemetry — runs automatically once
registered with ``CommandScheduler``.

.. note::
   ``getInstance(hardwareMap, telemetry)`` always constructs a fresh
   ``Follower`` rather than returning a cached one; it's a convenience
   constructor, not a true singleton accessor. Each autonomous OpMode calls
   the regular constructor directly instead.

``followPath``, ``pathBuilder``, ``isBusy``, ``isRobotStuck`` and
``breakFollowing`` all delegate straight through to the underlying Pedro
Pathing ``Follower`` — this class exists mainly to make the dependency
FTCLib-command-friendly.

Drawing
-------

``src/subsystems/Drawing.java`` renders the robot's path and pose history to
FTC Dashboard / Panels' field view. ``drawDebug(follower)`` is called once
per autonomous loop tick and draws the currently-executing path (or path
chain), the robot's projected pose at its closest point on that path, and
its historical pose trail. Every drawing method is defensive against NaN
poses (e.g. before the Pinpoint has produced a first reading).
