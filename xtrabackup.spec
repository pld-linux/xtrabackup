# NOTES
# - build instructions: http://www.percona.com/doc/percona-xtrabackup/2.1/installation/compiling_xtrabackup.html
# TODO
# - system zlib (seems unmodified)
# - BR deps (for libarchive, mysql builds)
# - repackage tarball without:
# Percona-Server-5.1.73-rel14.11.tar.gz
# Percona-Server-5.5.35-rel33.0.tar.gz
# mysql-5.1.73.tar.gz
# mysql-5.5.35.tar.gz
# mysql-5.6.15.tar.gz
Summary:	XtraBackup online backup for MySQL / InnoDB
Name:		xtrabackup
Version:	2.1.8
Release:	0.2
License:	GPL v2
Group:		Applications/Databases
Source0:	http://www.percona.com/downloads/XtraBackup/XtraBackup-%{version}/source/percona-%{name}-%{version}.tar.gz
# NoSource0-md5:	c36df9d65e07b292e1e63372d8a4bdec
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
Percona XtraBackup is OpenSource online (non-blockable) backup
solution for InnoDB and XtraDB engines.

%prep
%setup -q -n percona-%{name}-%{version}

#mv mysql-5.5.* mysql-5.5
#cd mysql-5.5
#%{__patch} -p1 < ../patches/innodb55.patch

%build
# This BUILD section is expanded from './utils/build.sh innodb56' because we need to pass our own flags

./utils/build.sh innodb56

%if 0
# The compiler flags are as per mysql "official" spec ;)
export CC="%{__cc}"
export CXX="%{__cxx}"
export CXXFLAGS="%{rpmcflags} -felide-constructors -fno-rtti -fno-exceptions %{!?debug:-fomit-frame-pointer}"
export CFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"

cd mysql-5.5
# We need to build with partitioning due to MySQL bug #58632
%cmake \
	-DCMAKE_BUILD_TYPE=%{!?debug:RelWithDebInfo}%{?debug:Debug} \
	-DCMAKE_C_FLAGS_RELEASE="%{rpmcflags} -DNDEBUG -fno-omit-frame-pointer -fno-strict-aliasing" \
	-DCMAKE_CXX_FLAGS_RELEASE="%{rpmcxxflags} -DNDEBUG -fno-omit-frame-pointer -fno-strict-aliasing" \
	-DWITH_ZLIB=bundled \
	%{?with_system_zlib:-DWITH_ZLIB=system} \
	-DENABLED_LOCAL_INFILE=ON \
	-DWITH_INNOBASE_STORAGE_ENGINE=ON \
	-DWITH_PARTITION_STORAGE_ENGINE=ON \
	-DWITH_EXTRA_CHARSETS=all \
	-DENABLE_DTRACE=OFF \
	-DWITH_LIBEDIT=OFF \
	-DWITH_READLINE=OFF \
	-DCURSES_INCLUDE_PATH=/usr/include/ncurses \
	.

for dir in include strings mysys dbug extra storage/innobase; do
	%{__make} -C $dir
done

# build_libarchive()
cd ../src/libarchive
%cmake \
	-DENABLE_CPIO=OFF \
	-DENABLE_OPENSSL=OFF \
	-DENABLE_TAR=OFF \
	-DENABLE_TEST=OFF \
	.
%{__make}

# build_xtrabackup
cd ../..
# Read XTRABACKUP_VERSION from the VERSION file
. ./VERSION

server_dir=$(pwd)/mysql-5.5
xtrabackup_target=5.5
cd src

export LIBS="$LIBS -lrt"
%{__make} MYSQL_ROOT_DIR=$server_dir clean
%{__make} MYSQL_ROOT_DIR=$server_dir XTRABACKUP_VERSION=$XTRABACKUP_VERSION $xtrabackup_target
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install -p innobackupex $RPM_BUILD_ROOT%{_bindir}
install -p src/xbstream $RPM_BUILD_ROOT%{_bindir}
install -p src/xtrabackup_56 $RPM_BUILD_ROOT%{_bindir}
#cp -p doc/xtrabackup.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/innobackupex
%attr(755,root,root) %{_bindir}/xbstream
%attr(755,root,root) %{_bindir}/xtrabackup_56
#%{_mandir}/man1/xtrabackup.1*
