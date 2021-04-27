# NOTES
# - build instructions: http://www.percona.com/doc/percona-xtrabackup/2.2/installation/compiling_xtrabackup.html
Summary:	XtraBackup online backup for MySQL / InnoDB
Name:		xtrabackup
Version:	2.4.20
Release:	1
License:	GPL v2
Group:		Applications/Databases
#Source0Download: https://github.com/percona/percona-xtrabackup/releases
Source0:	https://github.com/percona/percona-xtrabackup/archive/percona-%{name}-%{version}.tar.gz
# Source0-md5:	dfbd0310f1df084696fe16eea6efdc5d
Source1:	http://downloads.sourceforge.net/boost/boost_1_59_0.tar.bz2
# Source1-md5:	6aa9a5c6a4ca1016edd0ed1178e3cb87
URL:		https://www.percona.com/doc/percona-xtrabackup/
BuildRequires:	acl-devel
BuildRequires:	bash
BuildRequires:	bison >= 2
BuildRequires:	cmake >= 2.8.9
BuildRequires:	curl-devel
BuildRequires:	cyrus-sasl-devel
BuildRequires:	gnupg
BuildRequires:	libaio-devel
BuildRequires:	libarchive-devel
BuildRequires:	libatomic-devel
BuildRequires:	libedit-devel
BuildRequires:	libev-devel
BuildRequires:	libevent-devel >= 2
BuildRequires:	libgcrypt-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtirpc-devel >= 1.0
BuildRequires:	ncurses-devel >= 4.2
BuildRequires:	numactl-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel >= 2.5
BuildRequires:	python-modules
BuildRequires:	sphinx-pdg
BuildRequires:	systemd-units
BuildRequires:	xxd
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Percona XtraBackup is an open-source hot backup utility for
MySQL-based servers that doesn't lock your database during the backup.

It can back up data from InnoDB, XtraDB, and MyISAM tables on MySQL
5.1, 5.5 and 5.6 servers, as well as Percona Server with XtraDB.

Percona XtraBackup is a combination of the xtrabackup C program, and
the innobackupex Perl script. The xtrabackup program copies and
manipulates InnoDB and XtraDB data files, and the Perl script enables
enhanced functionality, such as interacting with a running MySQL
server and backing up MyISAM tables.

%prep
%setup -q -n percona-%{name}-percona-%{name}-%{version} -a1

# use system package
%{__mv} storage/innobase/xtrabackup/src/jsmn jsmn.dist
%{__mv} zlib zlib.dist

%build
install -d build
cd build
# ENABLE_OPENSSL is for internal libarchive to use MD5 implementation from (already used) openssl instad of additionally pulling libmd
%cmake \
	-DBUILD_CONFIG=xtrabackup_release \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DCMAKE_BUILD_TYPE=%{!?debug:RelWithDebInfo}%{?debug:Debug} \
	-DCMAKE_C_FLAGS_RELWITHDEBINFO="%{rpmcflags} -DNDEBUG -fno-omit-frame-pointer -fno-strict-aliasing" \
	-DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{rpmcxxflags} -DNDEBUG -fno-omit-frame-pointer -fno-strict-aliasing" \
	-DENABLE_DTRACE=OFF \
	-DENABLE_OPENSSL=ON \
	-DINSTALL_PLUGINDIR="%{_lib}/xtrabackup/plugins" \
	-DMYSQL_UNIX_ADDR=/var/lib/mysql/mysql.sock \
	-DWITH_BOOST="$(pwd)/$(ls -1d ../boost_*)" \
	-DWITH_CURL=system \
	-DWITH_EDITLINE=system \
	-DWITH_LIBEVENT=system \
	-DWITH_LZ4=system \
	-DWITH_PIC=ON \
	-DWITH_PROTOBUF=system \
	-DWITH_SASL=system \
	-DWITH_SSL=system \
	-DWITH_ZLIB=system \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# TODO: find fix in cmake rules (storage/innobase/xtrabackup/doc/source/CMakeLists.txt)
install -d $RPM_BUILD_ROOT%{_mandir}
b=$(readlink -f %{_builddir}/percona-%{name}-percona-%{name}-%{version})
%{__mv} $RPM_BUILD_ROOT$b/build/man/man1 $RPM_BUILD_ROOT%{_mandir}

%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/xtrabackup-test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/innobackupex
%attr(755,root,root) %{_bindir}/xbcloud
%attr(755,root,root) %{_bindir}/xbcloud_osenv
%attr(755,root,root) %{_bindir}/xbcrypt
%attr(755,root,root) %{_bindir}/xbstream
%attr(755,root,root) %{_bindir}/xtrabackup
%{_mandir}/man1/innobackupex.1*
%{_mandir}/man1/xbcrypt.1*
%{_mandir}/man1/xbstream.1*
%{_mandir}/man1/xtrabackup.1*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/keyring_file.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/keyring_vault.so
