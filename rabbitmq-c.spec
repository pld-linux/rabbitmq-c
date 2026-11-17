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
Version:	0.18.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/alanxz/rabbitmq-c/releases
Source0:	https://github.com/alanxz/rabbitmq-c/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e1f42868c14ac0ff39d3bf32474d762a
URL:		https://github.com/alanxz/rabbitmq-c
BuildRequires:	cmake >= 3.22
BuildRequires:	openssl-devel >= 1.1.1
BuildRequires:	popt-devel >= 1.14
BuildRequires:	pkgconfig >= 1:0.17
BuildRequires:	xmlto
Requires:	openssl%{?_isa} >= 1.1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a C-language AMQP client library for use with v2.0+ of the
RabbitMQ broker.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę kliencką AMQP dla języka C, przeznaczoną
do użycia z brokerami RabbitMQ w wersji 2.0+.

%package devel
Summary:	Header files for rabbitmq-c library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki rabbitmq-c
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	openssl-devel%{?_isa} >= 1.1.1

%description devel
Header files for rabbitmq-c library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki rabbitmq-c.

%package static
Summary:	Static rabbitmq-c library
Summary(pl.UTF-8):	Statyczna biblioteka rabbitmq-c
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static rabbitmq-c library.

%description static -l pl.UTF-8
Statyczna biblioteka rabbitmq-c.

%package tools
Summary:	Example tools utilizing the rabbitmq-c library
Summary(pl.UTF-8):	Przykładowe narzędzia wykorzystujące bibliotekę rabbitmq-c
Group:		Applications
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	popt%{?_isa} >= 1.14

%description tools
Example tools utilizing the rabbitmq-c library.

%description tools -l pl.UTF-8
Przykładowe narzędzia wykorzystujące bibliotekę rabbitmq-c.

%prep
%setup -q

%build
%cmake -B build \
	%{!?with_static_libs:-DBUILD_STATIC_LIBS=OFF} \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DBUILD_TOOLS=ON \
	-DBUILD_TOOLS_DOCS=ON

%{__make} -C build

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
%{_libdir}/librabbitmq.so.*.*.*
%ghost %{_libdir}/librabbitmq.so.4

%files devel
%defattr(644,root,root,755)
%{_libdir}/librabbitmq.so
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
