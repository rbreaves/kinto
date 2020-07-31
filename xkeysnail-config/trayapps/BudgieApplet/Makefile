#Just for building packages. (eopkg for solus)

DESTDIR ?=

INSTALLPATH ?= /usr/lib64/budgie-desktop/plugins

ICONPATH ?= /usr/share/icons/hicolor/scalable/apps

budgie-restart-applet:
	echo "Nothing to do"
install: budgie-restart-applet
	mkdir -p $(DESTDIR)$(INSTALLPATH)/org.budgie-desktop.applet.budgierestart
	mkdir -p $(DESTDIR)$(ICONPATH)
	#rm -f $(ICONDIR)/icon-theme.cache
	for file in BudgieRestart/*; \
	do \
		install -m 0755 "$$file" $(DESTDIR)$(INSTALLPATH)/org.budgie-desktop.applet.budgierestart/; \
	done
	for file in icons/*; \
	do \
		install -m 0755 "$$file" $(DESTDIR)$(ICONPATH)/; \
	done
