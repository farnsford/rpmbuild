# These are macros to be used with find_lang and other stuff
%global sname postgresql
%global pgmajorversion 96
%global prevmajorversion 9.5
%global pgpackageversion 9.6
%global pginstdir /usr/pgsql-%{pgpackageversion}


%global beta 0
%{?beta:%global __os_install_post /usr/lib/rpm/brp-compress}

# Macros that define the configure parameters:
%{!?kerbdir:%global kerbdir "/usr"}
%{!?disablepgfts:%global disablepgfts 0}
%if 0%{?rhel}
%{!?enabletaptests:%global enabletaptests 0}
%else
%{!?enabletaptests:%global enabletaptests 1}
%endif
%{!?intdatetimes:%global intdatetimes 1}
%{!?kerberos:%global kerberos 1}
%{!?ldap:%global ldap 1}
%{!?nls:%global nls 1}
%{!?pam:%global pam 1}
%{!?plpython:%global plpython 1}

%if 0%{?rhel} && 0%{?rhel} <= 7
# RHEL 6 and 7 does not have Python 3
%{!?plpython3:%global plpython3 0}
%endif

%if 0%{?fedora} > 23
# All Fedora releases now use Python3
%{!?plpython3:%global plpython3 1}
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
# Disable PL/Python 3 on SLES 12
%{!?plpython3:%global plpython3 0}
%endif
%endif

%{!?pltcl:%global pltcl 1}
%{!?plperl:%global plperl 1}
%{!?ssl:%global ssl 1}
%{!?test:%global test 1}
%{!?runselftest:%global runselftest 0}
%{!?uuid:%global uuid 1}
%{!?xml:%global xml 1}
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?systemd_enabled:%global systemd_enabled 0}
%{!?sdt:%global sdt 0}
%{!?selinux:%global selinux 0}
%else
%{!?systemd_enabled:%global systemd_enabled 1}
%ifarch ppc64 ppc64le
%{!?sdt:%global sdt 0}
%else
%{!?sdt:%global sdt 1}
%endif
%{!?selinux:%global selinux 1}
%endif
%if 0%{?fedora} > 23
%global _hardened_build 1
%endif

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL client programs and libraries
Name:		%{sname}%{pgmajorversion}
Version:	9.6.5
Release:	2PGDG%{?dist}
License:	PostgreSQL
Group:		Applications/Databases
Url:		https://www.postgresql.org/

Source0:	https://download.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.gz
Source4:	%{sname}-%{pgmajorversion}-Makefile.regress
Source5:	%{sname}-%{pgmajorversion}-pg_config.h
%if %{systemd_enabled}
Source6:	%{sname}-%{pgmajorversion}-README-systemd.rpm-dist
%else
Source6:	%{sname}-%{pgmajorversion}-README-init.rpm-dist
%endif
Source7:	%{sname}-%{pgmajorversion}-ecpg_config.h
Source9:	%{sname}-%{pgmajorversion}-libs.conf
Source12:	https://www.postgresql.org/files/documentation/pdf/%{pgpackageversion}/%{sname}-%{pgpackageversion}-A4.pdf
Source14:	%{sname}-%{pgmajorversion}.pam
Source16:	%{sname}-%{pgmajorversion}-filter-requires-perl-Pg.sh
Source17:	%{sname}-%{pgmajorversion}-setup
%if %{systemd_enabled}
Source10:	%{sname}-%{pgmajorversion}-check-db-dir
Source18:	%{sname}-%{pgmajorversion}.service
Source19:	%{sname}-%{pgmajorversion}-tmpfiles.d
%else
Source3:	%{sname}-%{pgmajorversion}.init
%endif

Patch10:         00004-postgresql-1c-9.6.patch
Patch1:		%{sname}-%{pgmajorversion}-rpm-pgsql.patch
Patch3:		%{sname}-%{pgmajorversion}-logging.patch
Patch5:		%{sname}-%{pgmajorversion}-var-run-socket.patch
Patch6:		%{sname}-%{pgmajorversion}-perl-rpath.patch
Patch7:         00001-1c_FULL_96-0.23.patch
Patch8:         00002-online_analyze.patch
Patch9:         00003-plantuner.patch
Patch11:         00005-exists_opt-2.patch
Patch12:         00006-coalesce_cost-1.patch

BuildRequires:	perl glibc-devel bison flex >= 2.5.31
BuildRequires:	perl(ExtUtils::MakeMaker)

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

Requires:	/sbin/ldconfig

%if %plperl
%if 0%{?rhel} && 0%{?rhel} >= 7
BuildRequires:	perl-ExtUtils-Embed
%endif
%if 0%{?fedora} >= 22
BuildRequires:	perl-ExtUtils-Embed
%endif
%endif

%if %plpython
BuildRequires:	python-devel
%endif

#%if %plpython3
#BuildRequires: python3-devel
#%endif

%if %pltcl
BuildRequires:	tcl-devel
%endif

BuildRequires:	readline-devel
BuildRequires:	zlib-devel >= 1.0.4

%if %ssl
# We depend un the SSL libraries provided by Advance Toolchain on PPC,
# so use openssl-devel only on other platforms:
%ifnarch ppc64 ppc64le
BuildRequires:	openssl-devel
%endif
%endif

%if %kerberos
BuildRequires:	krb5-devel
BuildRequires:	e2fsprogs-devel
%endif

%if %nls
BuildRequires:	gettext >= 0.10.35
%endif

%if %xml
BuildRequires:	libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires:	pam-devel
%endif

%if %sdt
BuildRequires:	systemtap-sdt-devel
%endif

%if %uuid
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	uuid-devel
%endif
%else
BuildRequires:	libuuid-devel
%endif
%endif

%if %ldap
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	openldap2-devel
%endif
%else
BuildRequires:	openldap-devel
%endif
%endif

%if %selinux
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	libselinux-devel >= 2.0.93
%endif
%else
BuildRequires:	libselinux-devel >= 2.0.93
%endif
BuildRequires:	selinux-policy >= 3.9.13
%endif

%if %{systemd_enabled}
BuildRequires:		systemd, systemd-devel
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires(post):		systemd-sysvinit
%endif
%else
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif
%else
Requires(post):		chkconfig
Requires(preun):	chkconfig
# This is for /sbin/service
Requires(preun):	initscripts
Requires(postun):	initscripts
%endif

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:	postgresql

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The base postgresql package contains the client programs that you'll need to
access a PostgreSQL DBMS server, as well as HTML documentation for the whole
system.  These client programs can be located on the same machine as the
PostgreSQL server, or on a remote machine that accesses a PostgreSQL server
over a network connection.  The PostgreSQL server can be found in the
postgresql%{pgmajorversion}-server sub-package.

If you want to manipulate a PostgreSQL database on a local or remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql%{pgmajorversion}-server package.

%package libs
Summary:	The shared libraries required for any PostgreSQL clients
Group:		Applications/Databases
Provides:	postgresql-libs = %{pgpackageversion}

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description libs
The postgresql%{pgmajorversion}-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary:	The programs needed to create and run a PostgreSQL server
Group:		Applications/Databases
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):	/usr/sbin/useradd /usr/sbin/groupadd
# for /sbin/ldconfig
Requires(post):		glibc
Requires(postun):	glibc
%if %{systemd_enabled}
# pre/post stuff needs systemd too

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires(post):		systemd
%endif
%else
Requires(post):		systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units
%endif
%else
Requires:	/usr/sbin/useradd, /sbin/chkconfig
%endif
Provides:	postgresql-server

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description server
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The postgresql%{pgmajorversion}-server package contains the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.

%package docs
Summary:	Extra documentation for PostgreSQL
Group:		Applications/Databases
Provides:	postgresql-docs

%description docs
The postgresql%{pgmajorversion}-docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation. This package also
includes HTML version of the documentation.

%package contrib
Summary:	Contributed source and binaries distributed with PostgreSQL
Group:		Applications/Databases
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Provides:	postgresql-contrib

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description contrib
The postgresql%{pgmajorversion}-contrib package contains various extension modules that are
included in the PostgreSQL distribution.

%package devel
Summary:	PostgreSQL development header files and libraries
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
%if %enabletaptests
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires:	perl-IPC-Run3
%endif
%else
Requires:	perl-IPC-Run
%endif
Requires:	perl-Test-Simple
%endif
Provides:	postgresql-devel

%description devel
The postgresql%{pgmajorversion}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server.  It also contains the ecpg
Embedded C Postgres preprocessor. You need to install this package if you want
to develop applications which will interact with a PostgreSQL server.

%if %plperl
%package plperl
Summary:	The Perl procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%ifarch ppc ppc64
BuildRequires:	perl-devel
%endif
Obsoletes:	postgresql%{pgmajorversion}-pl
Provides:	postgresql-plperl

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description plperl
The postgresql%{pgmajorversion}-plperl package contains the PL/Perl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Perl.

%endif

%if %plpython
%package plpython
Summary:	The Python procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Obsoletes:	%{name}-pl
Provides:	postgresql-plpython

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description plpython
The postgresql%{pgmajorversion}-plpython package contains the PL/Python procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python.

%endif

#%if %plpython3
#%package plpython3
#Summary:	The Python3 procedural language for PostgreSQL
#Group:		Applications/Databases
#Requires:	%{name}%{?_isa} = %{version}-%{release}
#Requires:	%{name}-server%{?_isa} = %{version}-%{release}
#Obsoletes:	%{name}-pl
#Provides:	postgresql-plpython3
#
#%ifarch ppc64 ppc64le
#AutoReq:	0
#3Requires:	advance-toolchain-%{atstring}-runtime
#%endif

#%description plpython3
#The postgresql%{pgmajorversion}-plpython3 package contains the PL/Python3 procedural language,
#which is an extension to the PostgreSQL database server.
#Install this if you want to write database functions in Python 3.
#
#%endif

%if %pltcl
%package pltcl
Summary:	The Tcl procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	tcl
Obsoletes:	%{name}-pl
Provides:	postgresql-pltcl

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system. The %{name}-pltcl package contains the PL/Tcl language
for the backend.
%endif

%if %test
%package test
Summary:	The test suite distributed with PostgreSQL
Group:		Applications/Databases
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Provides:	postgresql-test

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description test
The postgresql%{pgmajorversion}-test package contains files needed for various tests for the
PostgreSQL database management system, including regression tests and
benchmarks.
%endif

%global __perl_requires %{SOURCE16}

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p1
%patch3 -p1
%patch5 -p0
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%{__cp} -p %{SOURCE12} .

%build

# fail quickly and obviously if user tries to build as root
%if %runselftest
	if [ x"`id -u`" = x0 ]; then
		echo "postgresql's regression tests fail if run as root."
		echo "If you really need to build the RPM as root, use"
		echo "--define='runselftest 0' to skip the regression tests."
		exit 1
	fi
%endif

CFLAGS="${CFLAGS:-%optflags}"
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%else
	# Strip out -ffast-math from CFLAGS....
	CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
	%if 0%{?rhel}
		LDFLAGS="-Wl,--as-needed"; export LDFLAGS
	%endif
%endif

export CFLAGS

# plpython requires separate configure/build runs to build against python 2
# versus python 3.  Our strategy is to do the python 3 run first, then make
# distclean and do it again for the "normal" build.  Note that the installed
# Makefile.global will reflect the python 2 build, which seems appropriate
# since that's still considered the default plpython version.

unset PYTHON

# Normal (not python3) build begins here
./configure --enable-rpath \
	--prefix=%{pginstdir} \
	--includedir=%{pginstdir}/include \
	--mandir=%{pginstdir}/share/man \
	--datadir=%{pginstdir}/share \
	--libdir=%{pginstdir}/lib \
	--without-openssl \
	--without-ldap \
	--without-selinux \
	--with-blocksize=4 \
	--with-wal-blocksize=4 \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %enabletaptests
	--enable-tap-tests \
%endif
%if %plperl
	--with-perl \
%endif
%if %plpython
	--with-python \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	--with-gssapi \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
	--enable-nls \
%endif
%if %sdt
	--enable-dtrace \
%endif
%if !%intdatetimes
	--disable-integer-datetimes \
%endif
%if %disablepgfts
	--disable-thread-safety \
%endif
%if %uuid
	--with-uuid=e2fs \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
%if %{systemd_enabled}
	--with-systemd \
%endif
%ifarch ppc64 ppc64le
	--with-includes=%{atpath}/include \
	--with-libraries=%{atpath}/lib64 \
%endif
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/pgsql \
	--docdir=%{pginstdir}/doc \
	--htmldir=%{pginstdir}/doc/html

make %{?_smp_mflags} all
make %{?_smp_mflags} -C contrib all
%if %uuid
make %{?_smp_mflags} -C contrib/uuid-ossp all
%endif

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{pginstdir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
make %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
%{__rm} -f src/tutorial/GNUmakefile


# run_testsuite WHERE
# -------------------
# Run 'make check' in WHERE path.  When that command fails, return the logs
# given by PostgreSQL build system and set 'test_failure=1'.

run_testsuite()
{
	make -C "$1" MAX_CONNECTIONS=5 check && return 0

	test_failure=1

	(
		set +x
		echo "=== trying to find all regression.diffs files in build directory ==="
		find -name 'regression.diffs' | \
		while read line; do
			echo "=== make failure: $line ==="
			cat "$line"
		done
	)
}

%if %runselftest
	run_testsuite "src/test/regress"
	make clean -C "src/test/regress"
	run_testsuite "src/pl"
%if %plpython3
	# must install Makefile.global that selects python3
	%{__mv} src/Makefile.global src/Makefile.global.save
	%{__cp} src/Makefile.global.python3 src/Makefile.global
	touch -r src/Makefile.global.save src/Makefile.global
	# because "make check" does "make install" on the whole tree,
	# we must temporarily install plpython3 as src/pl/plpython,
	# since that is the subdirectory src/pl/Makefile knows about
	%{__mv} src/pl/plpython src/pl/plpython2
	%{__mv} src/pl/plpython3 src/pl/plpython

	run_testsuite "src/pl/plpython"

	# and clean up our mess
	%{__mv} src/pl/plpython src/pl/plpython3
	%{__mv} src/pl/plpython2 src/pl/plpython
	%{__mv} -f src/Makefile.global.save src/Makefile.global
%endif
	run_testsuite "contrib"
%endif

%if %test
	pushd src/test/regress
	make all
	popd
%endif

%install
%{__rm} -rf %{buildroot}

make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{pginstdir}/share/extensions/
make -C contrib DESTDIR=%{buildroot} install
%if %uuid
make -C contrib/uuid-ossp DESTDIR=%{buildroot} install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case $(uname -i) in
	i386 | x86_64 | ppc | ppc64 | s390 | s390x)
		%{__mv} %{buildroot}%{pginstdir}/include/pg_config.h %{buildroot}%{pginstdir}/include/pg_config_$(uname -i).h
		install -m 644 %{SOURCE5} %{buildroot}%{pginstdir}/include/pg_config.h
		%{__mv} %{buildroot}%{pginstdir}/include/server/pg_config.h %{buildroot}%{pginstdir}/include/server/pg_config_$(uname -i).h
		install -m 644 %{SOURCE5} %{buildroot}%{pginstdir}/include/server/pg_config.h
		%{__mv} %{buildroot}%{pginstdir}/include/ecpg_config.h %{buildroot}%{pginstdir}/include/ecpg_config_$(uname -i).h
		install -m 644 %{SOURCE7} %{buildroot}%{pginstdir}/include/ecpg_config.h
		;;
	*)
	;;
esac

# This is only for systemd supported distros:
%if %{systemd_enabled}
# prep the setup script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{version}|' \
	-e 's|^PGENGINE=.*$|PGENGINE=%{pginstdir}/bin|' \
	<%{SOURCE17} >postgresql%{pgmajorversion}-setup
install -m 755 postgresql%{pgmajorversion}-setup %{buildroot}%{pginstdir}/bin/postgresql%{pgmajorversion}-setup

# prep the startup check script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{version}|' \
	-e 's|^PREVMAJORVERSION=.*$|PREVMAJORVERSION=%{prevmajorversion}|' \
	-e 's|^PGDOCDIR=.*$|PGDOCDIR=%{_pkgdocdir}|' \
	<%{SOURCE10} >postgresql%{pgmajorversion}-check-db-dir
touch -r %{SOURCE10} postgresql%{pgmajorversion}-check-db-dir
install -m 755 postgresql%{pgmajorversion}-check-db-dir %{buildroot}%{pginstdir}/bin/postgresql%{pgmajorversion}-check-db-dir

install -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/postgresql-%{pgpackageversion}.service
%else
install -d %{buildroot}%{_initrddir}
sed 's/^PGVERSION=.*$/PGVERSION=%{version}/' <%{SOURCE3} > postgresql.init
install -m 755 postgresql.init %{buildroot}%{_initrddir}/postgresql-%{pgpackageversion}
%endif

%if %pam
install -d %{buildroot}/etc/pam.d
install -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/%{sname}
%endif

# Create the directory for sockets.
install -d -m 755 %{buildroot}/var/run/postgresql
%if %{systemd_enabled}
# ... and make a tmpfiles script to recreate it at reboot.
mkdir -p %{buildroot}/%{_tmpfilesdir}
install -m 0644 %{SOURCE19} %{buildroot}/%{_tmpfilesdir}/postgresql-%{pgpackageversion}.conf
%endif

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/pgsql/%{pgpackageversion}/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/pgsql/%{pgpackageversion}/backups

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/pgsql/%{pgpackageversion}

# Install linker conf file under postgresql installation directory.
# We will install the latest version via alternatives.
install -d -m 755 %{buildroot}%{pginstdir}/share/
install -m 700 %{SOURCE9} %{buildroot}%{pginstdir}/share/%{sname}-%{pgpackageversion}-libs.conf

%if %test
	# tests. There are many files included here that are unnecessary,
	# but include them anyway for completeness.  We replace the original
	# Makefiles, however.
	mkdir -p %{buildroot}%{pginstdir}/lib/test
	%{__cp} -a src/test/regress %{buildroot}%{pginstdir}/lib/test
	install -m 0755 contrib/spi/refint.so %{buildroot}%{pginstdir}/lib/test/regress
	install -m 0755 contrib/spi/autoinc.so %{buildroot}%{pginstdir}/lib/test/regress
	pushd  %{buildroot}%{pginstdir}/lib/test/regress
	strip *.so
	%{__rm} -f GNUmakefile Makefile *.o
	chmod 0755 pg_regress regress.so
	popd
	%{__cp} %{SOURCE4} %{buildroot}%{pginstdir}/lib/test/regress/Makefile
	chmod 0644 %{buildroot}%{pginstdir}/lib/test/regress/Makefile
%endif

# Fix some more documentation
# gzip doc/internals.ps
%{__cp} %{SOURCE6} README.rpm-dist
mkdir -p %{buildroot}%{pginstdir}/share/doc/html
%{__mv} doc/src/sgml/html doc
mkdir -p %{buildroot}%{pginstdir}/share/man/
%{__mv} doc/src/sgml/man1 doc/src/sgml/man3 doc/src/sgml/man7  %{buildroot}%{pginstdir}/share/man/
%{__rm} -rf %{buildroot}%{_docdir}/pgsql

# initialize file lists
%{__cp} /dev/null main.lst
%{__cp} /dev/null libs.lst
%{__cp} /dev/null server.lst
%{__cp} /dev/null devel.lst
%{__cp} /dev/null plperl.lst
%{__cp} /dev/null pltcl.lst
%{__cp} /dev/null plpython.lst
%{__cp} /dev/null pg_plpython3.lst

%if %nls
%find_lang ecpg-%{pgpackageversion}
%find_lang ecpglib6-%{pgpackageversion}
%find_lang initdb-%{pgpackageversion}
%find_lang libpq5-%{pgpackageversion}
%find_lang pg_basebackup-%{pgpackageversion}
%find_lang pg_config-%{pgpackageversion}
%find_lang pg_controldata-%{pgpackageversion}
%find_lang pg_ctl-%{pgpackageversion}
%find_lang pg_dump-%{pgpackageversion}
%find_lang pg_resetxlog-%{pgpackageversion}
%find_lang pg_rewind-%{pgpackageversion}
%find_lang pgscripts-%{pgpackageversion}
%if %plperl
%find_lang plperl-%{pgpackageversion}
cat plperl-%{pgpackageversion}.lang > pg_plperl.lst
%endif
%find_lang plpgsql-%{pgpackageversion}
%if %plpython
%find_lang plpython-%{pgpackageversion}
cat plpython-%{pgpackageversion}.lang > pg_plpython.lst
%endif

%if %pltcl
%find_lang pltcl-%{pgpackageversion}
cat pltcl-%{pgpackageversion}.lang > pg_pltcl.lst
%endif
%find_lang postgres-%{pgpackageversion}
%find_lang psql-%{pgpackageversion}

cat libpq5-%{pgpackageversion}.lang > pg_libpq5.lst
cat pg_config-%{pgpackageversion}.lang ecpg-%{pgpackageversion}.lang ecpglib6-%{pgpackageversion}.lang > pg_devel.lst
cat initdb-%{pgpackageversion}.lang pg_ctl-%{pgpackageversion}.lang psql-%{pgpackageversion}.lang pg_dump-%{pgpackageversion}.lang pg_basebackup-%{pgpackageversion}.lang pg_rewind-%{pgpackageversion}.lang pgscripts-%{pgpackageversion}.lang > pg_main.lst
cat postgres-%{pgpackageversion}.lang pg_resetxlog-%{pgpackageversion}.lang pg_controldata-%{pgpackageversion}.lang plpgsql-%{pgpackageversion}.lang > pg_server.lst
%endif

%pre server
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post server
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
 %if %{systemd_enabled}
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
   %if 0%{?suse_version} >= 1315
   %service_add_pre %{sname}-%{pgpackageversion}.service
   %endif
   %else
   %systemd_post %{sname}-%{pgpackageversion}.service
   %tmpfiles_create
   %endif
  %else
   chkconfig --add %{sname}-%{pgpackageversion}
  %endif
fi

# postgres' .bash_profile.
# We now don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
# so that package manager will be happy during upgrade to new major version.
echo "[ -f /etc/profile ] && source /etc/profile
PGDATA=/var/lib/pgsql/%{pgpackageversion}/data
export PGDATA
# If you want to customize your settings,
# Use the file below. This is not overridden
# by the RPMS.
[ -f /var/lib/pgsql/.pgsql_profile ] && source /var/lib/pgsql/.pgsql_profile" > /var/lib/pgsql/.bash_profile
chown postgres: /var/lib/pgsql/.bash_profile
chmod 700 /var/lib/pgsql/.bash_profile

%preun server
if [ $1 -eq 0 ] ; then
%if %{systemd_enabled}
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable postgresql-%{pgpackageversion}.service >/dev/null 2>&1 || :
	/bin/systemctl stop postgresql-%{pgpackageversion}.service >/dev/null 2>&1 || :
%else
	/sbin/service postgresql-%{pgpackageversion} condstop >/dev/null 2>&1
	chkconfig --del postgresql-%{pgpackageversion}

%endif
fi

%postun server
/sbin/ldconfig
%if %{systemd_enabled}
 /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
 /sbin/service postgresql-%{pgpackageversion} condrestart >/dev/null 2>&1
%endif
if [ $1 -ge 1 ] ; then
 %if %{systemd_enabled}
	# Package upgrade, not uninstall
	/bin/systemctl try-restart postgresql-%{pgpackageversion}.service >/dev/null 2>&1 || :
 %else
   /sbin/service postgresql-%{pgpackageversion} condrestart >/dev/null 2>&1
 %endif
fi

# Create alternatives entries for common binaries and man files
%post
%{_sbindir}/update-alternatives --install %{_bindir}/psql pgsql-psql %{pginstdir}/bin/psql %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/clusterdb pgsql-clusterdb %{pginstdir}/bin/clusterdb %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/createdb pgsql-createdb %{pginstdir}/bin/createdb %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/createlang pgsql-createlang %{pginstdir}/bin/createlang %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/createuser pgsql-createuser %{pginstdir}/bin/createuser %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/dropdb pgsql-dropdb %{pginstdir}/bin/dropdb %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/droplang pgsql-droplang %{pginstdir}/bin/droplang %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/dropuser pgsql-dropuser %{pginstdir}/bin/dropuser %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_basebackup pgsql-pg_basebackup %{pginstdir}/bin/pg_basebackup %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_dump pgsql-pg_dump %{pginstdir}/bin/pg_dump %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_dumpall pgsql-pg_dumpall %{pginstdir}/bin/pg_dumpall %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_restore pgsql-pg_restore %{pginstdir}/bin/pg_restore %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/reindexdb pgsql-reindexdb %{pginstdir}/bin/reindexdb %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/vacuumdb pgsql-vacuumdb %{pginstdir}/bin/vacuumdb %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/clusterdb.1 pgsql-clusterdbman %{pginstdir}/share/man/man1/clusterdb.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/createdb.1 pgsql-createdbman %{pginstdir}/share/man/man1/createdb.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/createlang.1 pgsql-createlangman %{pginstdir}/share/man/man1/createlang.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/createuser.1 pgsql-createuserman %{pginstdir}/share/man/man1/createuser.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/dropdb.1 pgsql-dropdbman %{pginstdir}/share/man/man1/dropdb.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/droplang.1 pgsql-droplangman %{pginstdir}/share/man/man1/droplang.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/dropuser.1 pgsql-dropuserman %{pginstdir}/share/man/man1/dropuser.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_basebackup.1 pgsql-pg_basebackupman %{pginstdir}/share/man/man1/pg_basebackup.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_dump.1 pgsql-pg_dumpman %{pginstdir}/share/man/man1/pg_dump.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_dumpall.1 pgsql-pg_dumpallman %{pginstdir}/share/man/man1/pg_dumpall.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_restore.1 pgsql-pg_restoreman %{pginstdir}/share/man/man1/pg_restore.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/psql.1 pgsql-psqlman %{pginstdir}/share/man/man1/psql.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/reindexdb.1 pgsql-reindexdbman %{pginstdir}/share/man/man1/reindexdb.1 %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/vacuumdb.1 pgsql-vacuumdbman %{pginstdir}/share/man/man1/vacuumdb.1 %{pgmajorversion}0

%post libs
%{_sbindir}/update-alternatives --install /etc/ld.so.conf.d/postgresql-pgdg-libs.conf pgsql-ld-conf %{pginstdir}/share/postgresql-%{pgpackageversion}-libs.conf %{pgmajorversion}0
/sbin/ldconfig

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove pgsql-psql		%{pginstdir}/bin/psql
	%{_sbindir}/update-alternatives --remove pgsql-clusterdb	%{pginstdir}/bin/clusterdb
	%{_sbindir}/update-alternatives --remove pgsql-clusterdbman	%{pginstdir}/share/man/man1/clusterdb.1
	%{_sbindir}/update-alternatives --remove pgsql-createdb		%{pginstdir}/bin/createdb
	%{_sbindir}/update-alternatives --remove pgsql-createdbman	%{pginstdir}/share/man/man1/createdb.1
	%{_sbindir}/update-alternatives --remove pgsql-createlang	%{pginstdir}/bin/createlang
	%{_sbindir}/update-alternatives --remove pgsql-createlangman	%{pginstdir}/share/man/man1/createlang.1
	%{_sbindir}/update-alternatives --remove pgsql-createuser	%{pginstdir}/bin/createuser
	%{_sbindir}/update-alternatives --remove pgsql-createuserman	%{pginstdir}/share/man/man1/createuser.1
	%{_sbindir}/update-alternatives --remove pgsql-dropdb		%{pginstdir}/bin/dropdb
	%{_sbindir}/update-alternatives --remove pgsql-dropdbman	%{pginstdir}/share/man/man1/dropdb.1
	%{_sbindir}/update-alternatives --remove pgsql-droplang		%{pginstdir}/bin/droplang
	%{_sbindir}/update-alternatives --remove pgsql-droplangman	%{pginstdir}/share/man/man1/droplang.1
	%{_sbindir}/update-alternatives --remove pgsql-dropuser		%{pginstdir}/bin/dropuser
	%{_sbindir}/update-alternatives --remove pgsql-dropuserman	%{pginstdir}/share/man/man1/dropuser.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_basebackup	%{pginstdir}/bin/pg_basebackup
	%{_sbindir}/update-alternatives --remove pgsql-pg_dump		%{pginstdir}/bin/pg_dump
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpall	%{pginstdir}/bin/pg_dumpall
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpallman	%{pginstdir}/share/man/man1/pg_dumpall.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_basebackupman	%{pginstdir}/share/man/man1/pg_basebackup.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpman	%{pginstdir}/share/man/man1/pg_dump.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_restore	%{pginstdir}/bin/pg_restore
	%{_sbindir}/update-alternatives --remove pgsql-pg_restoreman	%{pginstdir}/share/man/man1/pg_restore.1
	%{_sbindir}/update-alternatives --remove pgsql-psqlman		%{pginstdir}/share/man/man1/psql.1
	%{_sbindir}/update-alternatives --remove pgsql-reindexdb	%{pginstdir}/bin/reindexdb
	%{_sbindir}/update-alternatives --remove pgsql-reindexdbman	%{pginstdir}/share/man/man1/reindexdb.1
	%{_sbindir}/update-alternatives --remove pgsql-vacuumdb		%{pginstdir}/bin/vacuumdb
	%{_sbindir}/update-alternatives --remove pgsql-vacuumdbman	%{pginstdir}/share/man/man1/vacuumdb.1
  fi

%postun libs
if [ "$1" -eq 0 ]
  then
	%{_sbindir}/update-alternatives --remove pgsql-ld-conf		%{pginstdir}/share/postgresql-%{pgpackageversion}-libs.conf
	/sbin/ldconfig
fi

%clean
%{__rm} -rf %{buildroot}

# FILES section.

%files -f pg_main.lst
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES
%doc COPYRIGHT doc/bug.template
%doc README.rpm-dist
%{pginstdir}/bin/clusterdb
%{pginstdir}/bin/createdb
%{pginstdir}/bin/createlang
%{pginstdir}/bin/createuser
%{pginstdir}/bin/dropdb
%{pginstdir}/bin/droplang
%{pginstdir}/bin/dropuser
%{pginstdir}/bin/pgbench
%{pginstdir}/bin/pg_archivecleanup
%{pginstdir}/bin/pg_basebackup
%{pginstdir}/bin/pg_config
%{pginstdir}/bin/pg_dump
%{pginstdir}/bin/pg_dumpall
%{pginstdir}/bin/pg_isready
%{pginstdir}/bin/pg_restore
%{pginstdir}/bin/pg_rewind
%{pginstdir}/bin/pg_test_fsync
%{pginstdir}/bin/pg_test_timing
%{pginstdir}/bin/pg_receivexlog
%{pginstdir}/bin/pg_upgrade
%{pginstdir}/bin/pg_xlogdump
%{pginstdir}/bin/psql
%{pginstdir}/bin/reindexdb
%{pginstdir}/bin/vacuumdb
%{pginstdir}/share/man/man1/clusterdb.*
%{pginstdir}/share/man/man1/createdb.*
%{pginstdir}/share/man/man1/createlang.*
%{pginstdir}/share/man/man1/createuser.*
%{pginstdir}/share/man/man1/dropdb.*
%{pginstdir}/share/man/man1/droplang.*
%{pginstdir}/share/man/man1/dropuser.*
%{pginstdir}/share/man/man1/pgbench.1
%{pginstdir}/share/man/man1/pg_archivecleanup.1
%{pginstdir}/share/man/man1/pg_basebackup.*
%{pginstdir}/share/man/man1/pg_config.*
%{pginstdir}/share/man/man1/pg_dump.*
%{pginstdir}/share/man/man1/pg_dumpall.*
%{pginstdir}/share/man/man1/pg_isready.*
%{pginstdir}/share/man/man1/pg_receivexlog.*
%{pginstdir}/share/man/man1/pg_restore.*
%{pginstdir}/share/man/man1/pg_rewind.1
%{pginstdir}/share/man/man1/pg_test_fsync.1
%{pginstdir}/share/man/man1/pg_test_timing.1
%{pginstdir}/share/man/man1/pg_upgrade.1
%{pginstdir}/share/man/man1/pg_xlogdump.1
%{pginstdir}/share/man/man1/psql.*
%{pginstdir}/share/man/man1/reindexdb.*
%{pginstdir}/share/man/man1/vacuumdb.*
%{pginstdir}/share/man/man3/*
%{pginstdir}/share/man/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/*
%doc *-A4.pdf
%doc src/tutorial
%doc doc/html

%files contrib
%defattr(-,root,root)
%doc %{pginstdir}/doc/extension/*.example
%{pginstdir}/lib/_int.so
%{pginstdir}/lib/adminpack.so
%{pginstdir}/lib/auth_delay.so
%{pginstdir}/lib/autoinc.so
%{pginstdir}/lib/auto_explain.so
%{pginstdir}/lib/bloom.so
%{pginstdir}/lib/btree_gin.so
%{pginstdir}/lib/btree_gist.so
%{pginstdir}/lib/chkpass.so
%{pginstdir}/lib/citext.so
%{pginstdir}/lib/cube.so
%{pginstdir}/lib/dblink.so
%{pginstdir}/lib/earthdistance.so
%{pginstdir}/lib/file_fdw.so*
%{pginstdir}/lib/fuzzystrmatch.so
%{pginstdir}/lib/insert_username.so
%{pginstdir}/lib/isn.so
%{pginstdir}/lib/hstore.so
%if %plperl
%{pginstdir}/lib/hstore_plperl.so
%endif
%if %plpython
%{pginstdir}/lib/hstore_plpython2.so
%endif
%{pginstdir}/lib/lo.so
%{pginstdir}/lib/ltree.so
%if %plpython
%{pginstdir}/lib/ltree_plpython2.so
%endif
%{pginstdir}/lib/moddatetime.so
%{pginstdir}/lib/pageinspect.so
%{pginstdir}/lib/passwordcheck.so
%{pginstdir}/lib/pgcrypto.so
%{pginstdir}/lib/pgrowlocks.so
%{pginstdir}/lib/pgstattuple.so
%{pginstdir}/lib/pg_buffercache.so
%{pginstdir}/lib/pg_freespacemap.so
%{pginstdir}/lib/pg_prewarm.so
%{pginstdir}/lib/pg_stat_statements.so
%{pginstdir}/lib/pg_trgm.so
%{pginstdir}/lib/pg_visibility.so
%{pginstdir}/lib/postgres_fdw.so
%{pginstdir}/lib/refint.so
%{pginstdir}/lib/seg.so
%if %selinux
%{pginstdir}/lib/sepgsql.so
%{pginstdir}/share/contrib/sepgsql.sql
%endif
%{pginstdir}/lib/tablefunc.so
%{pginstdir}/lib/tcn.so
%{pginstdir}/lib/test_decoding.so
%{pginstdir}/lib/timetravel.so
%{pginstdir}/lib/tsm_system_rows.so
%{pginstdir}/lib/tsm_system_time.so
%{pginstdir}/lib/unaccent.so
%if %xml
%{pginstdir}/lib/pgxml.so
%endif
%if %uuid
%{pginstdir}/lib/uuid-ossp.so
%endif
%{pginstdir}/share/extension/adminpack*
%{pginstdir}/share/extension/autoinc*
%{pginstdir}/share/extension/bloom*
%{pginstdir}/share/extension/btree_gin*
%{pginstdir}/share/extension/btree_gist*
%{pginstdir}/share/extension/chkpass*
%{pginstdir}/share/extension/citext*
%{pginstdir}/share/extension/cube*
%{pginstdir}/share/extension/dblink*
%{pginstdir}/share/extension/dict_int*
%{pginstdir}/share/extension/dict_xsyn*
%{pginstdir}/share/extension/earthdistance*
%{pginstdir}/share/extension/file_fdw*
%{pginstdir}/share/extension/fuzzystrmatch*
%{pginstdir}/share/extension/hstore*
%{pginstdir}/share/extension/insert_username*
%{pginstdir}/share/extension/intagg*
%{pginstdir}/share/extension/intarray*
%{pginstdir}/share/extension/isn*
%{pginstdir}/share/extension/lo*
%{pginstdir}/share/extension/ltree*
%{pginstdir}/share/extension/moddatetime*
%{pginstdir}/share/extension/pageinspect*
%{pginstdir}/share/extension/pg_buffercache*
%{pginstdir}/share/extension/pg_freespacemap*
%{pginstdir}/share/extension/pg_prewarm*
%{pginstdir}/share/extension/pg_stat_statements*
%{pginstdir}/share/extension/pg_trgm*
%{pginstdir}/share/extension/pg_visibility*
%{pginstdir}/share/extension/pgcrypto*
%{pginstdir}/share/extension/pgrowlocks*
%{pginstdir}/share/extension/pgstattuple*
%{pginstdir}/share/extension/postgres_fdw*
%{pginstdir}/share/extension/refint*
%{pginstdir}/share/extension/seg*
%{pginstdir}/share/extension/tablefunc*
%{pginstdir}/share/extension/tcn*
%{pginstdir}/share/extension/timetravel*
%{pginstdir}/share/extension/tsearch2*
%{pginstdir}/share/extension/tsm_system_rows*
%{pginstdir}/share/extension/tsm_system_time*
%{pginstdir}/share/extension/unaccent*
%if %uuid
%{pginstdir}/share/extension/uuid-ossp*
%endif
%if %xml
%{pginstdir}/share/extension/xml2*
%endif
%{pginstdir}/bin/oid2name
%{pginstdir}/bin/vacuumlo
%{pginstdir}/bin/pg_recvlogical
%{pginstdir}/bin/pg_standby
%{pginstdir}/share/man/man1/oid2name.1
%{pginstdir}/share/man/man1/pg_recvlogical.1
%{pginstdir}/share/man/man1/pg_standby.1
%{pginstdir}/share/man/man1/vacuumlo.1

%files libs -f pg_libpq5.lst
%defattr(-,root,root)
%{pginstdir}/lib/libpq.so.*
%{pginstdir}/lib/libecpg.so*
%{pginstdir}/lib/libpgfeutils.a
%{pginstdir}/lib/libpgtypes.so.*
%{pginstdir}/lib/libecpg_compat.so.*
%{pginstdir}/lib/libpqwalreceiver.so
%config(noreplace) %attr (644,root,root) %{pginstdir}/share/postgresql-%{pgpackageversion}-libs.conf

%files server -f pg_server.lst
%defattr(-,root,root)
%if %{systemd_enabled}
%{pginstdir}/bin/postgresql%{pgmajorversion}-setup
%{pginstdir}/bin/postgresql%{pgmajorversion}-check-db-dir
%{_tmpfilesdir}/postgresql-%{pgpackageversion}.conf
%{_unitdir}/postgresql-%{pgpackageversion}.service
%else
%config(noreplace) %{_initrddir}/postgresql-%{pgpackageversion}
%endif
%if %pam
%config(noreplace) /etc/pam.d/%{sname}
%endif
%attr (755,root,root) %dir /etc/sysconfig/pgsql
%{pginstdir}/bin/initdb
%{pginstdir}/bin/pg_controldata
%{pginstdir}/bin/pg_ctl
%{pginstdir}/bin/pg_resetxlog
%{pginstdir}/bin/postgres
%{pginstdir}/bin/postmaster
%{pginstdir}/share/man/man1/initdb.*
%{pginstdir}/share/man/man1/pg_controldata.*
%{pginstdir}/share/man/man1/pg_ctl.*
%{pginstdir}/share/man/man1/pg_resetxlog.*
%{pginstdir}/share/man/man1/postgres.*
%{pginstdir}/share/man/man1/postmaster.*
%{pginstdir}/share/postgres.bki
%{pginstdir}/share/postgres.description
%{pginstdir}/share/postgres.shdescription
%{pginstdir}/share/system_views.sql
%{pginstdir}/share/*.sample
%{pginstdir}/share/timezonesets/*
%{pginstdir}/share/tsearch_data/*.affix
%{pginstdir}/share/tsearch_data/*.dict
%{pginstdir}/share/tsearch_data/*.ths
%{pginstdir}/share/tsearch_data/*.rules
%{pginstdir}/share/tsearch_data/*.stop
%{pginstdir}/share/tsearch_data/*.syn
%{pginstdir}/lib/dict_int.so
%{pginstdir}/lib/dict_snowball.so
%{pginstdir}/lib/dict_xsyn.so
%{pginstdir}/lib/euc2004_sjis2004.so
%{pginstdir}/lib/plpgsql.so
%dir %{pginstdir}/share/extension
%{pginstdir}/share/extension/plpgsql*
%{pginstdir}/lib/tsearch2.so

%dir %{pginstdir}/lib
%dir %{pginstdir}/share
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
#%attr(700,postgres,postgres) %dir /var/lib/pgsql
%endif
%else
%attr(700,postgres,postgres) %dir /var/lib/pgsql
%endif
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{pgpackageversion}
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{pgpackageversion}/data
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{pgpackageversion}/backups
%attr(755,postgres,postgres) %dir /var/run/postgresql
%{pginstdir}/lib/*_and_*.so
%{pginstdir}/share/conversion_create.sql
%{pginstdir}/share/information_schema.sql
%{pginstdir}/share/snowball_create.sql
%{pginstdir}/share/sql_features.txt

%files devel -f pg_devel.lst
%defattr(-,root,root)
%{pginstdir}/include/*
%{pginstdir}/bin/ecpg
%{pginstdir}/lib/libpq.so
%{pginstdir}/lib/libecpg.so
%{pginstdir}/lib/libpq.a
%{pginstdir}/lib/libecpg.a
%{pginstdir}/lib/libecpg_compat.so
%{pginstdir}/lib/libecpg_compat.a
%{pginstdir}/lib/libpgcommon.a
%{pginstdir}/lib/libpgport.a
%{pginstdir}/lib/libpgtypes.so
%{pginstdir}/lib/libpgtypes.a
%{pginstdir}/lib/pgxs/*
%{pginstdir}/lib/pkgconfig/*
%{pginstdir}/share/man/man1/ecpg.*

%if %plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%{pginstdir}/lib/plperl.so
%{pginstdir}/share/extension/plperl*
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%{pginstdir}/lib/pltcl.so
%{pginstdir}/bin/pltcl_delmod
%{pginstdir}/bin/pltcl_listmod
%{pginstdir}/bin/pltcl_loadmod
%{pginstdir}/share/unknown.pltcl
%{pginstdir}/share/extension/pltcl*
%endif

%if %plpython
%files plpython -f pg_plpython.lst
%defattr(-,root,root)
%{pginstdir}/lib/plpython2.so
%{pginstdir}/share/extension/plpython2u*
%{pginstdir}/share/extension/plpythonu*
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{pginstdir}/lib/test/*
%attr(-,postgres,postgres) %dir %{pginstdir}/lib/test
%endif

%changelog
* Wed Nov 29 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.6-2PGDG-1
- Fixes for CVE-2017-12172 (RHEL-6 only)

* Wed Nov 8 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.6-1PGDG-1
- Update to 9.6.6, per changes described at:
  https://www.postgresql.org/docs/devel/static/release-9-6-6.html

* Sun Oct 15 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.5-2PGDG-1
- Fix #1289 (OOM killer control for PostgreSQL)
- Do not set any timeout value, so that systemd will not kill postmaster
  during crash recovery. Fixes #2786.

* Mon Aug 28 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.5-1PGDG-1
- Update to 9.6.5, per changes described at:
  http://www.postgresql.org/docs/devel/static/release-9-6-5.html

* Mon Aug 7 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.4-1PGDG-1
- Update to 9.6.4, per changes described at:
  http://www.postgresql.org/docs/devel/static/release-9-6-4.html

* Mon Jul 17 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.3-4PGDG-1
- Add tcl as a dependency to pltcl subpackage, per Fahar Abbas.

* Tue Jul 4 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.3-3PGDG-1
- Bump up the version to fix breakage on RHEL 6 - i386. The other
  distros will not be updated.

* Mon Jun 12 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.3-2PGDG-1
- Rename all patches, and add the same prefix to them.
- Rename some macros for consistency with other packages.
- Use separate README files for RHEL6 and others. Fixes #2471.
- Remove nonexistent Patch7 reference
- Add missing prevversion macro, per #2416.

* Tue May 9 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.3-1PGDG-1
- Update to 9.6.3, per changes described at:
  http://www.postgresql.org/docs/devel/static/release-9-6-3.html
- Fix #2189 and #2384.

* Wed Apr 12 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.2-3PGDG-1
- Initial attempt for Power RPMs.

* Wed Feb 22 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.2-2PGDG-1
- Fix creating parent directory issue in setup script, per report and fix
  from Magnus. Fixes #2188

* Tue Feb 7 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.2-1PGDG-1
- Update to 9.6.2,  per changes described at:
  http://www.postgresql.org/docs/devel/static/release-9-6-2.html

* Thu Jan 5 2017 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.1-3PGDG-1
- Remove various hacks for RHEL 5.

* Sat Dec 31 2016 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.1-2PGDG-1
- Remove unnecessary ldconfig calls, per
  https://bugzilla.redhat.com/show_bug.cgi?id=849344
- Fix build when some macros are disabled. Per report and patch from
  Tomoaki Sato.
- Various cleanup and improvements, Jonathon Nelson:
  - Add min version to flex dependency
  - Remove redundant strip of -ffast-math from CFLAGS
  - Aesthetic cleanup in a Requires line (groupadd)
  - Remove redundant translation file list init.
  - Use %%{mandir} and %%{bindir} in update-alternatives section.

* Mon Oct 24 2016 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.1-1PGDG-1
- Update to 9.6.1,  per changes described at:
  http://www.postgresql.org/docs/devel/static/release-9-6-1.html
- Remove the hack in spec file for PL/Python builds. Fixed upstream.
- Put back a useless block, to supress ldconfig issues temporarily until
  we have a good fix. Per John.
- Append PostgreSQL major version number to -libs provides.

* Mon Sep 26 2016 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6.0-1PGDG-1
- Update to 9.6.0,  per changes described at:
  http://www.postgresql.org/docs/devel/static/release-9-6.html
- Compile with --enable-tap-tests, per suggestion from Tom Lane.
- Disable tap tests on RHEL, because Red Hat does not ship with the
  necessary deps. CentOS has them, but we cannot ask RHEL users to use
  CentOS packages.  Per John Harvey.

* Tue Aug 30 2016 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6rc1-1PGDG-1
- Update to 9.6 rc1
- Don't remove .pgsql_profile line in .bash_profile each time. Fixes #1215.

* Fri Aug 12 2016 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6beta4-1PGDG-1
- Put systemd support to both build parts. This fixes the startup issue.

* Thu Aug 11 2016 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6beta4-1PGDG-1
- Update to 9.6 beta4
- Build with systemd support natively, and change the service file to
  use the notify type. Patch from Peter Eisentraut. Fixes #1529.
- Remove useless chown in %%test conditional, per report from John
  Harvey. Fixes #1522.
- Add /usr/sbin/groupadd as a dependency, per John . Fixes #1522
- Remove useless BR, per Peter Eisentraut. Fixes #1528.

* Tue Jul 19 2016 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6beta3-1PGDG-1
- Update to 9.6 beta3

* Wed Jun 29 2016 Jeff Frost <jeff@pgexperts.com> - 9.6beta2-2PGDG-1
- Fix data and bin directories in init script for EL-6

* Thu Jun 23 2016 Jeff Frost <jeff@pgexperts.com> - 9.6beta2-1PGDG-1
- Initial cut for PostgreSQL 9.6 Beta 2

* Sat May 14 2016 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6beta1-2PGDG-1
- Fix typo in spec file, per report from Andrew Dunstan.

* Thu May 12 2016 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6beta1-1PGDG-1
- Initial cut for PostgreSQL 9.6 Beta 1

* Fri Mar 25 2016 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6devel-git20160325_1PGDG-1
- Update to Mar 25, 2016 tarball.

* Thu Mar 10 2016 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6devel-git20160310_1PGDG-1
- Sync with 9.5 spec, which is the unified one, before it is too late.
- Update to Mar 10, 2016 tarball.

* Thu Jan 21 2016 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6devel-git20160121_1PGDG-1
- Update to Jan 21, 2016 tarball.

* Mon Dec 28 2015 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6devel-git20151228_1PGDG-1
- Update to Dec 28, 2015 tarball.

* Wed Nov 18 2015 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6devel-git20151118_1PGDG-1
- Update to Nov 18, 2015 tarball.
- Enable debug and cassert builds.
- Start pg_ctl with -c parameter, so that it produces core dumps.

* Mon Nov 16 2015 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6devel-git20151116_1PGDG-1
- Update to Nov 16, 2015 tarball.

* Fri Nov 13 2015 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> - 9.6devel-git20151113_1PGDG-1
- Initial cut for PostgreSQL 9.6devel.

