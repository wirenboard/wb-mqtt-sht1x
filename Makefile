LIB_LOCATION=/usr/lib/wb-mqtt-sht1x
.PHONY: all clean

all:
clean :

install: all
	install -m 0755 sht1x.py  $(DESTDIR)/$(LIB_LOCATION)
	install -m 0755 wb-mqtt-sht1x.py  $(DESTDIR)/$(LIB_LOCATION)

	install -m 0644 wb-mqtt-sht1x.conf  $(DESTDIR)/etc/

	ln -s $(LIB_LOCATION)/wb-mqtt-sht1x.py $(DESTDIR)/usr/bin/wb-mqtt-sht1x
	ln -s $(LIB_LOCATION)/sht1x.py $(DESTDIR)/usr/bin/sht1x





