Summary:	User-space port forwarder
Summary(pl.UTF-8):	Forwarder portów działający w przestrzeni użytkownika
Name:		portfwd
Version:	0.29
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/portfwd/%{name}-%{version}.tar.gz
# Source0-md5:	93161c91e12b0d67ca52dc13708a2f2f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://portfwd.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PortFwd, by Everton da Silva Marques, is a small C++ user-space
utility which forwards incoming TCP connections and/or UDP packets to
remote hosts. Features:
- forwarding based on originator port
- multiple ports forwarded from one config file
- FTP forwarding, which requires two ports.

%description -l pl.UTF-8
PortFwd, autorstwa Evertona de Silva Marquesa, jest małym narzędziem w
C++ działającym w przestrzeni użytkownika, przekierowującym połączenia
TCP lub pakiety UDP na zewnętrzne hosty. Cechy:
- przekierowywanie zależne od portu źródłowego
- konfiguracja wielu portów w jednym pliku konfiguracyjnym
- przekierowywanie FTP - wymagające dwóch portów.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install cfg/empty.cfg $RPM_BUILD_ROOT%{_sysconfdir}/portfwd.cfg

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/portfwd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/portfwd
rm -rf $RPM_BUILD_ROOT%{_prefix}/doc/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add portfwd
%service portfwd restart

%preun
if [ "$1" = "0" ]; then
	%service portfwd stop
	/sbin/chkconfig --del portfwd
fi

%files
%defattr(644,root,root,755)
%doc CREDITS README TODO cfg/* contrib/suggestions.txt doc/FAQ doc/conf.txt
%attr(755,root,root) %{_sbindir}/portfwd
%attr(754,root,root) /etc/rc.d/init.d/portfwd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/portfwd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/portfwd.cfg
%{_mandir}/man?/*
