# TODO
# - which configure args should be set? same as mysql.spec?
Summary:	Open source backup tool for InnoDB and XtraDB
Name:		xtrabackup
Version:	0.7
Release:	0.2
License:	GPL v2
Group:		Applications/Databases
URL:		http://www.percona.com/docs/wiki/percona-xtrabackup:start
Source0:	http://ftp.gwdg.de/pub/misc/mysql/Downloads/MySQL-5.0/mysql-5.0.83.tar.gz
# Source0-md5:	051392064a1e32cca5c23a593908b10e
Source1:	xtrabackup.tar.bz2
# Source1-md5:	79ad151ec9055d30ee30d66993751f98
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# CFLAGS for innodb are altered
%undefine	configure_cache

%description
Percona XtraBackup is OpenSource online (non-blockable) backup
solution for InnoDB and XtraDB engines. It works with MySQL 5.0 and
5.1 versions (InnoDB Plugin is not supported yet as for alpha-0.3) and
also can handle MyISAM tables.

%prep
%setup -qc -a1
mv mysql-*/* .
%{__patch} -p1 < xtrabackup/fix_innodb_for_backup.patch
mv xtrabackup innobase

%build
# The compiler flags are as per mysql "official" spec ;)
CXXFLAGS="%{rpmcflags} -felide-constructors -fno-rtti -fno-exceptions %{!?debug:-fomit-frame-pointer}"
CFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"

%configure \
	--with-extra-charsets=all
%{__make}
%{__make} -C innobase/xtrabackup \
	CC="%{__cc}" \
	CXXFLAGS="$CFLAGS" \
	CFLAGS="$CFLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install innobase/xtrabackup/innobackupex-1.5.1 $RPM_BUILD_ROOT%{_bindir}/innobackupex
install innobase/xtrabackup/xtrabackup $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/innobackupex
%attr(755,root,root) %{_bindir}/xtrabackup
