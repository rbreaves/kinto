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

**Kinto Input Caret Status**
```
cat /tmp/kinto/caret
```

**Kinto Standard Log**
```
journalctl --user-unit=keyswap.service -b
```
**Kinto Debug Log (1.0.6-2+)**
```
systemctl --user stop keyswap
cd ~/.config/kinto
./kintox11 --debug
```

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Additional context**
Add any other context about the problem here.
