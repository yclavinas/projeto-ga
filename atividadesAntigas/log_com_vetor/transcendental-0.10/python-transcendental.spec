Name:         python-transcendental
Summary:      Python interface to the Cephes Transcendental Functions Library
Version:      0.05
Release:      1
Source0:      transcendental-%{version}.tar.gz
License:      BSD
Group:        Development/Libraries/Python
URL:          http://bonsai.ims.u-tokyo.ac.jp/~mdehoon/software/python/statistics.html
Requires:     python 
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
An extension module that gives access to the special functions available in
Cephes.  Unlike SciPy, this extension module is written in ANSI-C; its
compilation should therefore be straightforward (which was the main motivation
for this package).

%prep
%setup -n transcendental-%{version}

%build
export CFLAGS="$RPM_OPT_FLAGS" 
python setup.py build

%install
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES 
%defattr(-,root,root)
%doc HISTORY PKG-INFO README
