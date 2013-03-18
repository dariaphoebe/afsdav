lighttpd = lighttpd-trunk/src/lighttpd

all: lighttpd-trunk $(lighttpd)

lighttpd-trunk:
	mkdir lighttpd-trunk
	curl -L https://github.com/lighttpd/lighttpd1.4/tarball/lighttpd-1.5.x | tar -xz
	mv lighttpd-lighttpd1.4-*/* lighttpd-trunk/
	rm -rf lighttpd-lighttpd1.4-*
	patch -p0 < lighty-gssapi-r2854.patch
	patch -p0 < lighty-mod_magnet-r2854.patch
	patch -p0 < lighty-mod_proxy_core-r2505.patch

$(lighttpd):
	sudo yum -y install make gcc pkgconfig libtool patch pcre-devel libxml2-devel sqlite-devel lua-devel openssl-devel glib2-devel bzip2-devel libuuid-devel
	cd lighttpd-trunk; ./autogen.sh; ./configure --with-openssl --with-kerberos5 --with-bzip2 --with-lua --with-webdav-locks --with-webdav-props; make

clean:
	rm -rf lighttpd-trunk
