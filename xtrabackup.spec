# TODO
# - which configure args should be set as mysql.spec?
Summary:	Open source backup tool for InnoDB and XtraDB
Name:		xtrabackup
Version:	0.3
Release:	0.1
License:	GPL v2
Group:		Applications/Databases
URL:		https://launchpad.net/percona-xtrabackup/
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	3400a3f671719206cba56b29255f70b1
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# CFLAGS for innodb are altered
%undefine	configure_cache

%description
OpenSource version of InnoDB backup with support of Percona
extensions.

%prep
%setup -q

%build
# The compiler flags are as per mysql "official" spec ;)
CXXFLAGS="%{rpmcflags} -felide-constructors -fno-rtti -fno-exceptions %{!?debug:-fomit-frame-pointer}"
CFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"

%configure
%{__make}
%{__make} -C innobase/xtrabackup

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
