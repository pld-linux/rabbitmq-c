#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_without	tests		# tests
#
%if %{without static_libs}
# tests require static libs
%undefine	with_tests
%endif
Summary:	RabbitMQ C AMQP client library
Summary(pl.UTF-8):	Biblioteka kliencka C RabbitMQ AMQP
Name:		rabbitmq-c
Version:	0.13.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/alanxz/rabbitmq-c/releases
Source0:	https://github.com/alanxz/rabbitmq-c/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2de19cdd2b4f7c76f624f031e161f925
URL:		https://github.com/alanxz/rabbitmq-c
BuildRequires:	cmake >= 3.12
BuildRequires:	openssl-devel >= 1.1.1
BuildRequires:	popt-devel
BuildRequires:	pkgconfig >= 1:0.17
BuildRequires:	xmlto
Requires:	openssl >= 1.1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a C-language AMQP client library for use with AMQP servers
speaking protocol versions 0-9-1.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę kliencką AMQP dla języka C, przeznaczoną
do użycia z serwerami AMQP obsługującymi protokół w wersjach 0-9-1.

%package devel
Summary:	Header files for rabbitmq-c library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki rabbitmq-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel >= 1.1.1

%description devel
Header files for rabbitmq-c library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki rabbitmq-c.

%package static
Summary:	Static rabbitmq-c library
Summary(pl.UTF-8):	Statyczna biblioteka rabbitmq-c
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static rabbitmq-c library.

%description static -l pl.UTF-8
Statyczna biblioteka rabbitmq-c.

%package tools
Summary:	Example tools utilizing the rabbitmq-c library
Summary(pl.UTF-8):	Przykładowe narzędzia wykorzystujące bibliotekę rabbitmq-c
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description tools
Example tools utilizing the rabbitmq-c library.

%description tools -l pl.UTF-8
Przykładowe narzędzia wykorzystujące bibliotekę rabbitmq-c.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	%{!?with_static_libs:-DBUILD_STATIC_LIBS=OFF} \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DBUILD_TOOLS=ON \
	-DBUILD_TOOLS_DOCS=ON \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING.md LICENSE README.md THANKS
%attr(755,root,root) %{_libdir}/librabbitmq.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librabbitmq.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librabbitmq.so
%{_includedir}/amqp.h
%{_includedir}/amqp_framing.h
%{_includedir}/amqp_ssl_socket.h
%{_includedir}/amqp_tcp_socket.h
%{_includedir}/rabbitmq-c
%{_pkgconfigdir}/librabbitmq.pc
%{_libdir}/cmake/rabbitmq-c

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/librabbitmq.a
%endif

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/amqp-consume
%attr(755,root,root) %{_bindir}/amqp-declare-queue
%attr(755,root,root) %{_bindir}/amqp-delete-queue
%attr(755,root,root) %{_bindir}/amqp-get
%attr(755,root,root) %{_bindir}/amqp-publish
%{_mandir}/man1/amqp-consume.1*
%{_mandir}/man1/amqp-declare-queue.1*
%{_mandir}/man1/amqp-delete-queue.1*
%{_mandir}/man1/amqp-get.1*
%{_mandir}/man1/amqp-publish.1*
%{_mandir}/man7/librabbitmq-tools.7*
