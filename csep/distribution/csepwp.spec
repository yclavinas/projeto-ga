Summary: CSEP Distribution of the Western Pacific testing region
Name: csepwp
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
Distribution of the CSEP codes for the Western Pacific testing region.

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
