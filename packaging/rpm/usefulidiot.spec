Name:           UsefulIdiot
Version:        0.1
Release:        1%{dist}
Summary:        A python re-implimentation of Netflix's Simian Army
License:        GPLv3
URL:            https://github.com/weaselkeeper/UsefulIdiot
Group:          System Environment/Base
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       python
Requires:       rpm-python
Requires:       python-argparse
Requires:	python-simplejson

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
cp -r ./src/plugins/* %{buildroot}%{_bindir}/usefulidiot/plugins/
cp -r ./src/UsefulIdiot.py %{buildroot}%{_bindir}/usefulidiot/
cp -r ./conf/* %{buildroot}%{_sysconfdir}/usefulidiot

%files
%{_bindir}/usefulidiot/*
%{_sysconfdir}/usefulidiot/*
%{_datadir}/usefulidiot/*

%pre

%post

%clean
rm -rf %{buildroot}

%changelog
* Thu Jan 10 2013 David Wahlstrom <dwahlstrom@classmates.com> - 0.1-1
- initial packaging of UsefulIdiot

