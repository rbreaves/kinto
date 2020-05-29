---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: rbreaves

---

**Describe the bug**
A clear and concise description of what the bug is.

**Expected behavior**
A clear and concise description of what you expected to happen.

**Install Type:** Bare Metal or VM
**Distro:** Name + Version
**DE:** Gnome, XFCE, KDE
**Branch:** master, dev
**Commit:** git rev-parse --short HEAD

Logs and status if relevant
```
# xkeysnail
sudo systemctl status xkeysnail
sudo journalctl --unit=xkeysnail.service -b

# xkb
systemctl --user status keyswap
journalctl --user-unit=keyswap.service -b
```

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Additional context**
Add any other context about the problem here.
