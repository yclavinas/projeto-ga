Summary: CSEP Distribution of the Oceanic Transform Faults testing region
Name: csepoceanic
Version: 13.4.0
Release: 1
Source0: %{name}-%{version}.tar.gz
License: GPL
Vendor: SCEC
URL: www.cseptesting.org
Group: Development/Tools
Prefix: /usr/local

%define install_dir %{prefix}/csep-%{version}

%description
Distribution of the CSEP codes for the Oceanic Transform Faults testing region.

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
