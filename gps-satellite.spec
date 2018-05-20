Name: gps-satellite
Version: 1.0	
Release: 15%{?dist}
Summary: Satellite 6 mapping tool	
Group: Applications/File	
License: GPLv3	
URL: http://splinter.usersys.redhat.com:3000/taft/gps-satellite
Source0: gps-satellite-1.0.tar
BuildRequires: python	
Requires: python	

%description
Red Hat Satellite 6 mapping tool

%prep
%setup -q

%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/lib64/python2.7
mkdir -p $RPM_BUILD_ROOT%{_doc}

cp gps_satellite.py ${RPM_BUILD_ROOT}/usr/bin
cp pulp_api.py ${RPM_BUILD_ROOT}/usr/lib64/python2.7
cp LICENSE CHANGELOG $RPM_BUILD_ROOT%{_doc} 

chmod +x ${RPM_BUILD_ROOT}/usr/bin/gps_satellite.py

%files
/usr/bin/gps_satellite.py
/usr/lib64/python2.7/*
%doc CHANGELOG LICENSE

%changelog
* Fri May 18 2018 Taft Sanders <tasander@redhat.com> - 1.0-15
- Added pulp-api calls
- Auto populate local server hostname

* Wed Dec 13 2017 Taft Sanders <tasander@redhat.com> - 1.0-1
- Created first package.
