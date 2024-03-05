Name: libmodi
Version: 20240305
Release: 1
Summary: Library to access Mac OS disk image formats
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libmodi
Requires: bzip2          openssl           xz-libs zlib
BuildRequires: gcc bzip2-devel          openssl-devel           xz-devel zlib-devel

%description -n libmodi
Library to access Mac OS disk image formats

%package -n libmodi-static
Summary: Library to access Mac OS disk image formats
Group: Development/Libraries
Requires: libmodi = %{version}-%{release}

%description -n libmodi-static
Static library version of libmodi.

%package -n libmodi-devel
Summary: Header files and libraries for developing applications for libmodi
Group: Development/Libraries
Requires: libmodi = %{version}-%{release}

%description -n libmodi-devel
Header files and libraries for developing applications for libmodi.

%package -n libmodi-python3
Summary: Python 3 bindings for libmodi
Group: System Environment/Libraries
Requires: libmodi = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libmodi-python3
Python 3 bindings for libmodi

%package -n libmodi-tools
Summary: Several tools for reading Mac OS disk images
Group: Applications/System
Requires: libmodi = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libmodi-tools
Several tools for reading Mac OS disk images

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libmodi
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libmodi-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libmodi-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libmodi.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libmodi-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libmodi-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Tue Mar  5 2024 Joachim Metz <joachim.metz@gmail.com> 20240305-1
- Auto-generated

