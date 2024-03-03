Name: libvmdk
Version: 20240303
Release: 1
Summary: Library to access the VMware Virtual Disk (VMDK) format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libvmdk
Requires:              zlib
BuildRequires: gcc              zlib-devel

%description -n libvmdk
Library to access the VMware Virtual Disk (VMDK) format

%package -n libvmdk-static
Summary: Library to access the VMware Virtual Disk (VMDK) format
Group: Development/Libraries
Requires: libvmdk = %{version}-%{release}

%description -n libvmdk-static
Static library version of libvmdk.

%package -n libvmdk-devel
Summary: Header files and libraries for developing applications for libvmdk
Group: Development/Libraries
Requires: libvmdk = %{version}-%{release}

%description -n libvmdk-devel
Header files and libraries for developing applications for libvmdk.

%package -n libvmdk-python3
Summary: Python 3 bindings for libvmdk
Group: System Environment/Libraries
Requires: libvmdk = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libvmdk-python3
Python 3 bindings for libvmdk

%package -n libvmdk-tools
Summary: Several tools for reading VMware Virtual Disk (VMDK) files
Group: Applications/System
Requires: libvmdk = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libvmdk-tools
Several tools for reading VMware Virtual Disk (VMDK) files

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

%files -n libvmdk
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libvmdk-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libvmdk-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libvmdk.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libvmdk-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libvmdk-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Mar  3 2024 Joachim Metz <joachim.metz@gmail.com> 20240303-1
- Auto-generated

