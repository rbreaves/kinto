---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: rbreaves

---

**Install Type:** Bare Metal or VM
**Distro:** Name + Version
**DE:** Gnome, XFCE, KDE
**Branch:** master, dev
**Commit:** git rev-parse --short HEAD

If applicable include kinto log and the status of your input caret
```
cat /tmp/kinto/caret
journalctl --user-unit=keyswap.service -b
```

**Describe the bug**
A clear and concise description of what the bug is.

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Additional context**
Add any other context about the problem here.
