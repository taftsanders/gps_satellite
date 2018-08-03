Name: gps-satellite
Version: 2.0	
Release: 2%{?dist}
Summary: Satellite 6 multi-functional troubleshooting tool	
Group: Applications/File	
License: GPLv3	
URL: http://splinter.usersys.redhat.com:3000/taft/gps-satellite
Source0: gps-satellite-2.0.tar
BuildRequires: python	
Requires: python	

%description
Red Hat Satellite 6 multi-functional troubleshooting tool

%prep
%setup -q

%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/lib64/python2.7
mkdir -p $RPM_BUILD_ROOT%{_doc}

cp gps_satellite.py ${RPM_BUILD_ROOT}/usr/lib64/python2.7
cp pulp_api.py ${RPM_BUILD_ROOT}/usr/lib64/python2.7
cp satellite_monitor.py ${RPM_BUILD_ROOT}/usr/lib64/python2.7
cp menu.py ${RPM_BUILD_ROOT}/usr/bin/gps_satellite
cp LICENSE CHANGELOG $RPM_BUILD_ROOT%{_doc} 

chmod +x ${RPM_BUILD_ROOT}/usr/bin/gps_satellite

%files
/usr/bin/gps_satellite
/usr/lib64/python2.7/*
%doc CHANGELOG LICENSE

%changelog
* Fri Aug 03 2018 Taft Sanders <tasander@redhat.com> - 2.0.2
- Resolved qpid cert path error not found

* Wed Aug 01 2018 Taft Sanders <tasander@redhat.com> - 2.0.1
- Added Satellite performance monitoring feature

* Thu May 24 2018 Taft Sanders <tasander@redhat.com> - 1.0-16
- Added activation-key arg
- Included GET for individual hosts

* Fri May 18 2018 Taft Sanders <tasander@redhat.com> - 1.0-15
- Added pulp-api calls
- Auto populate local server hostname

* Wed Dec 13 2017 Taft Sanders <tasander@redhat.com> - 1.0-1
- Created first package.
