Shooter PIDF Tuning
====================

This is an English write-up of ``src/ShooterPIDF_Guide.md`` (original in
Chinese), covering why the flywheel needs velocity PIDF tuning and how to
do it against the current codebase.

Background
----------

During continuous fire in autonomous, flywheel RPM drops when a ball
transfers momentum to it on the way out, and if the next ball fires before
RPM recovers, that shot comes out weak. The fix is tuning the flywheel's
velocity PIDF loop (``Shooter.setShooterVelocity``, see :doc:`subsystems`)
so it recovers fast enough between shots.

What each term does
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Term
     - Effect
   * - **P** (Proportional)
     - Reacts to the current velocity error. Higher P = faster reaction,
       but too high causes oscillation.
   * - **I** (Integral)
     - Eliminates steady-state error. Higher I recovers lost RPM faster,
       but too high causes overshoot.
   * - **D** (Derivative)
     - Damps oscillation. Higher D smooths overshoot, but too high makes
       the response sluggish.
   * - **F** (Feedforward)
     - Base power for the target velocity, applied before P/I/D correct
       anything.

Current live values
--------------------

These are set in ``src/constants/RobotConstants.java`` and applied on
every ``setShooterVelocity()`` call, so editing them via FTC
Dashboard/Panels takes effect immediately with no redeploy:

.. code-block:: java

   public static volatile double FAST_RECOVERY_P = 50.0;
   public static volatile double FAST_RECOVERY_I = 0.1;
   public static volatile double FAST_RECOVERY_D = 1;
   public static volatile double FAST_RECOVERY_F = 11.7;

.. note::
   The original guide's example config (``P=22, I=6, D=2.5, F=0.25``) and
   its suggested tuning ranges below predate these values and a
   ``FAST_RECOVERY_F`` scale change — treat the ranges as a starting
   point, not a target to converge back to.

.. important::
   The guide also references two dedicated OpModes —
   *Shooter Continuous Fire Test* and *Shooter PIDF Tuner* — that aren't
   present in the current ``src/teleOp/`` tree. Until they're rebuilt,
   tune by editing ``FAST_RECOVERY_P/I/D/F`` live via FTC Dashboard/Panels
   while running any TeleOp (or ``Test``, whose d-pad also trims target
   velocity directly — see :doc:`teleop`) and firing repeated shots.

Tuning workflow
----------------

1. **Baseline** — run repeated shots with the current gains and note RPM
   drop per shot and recovery time.
2. **Tune P first** — increase if RPM drops too much, decrease if it
   oscillates. Reasonable range: 15.0 - 30.0 (adjust upward from this if the
   flywheel is heavier/faster than the guide's original setup).
3. **Then I** — increase if recovery is slow, decrease if it overshoots.
   Range: 3.0 - 10.0.
4. **Then D** — increase if oscillating, decrease if response is too slow.
   Range: 1.0 - 4.0.
5. **Then F** — sets the base power for target velocity. Range: 0.1 - 0.4
   (scale this against the current ``F=11.7`` baseline, not the guide's
   original ``F=0.25`` — the working range depends on the flywheel's
   velocity units/gearing).
6. **Re-verify**, then confirm against real shots in an actual autonomous
   run — battery voltage affects flywheel recovery too.

Performance targets
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Rating
     - RPM drop per shot
     - Recovery time
     - Stability across a burst
   * - Good
     - < 15%
     - < 1.5 s
     - > 90%
   * - Acceptable
     - < 20%
     - < 2 s
     - > 85%
   * - Needs tuning
     - > 25%
     - > 2.5 s
     - < 80%, or visible oscillation

Adjustment cheatsheet
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Symptom
     - Adjustment
   * - RPM drop too large
     - P +3~5, I +1~2, F +0.05 (scaled to current F)
   * - Recovery too slow
     - P +2~4, I +0.5~1
   * - Oscillation
     - D +0.5~1, P -2~3, I -0.5~1
   * - Response too sluggish
     - P +3~5, D -0.5~1

Once satisfied, write the final values back into
``RobotConstants.FAST_RECOVERY_P/I/D/F`` — Dashboard edits are only live
for the current run and reset to the source values on redeploy/restart.
Autonomous automatically benefits since it calls the same
``Shooter.setShooterVelocity()`` path — no separate tuning is needed there.
