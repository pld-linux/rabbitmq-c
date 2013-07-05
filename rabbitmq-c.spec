#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	RabbitMQ C AMQP client library
Summary(pl.UTF-8):	Biblioteka kliencka C RabbitMQ AMQP
Name:		rabbitmq-c
Version:	0.3.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/alanxz/rabbitmq-c
Source0:	https://github.com/alanxz/rabbitmq-c/archive/%{name}-v%{version}.tar.gz
# Source0-md5:	a7f0fbf59bf29843ad4125b1a784a520
URL:		https://github.com/alanxz/rabbitmq-c
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	libtool >= 2:2.2
BuildRequires:	xmlto
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
%setup -q -n %{name}-%{name}-v%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING.md LICENSE-MIT README.md THANKS TODO
%attr(755,root,root) %{_libdir}/librabbitmq.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librabbitmq.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librabbitmq.so
%{_includedir}/amqp.h
%{_includedir}/amqp_framing.h
%{_pkgconfigdir}/librabbitmq.pc

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
