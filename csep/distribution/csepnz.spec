Summary: CSEP New Zealand Distribution
Name: csepnz
Version: 13.4.0
Release: 1
Source0: %{name}-%{version}.tar.gz
License: GPL
Vendor: SCEC
URL: www.cseptesting.org
Group: Development/Tools
Prefix: /usr/local

%global install_dir %{prefix}/csep-%{version}

%description
Distribution of the CSEP New Zealand codes to the testing center. The package includes 
authorized data source GeoNetNZ used by the center, and definition of the 
geographical region for New Zealand testing center.

%prep
%setup -q

%build
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot}/%{install_dir} install

%clean
rm -rf %{buildroot}

%files
%{install_dir}
