Commands
========

DrivePointToPoint
------------------

``src/commands/DrivePointToPoint.java`` is an FTCLib ``CommandBase`` that
drives the ``Follower`` subsystem from a start ``Pose`` to an end ``Pose``,
optionally through one or two midpoints. It's the only building block every
autonomous routine uses to move.

Constructor overloads pick the path shape by point count:

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Constructor
     - Points
     - Path built
   * - ``(follower, start, end)``
     - 2
     - ``BezierLine`` (straight line)
   * - ``(follower, start, end, power)``
     - 2
     - Same, with an explicit max power (default is 1.0)
   * - ``(follower, start, mid1, end)``
     - 3
     - ``BezierCurve`` through one control point
   * - ``(follower, start, mid1, mid2, end)``
     - 4
     - ``BezierCurve`` through two control points

Heading is always linearly interpolated between the start and end pose's
heading, regardless of path shape. ``setHoldEnd(true)`` and
``setBreaking(strength)`` are fluent setters that must be called before the
command is scheduled — ``initialize()`` reads them once when the path is
built.

.. mermaid::

   flowchart LR
       Init["initialize()\nbuild PathBuilder from\nstart/mid(s)/end\nfollower.followPath(...)"]
       Exec["execute()\n(no-op — Follower's own\nperiodic() drives it)"]
       Done{"isFinished()?\n!follower.isBusy()\n|| follower.isRobotStuck()"}
       End["end(interrupted)\n(no-op)"]

       Init --> Exec --> Done
       Done -- no --> Exec
       Done -- yes --> End

Because ``isFinished()`` also returns true when ``isRobotStuck()`` is
true, a command sequence won't stall forever if the robot physically can't
reach a waypoint (e.g. pinned against another robot) — it just moves on to
the next command, slightly off-target.
