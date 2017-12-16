Name: gps-satellite
Version: 1.0	
Release: 14%{?dist}
Summary: Satellite 6 mapping tool	
Group: Applications/File	
License: GPLv3	
URL: http://splinter.usersys.redhat.com:3000/taft/gps-satellite
Source0: gps-satellite.tar
BuildRequires: python	
Requires: python	

%description
Red Hat Satellite 6 mapping tool

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_doc}

cp gps_satellite.py $RPM_BUILD_ROOT%{_bindir}/gps-satellite
cp LICENSE CHANGELOG $RPM_BUILD_ROOT%{_doc} 

chmod +x $RPM_BUILD_ROOT%{_bindir}/gps-satellite

%files
%{_bindir}/gps-satellite
%doc CHANGELOG LICENSE

%changelog
* Wed Dec 13 2017 Taft Sanders <tsanders@redhat.com> - 1.0-1
- Created first package.
