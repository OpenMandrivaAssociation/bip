%define prerel	rc1
%define rel	1

%if %{prerel}
%define release		%mkrel 0.%{prerel}.%{rel}
%define distname	%{name}-%{version}-%{prerel}.tar.gz
%define dirname		%{name}-%{version}-%{prerel}
%else
%define release		%mkrel %{rel}
%define distname	%{name}-%{version}.tar.gz
%define dirname		%{name}-%{version}
%endif

Name:		bip
Version:	0.8.0
Release:	%{release}
Summary:	IRC Bouncer (proxy)
Group:		Networking/IRC
License:	GPLv2+
URL:		http://bip.t1r.net
Source0:	http://bip.t1r.net/downloads/%{distname}
Source1:	bip.init
Patch0:		bip-conf.patch
BuildRequires:	openssl-devel
BuildRequires:	flex
BuildRequires:	byacc

%description
Bip is an IRC proxy, which means it keeps connected to your preferred IRC
servers, can store the logs for you, and even send them back to your IRC
client(s) upon connection.
You may want to use bip to keep your logfiles (in a unique format and on a
unique computer) whatever your client is, when you connect from multiple
workstations, or when you simply want to have a playback of what was said
while you were away.

%prep
%setup -q -n %{dirname}
%patch0 -p0
iconv -f iso-8859-1 -t utf-8 -o ChangeLog{.utf8,}
mv ChangeLog{.utf8,}

%build
%configure2_5x --enable-openssl
make CFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Remove misplaced files
rm -rf %{buildroot}%{_defaultdocdir}/bip
mkdir -p %{buildroot}%{_sysconfdir}
# Install bip.conf
install -m 644 samples/bip.conf %{buildroot}%{_sysconfdir}/bip.conf
# Install initscript
mkdir -p %{buildroot}%{_initrddir}
install -m755 %{SOURCE1} %{buildroot}%{_initrddir}/bip
mkdir -p %{buildroot}%{_localstatedir}/run/bip
mkdir -p %{buildroot}%{_localstatedir}/log/bip

%clean
rm -rf %{buildroot}


%pre
/usr/sbin/useradd -c "Bip IRC Proxy" \
  -s /bin/sh -r -d / bip 2> /dev/null || :

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
if [ "$1" -ge 1 ]; then
  /sbin/service bip condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog README TODO
%doc samples/bip.vim
%{_bindir}/bip
%{_bindir}/bipmkpw
%{_mandir}/man1/bip.1*
%{_mandir}/man5/bip.conf.5*
%config(noreplace) %{_sysconfdir}/bip.conf
%{_initrddir}/bip
%attr(-,bip,bip) %dir %{_localstatedir}/run/bip
%attr(-,bip,bip) %dir %{_localstatedir}/log/bip

