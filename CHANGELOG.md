# 1.1.4

  - Moved code responsible for running tests and watching tests to tasks.py.
    This tasks are now run using invoke.

# 1.1.3

  - Added `__repr__` method to `FigURI` for better printed messages

# 1.1.2

  - Removed unnecessary dependency on `watchdog`.

# 1.1.1

  - Added `watchdog` package as dependency. This is a temportary fix.

# 1.1.0

  - Instead of having single `port` property, now each container has `ports`
    list which is a list of all ports exposed by this container, sorted in
    ascending order. This way containers that expose more than one port can
    be handled properly.

# 1.0.1

  - Added `README.md`.
  - Added `CHANGELOG.md`.
  - Fixed repo url in `setup.py`.

