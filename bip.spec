Summary:	IRC Bouncer (proxy)
Name:		bip
Version:	0.8.9
Release:	2
Group:		Networking/IRC
License:	GPLv2+
Url:		https://bip.t1r.net
Source0:	https://projects.duckcorp.org/attachments/download/20/bip-%{version}.tar.gz
Source2:	bip-tmpfs.conf
Source3:	bip.service
Patch0:		0001-Setup-bip-for-Fedora-s-paths.patch
Patch1:		0002-Throttle-joins-to-prevent-flooding.patch
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	systemd-units
BuildRequires:	pkgconfig(openssl)
Requires(post,preun,postun):	systemd-units

%description
Bip is an IRC proxy, which means it keeps connected to your preferred IRC
servers, can store the logs for you, and even send them back to your IRC
client(s) upon connection.
You may want to use bip to keep your logfiles (in a unique format and on a
unique computer) whatever your client is, when you connect from multiple
workstations, or when you simply want to have a playback of what was said
while you were away.

%files
%doc AUTHORS ChangeLog COPYING README TODO
%doc samples/bip.vim
%{_bindir}/bip
%{_bindir}/bipgenconfig
%{_bindir}/bipmkpw
%{_mandir}/man1/bip.1*
%{_mandir}/man1/bipmkpw.1*
%{_mandir}/man5/bip.conf.5*
%attr(0640,root,bip) %config(noreplace) %{_sysconfdir}/bip.conf
%config %{_sysconfdir}/tmpfiles.d/bip.conf
%attr(-,bip,bip) %ghost %{_localstatedir}/run/bip
%attr(-,bip,bip) %dir %{_localstatedir}/log/bip
%{_unitdir}/bip.service

%pre
/usr/sbin/useradd -c "Bip IRC Proxy" \
  -s /bin/sh -r -d / bip 2> /dev/null || :

%post
%systemd_post bip.service
/bin/systemd-tmpfiles --create %{_sysconfdir}/tmpfiles.d/bip.conf

%preun
%systemd_preun bip.service

%postun
%systemd_postun_with_restart bip.service

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1
%patch1 -p1

iconv -f iso-8859-1 -t utf-8 -o ChangeLog{.utf8,}
mv ChangeLog{.utf8,}

%build
%configure2_5x --with-openssl
make CFLAGS="%{optflags} -fPIE -Wno-unused-result -Wstrict-aliasing=0"

%install
%makeinstall_std

# Remove misplaced files
rm -rf %{buildroot}%{_defaultdocdir}/bip
mkdir -p %{buildroot}%{_sysconfdir}
# Install bip.conf
install -m 0644 samples/bip.conf %{buildroot}%{_sysconfdir}/bip.conf
# Install bipgenconfig
install -m 0755 scripts/bipgenconfig %{buildroot}%{_bindir}/bipgenconfig
mkdir -p %{buildroot}%{_localstatedir}/run/bip
mkdir -p %{buildroot}%{_localstatedir}/log/bip

install -d -m 755 %{buildroot}%{_sysconfdir}/tmpfiles.d
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/tmpfiles.d/bip.conf

# Install systemd service file
install -d -m 755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/

