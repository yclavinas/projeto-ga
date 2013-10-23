Summary: CSEP Generic Distribution
Name: csep
Version: 13.4.0
Release: 1
Source: %{name}-%{version}.tar.gz
License: GPL
Vendor: SCEC
URL: www.cseptesting.org
Group: Development/Tools
Prefix: /usr/local

%global install_dir %{prefix}/%{name}-%{version}

%description
Distribution of the CSEP generic codes to the testing centers. The package includes 
authorized data sources as used by the CSEP Testing Center at SCEC (ANSS, CMT).

%prep
%setup -q

%build
make
chmod -R a+w src/generic/test/data

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot}/%{install_dir} install
cp NEWS %{buildroot}/%{install_dir}

%clean
rm -rf %{buildroot}

%files
%{install_dir}
