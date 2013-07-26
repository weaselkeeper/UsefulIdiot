Name:           usefulidiot
Version:        0.3
Release:        %{dist}
Summary:        A python re-implimentation of Netflix's Simian Army
License:        GPLv3
URL:            https://github.com/weaselkeeper/UsefulIdiot
Group:          System Environment/Base
Source0:        %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       python
Requires:       rpm-python
Requires:       python-argparse
Requires:       python-simplejson

%description
A plugable framework to create chaos on your network. Designed to be used with
Ansible. UsefulIdiot will help pinpoint areas where you need to improve
automation, documentation and/or monitoring.

%prep
%setup -q -n %{name}

%install
rm -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_bindir}/usefulidiot
%{__mkdir_p} %{buildroot}%{_sysconfdir}/usefulidiot
%{__mkdir_p} %{buildroot}%{_datadir}/usefulidiot/plugins
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/usefulidiot
cp -r ./plugins/*.py %{buildroot}%{_datadir}/usefulidiot/plugins/
cp -r ./UsefulIdiot.py %{buildroot}%{_bindir}/usefulidiot/
cp -r ./config/* %{buildroot}%{_sysconfdir}/usefulidiot

%files
%{_bindir}/usefulidiot/*
%{_sysconfdir}/usefulidiot/*
%{_datadir}/usefulidiot/*

%pre

%post

%clean
rm -rf %{buildroot}

%changelog
* Sat Jul 06 2013 Jim Richardson <weaselkeeper@gmail.com> - 0.3
- Added runpuppet plugin, plus numerous changes to __main__ Also added config reading.
* Wed Jun 26 2013 Jim Richardson <weaselkeeper@gmail.com> - 0.2
- Added a couple plugins, cronripper,runpuppet, and reboot
* Thu Jan 10 2013 David Wahlstrom <dwahlstrom@classmates.com> - 0.1-1
- initial packaging of UsefulIdiot
