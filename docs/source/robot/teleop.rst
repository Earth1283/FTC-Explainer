TeleOp
======

``src/teleOp/`` holds seven driver-control OpModes. They range from a
minimal two-gamepad baseline to two-gamepad auto-aim variants split by
alliance. All of them poll ``gamepad1``/``gamepad2`` state directly inside
a ``while (opModeIsActive())`` loop — there's no command scheduler on the
TeleOp side.

.. list-table::
   :header-rows: 1
   :widths: 20 15 20 20 25

   * - OpMode
     - Gamepads
     - Drive mode
     - Aiming
     - Pose seed
   * - ``AB_Tele``
     - 1 + 2
     - ``drive()`` (robot-centric)
     - Manual turret nudge only
     - None (odometry not zeroed)
   * - ``A_Tele``
     - 1 only
     - ``driveConstantOriented()``
     - Heading-lock PD toward target when ``dpad_left`` held
     - From ``autoEndX/Y/H``
   * - ``Test``
     - 1 only
     - None (no drivetrain calls)
     - None — d-pad instead trims panel/velocity live
     - None
   * - ``AB_S_B_Tele``
     - 1 + 2
     - ``driveWithSmartTracking()``
     - Turret auto-aim + cooperative chassis assist; velocity/panel
       auto-computed from distance to target when aim is active
     - From ``autoEndX/Y/H``
   * - ``AB_S_B_Tele_2 (Linear)``
     - 1 + 2
     - ``driveWithSmartTracking()``
     - Same as above minus the distance-based velocity/panel calc
       (presets only)
     - Hardcoded Blue pose ``(144-8, 9, 90°)``
   * - ``AB_S_R_Tele``
     - 1 + 2
     - ``driveWithSmartTracking()``
     - Same as ``AB_S_B_Tele``, Red alliance targets
     - Hardcoded Red pose ``(8, 9, 90°)``
   * - ``AB_S_Tele``
     - 1 + 2
     - ``driveWithSmartTracking()``
     - Same as ``AB_S_B_Tele``, alliance-agnostic (reads whichever
       alliance's targets autonomous already set)
     - From ``autoEndX/Y/H``

``AB_S_Tele`` is effectively the alliance-agnostic successor to the two
``AB_S_B_Tele*``/``AB_S_R_Tele`` variants: because it seeds both its
starting pose and its target from state autonomous already wrote
(``autoEndX/Y/H`` and whichever of ``teleOpTargetXB/YB`` /
``teleOpTargetXR/YR`` the matching ``auto.*`` OpMode copied into
``teleOpTargetX/Y``), one build works after either alliance's autonomous
without picking a Blue- or Red-specific TeleOp.

Common gamepad map
-------------------

The four ``driveWithSmartTracking`` variants (``AB_S_B_Tele``,
``AB_S_B_Tele_2``, ``AB_S_R_Tele``, ``AB_S_Tele``) share one control
scheme:

.. tab-set::

   .. tab-item:: Gamepad 1 (driver)

      .. list-table::
         :header-rows: 1
         :widths: 30 70

         * - Input
           - Action
         * - Left stick / right stick X
           - Field-oriented drive / turn
         * - Left bumper
           - Hold to enable cooperative chassis aim assist
         * - Right trigger
           - Intake in + hold gate
         * - Left trigger
           - Intake out
         * - Right bumper
           - Fire (intake in + open gate)
         * - D-pad up
           - Reset odometry to ``MANUAL_POS``

   .. tab-item:: Gamepad 2 (operator)

      .. list-table::
         :header-rows: 1
         :widths: 30 70

         * - Input
           - Action
         * - X / Y / B
           - Select near-1 / near-2 / far shot preset (velocity + panel)
         * - Left trigger
           - Enable turret/chassis auto-aim
         * - D-pad left / right
           - Manual turret nudge (±0.03 servo position)
         * - D-pad up / down
           - Trim target velocity ±25
         * - Right bumper
           - Fire (intake in + open gate)
         * - A
           - Hold gate + intake in (feed without firing)

``AB_Tele`` and ``A_Tele`` use a reduced subset of the same bindings
(no smart-aim gamepad2 inputs); see each file directly for the exact
mapping. ``Test`` is a bring-up/tuning OpMode — its d-pad trims panel and
velocity live instead of switching between presets, useful for finding new
preset values to add to ``RobotConstants``.
