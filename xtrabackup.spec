Summary:	Open source backup tool for InnoDB and XtraDB
Name:		xtrabackup
Version:	0
Release:	0.1
License:	GPL v2
Group:		Applications/Databases
URL:		https://launchpad.net/percona-xtrabackup/
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenSource version of InnoDB backup with support of Percona
extensions.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
