Summary:	A port forwarder that works with IPChains and IPFWADM
Summary(pl):	Forwarder portów dzia³aj±cy z ipchains i ipfwadm
Name:		portfwd
Version:	0.22
Release:	2
License:	GPL
Vendor:		Everton da Silva Marques
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(es):	Red/Servidores
Group(fr):	Réseau/Serveurs
Group(pl):	Sieciowe/Serwery
Group(pt):	Rede/Server
Source0:	ftp://ftp.sourceforge.net/pub/sorceforge/portfwd/%{name}-%{version}.tar.gz
Patch0:		%{name}-am_fixes.patch
PAtch1:		%{name}-ac_fixes.patch
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://portfwd.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	libstdc++-devel
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PortFwd, by Everton da Silva Marques, is a small C++ user-space
utility which forwards incoming TCP connections and/or UDP packets to
remote hosts. Features:
- forwarding based on originator port
- multiple ports forwarded from one config file
- FTP forwarding, which requires two ports.

%description -l pl
PortFwd, autorstwa Evertona de Silva Marquesa, jest ma³ym narzêdziem w
C++ dzia³aj±cym w user-space, przekierowuj±cym po³±czenia TCP lub
pakiety UDP na zewnêtrzne hosty. Cechy:
- przekierowywanie zale¿ne od portu ¼ród³owego
- konfiguracja wielu portów w jednym pliku konfiguracyjnym
- przekierowywanie FTP - wymagaj±ce dwóch portów.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f config/missing
aclocal
autoconf
automake -a -c
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

gzip -9nf CREDITS README TODO cfg/* contrib/suggestions.txt doc/FAQ doc/conf.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add portfwd

%postun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del portfwd
fi

%files
%defattr(644,root,root,755)
%doc *.gz cfg/*.gz contrib/*.gz doc/*.gz
%attr(755,root,root) %{_sbindir}/portfwd
%{_mandir}/man?/*
%attr(754,root,root) /etc/rc.d/init.d/portfwd
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/portfwd
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/portfwd.cfg
