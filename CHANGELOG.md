# 1.1.0

  - Instead of having single `port` property, now each container has `ports`
    list which is a list of all ports exposed by this container, sorted in
    ascending order. This way containers that expose more than one port can
    be handled properly.

# 1.0.1

  - Added `README.md`.
  - Added `CHANGELOG.md`.
  - Fixed repo url in `setup.py`.

