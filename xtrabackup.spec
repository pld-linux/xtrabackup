# NOTES
# - build instructions: http://www.percona.com/doc/percona-xtrabackup/2.2/installation/compiling_xtrabackup.html
# TODO
# - system zlib (seems unmodified)
# - BR deps (for libarchive, mysql builds)
Summary:	XtraBackup online backup for MySQL / InnoDB
Name:		xtrabackup
Version:	2.2.10
Release:	1
License:	GPL v2
Group:		Applications/Databases
Source0:	http://www.percona.com/downloads/XtraBackup/LATEST/source/tarball/percona-%{name}-%{version}.tar.gz
# Source0-md5:	81c70aeff37537331b3be0a0d408265a
URL:		http://www.percona.com/doc/percona-xtrabackup/
BuildRequires:	bash
BuildRequires:	cmake >= 2.6
BuildRequires:	libaio-devel
#BuildRequires:	libarchive-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel >= 4.2
#BuildRequires:	zlib-devel
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
%setup -q -n percona-%{name}-%{version}

%build
install -d build
cd build
%cmake \
	-DBUILD_CONFIG=xtrabackup_release \
	-DCMAKE_C_FLAGS_RELEASE="%{rpmcflags} -DNDEBUG -fno-omit-frame-pointer -fno-strict-aliasing" \
	-DCMAKE_CXX_FLAGS_RELEASE="%{rpmcxxflags} -DNDEBUG -fno-omit-frame-pointer -fno-strict-aliasing" \
	-DENABLE_DTRACE=OFF \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# TODO: find fix in make or cmake rules
install -d $RPM_BUILD_ROOT%{_mandir}
b=$(readlink -f %{_builddir})
mv $RPM_BUILD_ROOT$b/percona-xtrabackup-%{version}/build/man/man1 $RPM_BUILD_ROOT%{_mandir}

%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/xtrabackup-test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/innobackupex
%attr(755,root,root) %{_bindir}/xbcrypt
%attr(755,root,root) %{_bindir}/xbstream
%attr(755,root,root) %{_bindir}/xtrabackup
%{_mandir}/man1/innobackupex.1*
%{_mandir}/man1/xbcrypt.1*
%{_mandir}/man1/xbstream.1*
%{_mandir}/man1/xtrabackup.1*
