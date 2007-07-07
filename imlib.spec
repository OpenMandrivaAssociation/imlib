%define lib_major 1
%define lib_name  %mklibname %{name} %{lib_major}
%define gdk_lib_name %mklibname gdkimlib %{lib_major}

Summary:	An image loading and rendering library for X11R6
Name:		imlib
Version:	1.9.15
Release:	%mkrel 2
License:	LGPL
Group:		System/Libraries
BuildRequires:	gettext
BuildRequires:	gtk+-devel >= 1.2.1
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libungif-devel autoconf2.1
BuildRequires:	chrpath
Source0:	ftp://ftp.gnome.org/pub/GNOME/stable/sources/imlib/1.9/%{name}-%{version}.tar.bz2
Source1:	imlib-pofiles.tar.bz2
Obsoletes:	Imlib
Provides:	Imlib
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.enlightenment.org/Libraries/Imlib/	

Patch0:		imlib-1.9-m4.patch.bz2
Patch1:		imlib-1.9.11-i18n.patch.bz2
Patch2:		imlib-1.9.10-path.patch.bz2
Patch3:		imlib-1.9.14-no-locincpth.patch.bz2
Patch5:		imlib-1.9.13-secfixes.patch.bz2
Patch6:		imlib-1.9.14-fix-underquoted-calls.patch.bz2

# Comment to Source1 :
# I don't understand why official imlib dropped i18n support ?! all
# hooks are there though, only the po/ directory has been deleted

%description
Imlib is a display depth independent image loading and rendering library.
Imlib is designed to simplify and speed up the process of loading images
and obtaining X Window System drawables.  Imlib provides many simple
manipulation routines which can be used for common operations.  

Install imlib if you need an image loading and rendering library for X11R6.
You may also want to install the imlib-cfgeditor package, which will help
you configure Imlib.

%package -n	%{lib_name}
Summary:	Main library for %{name} 
Group:		System/Libraries
Requires:	%{name}

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{lib_name}-devel
Summary:	Includes and other files to develop %{name} applications
Group:		Development/GNOME and GTK+
Requires:	%{lib_name} = %{version} libjpeg-devel libpng-devel libtiff-devel libungif-devel 
Provides:	lib%{name}-devel = %{version}
Provides:	imlib-devel = %{version}
Obsoletes:	imlib-devel

%description -n	%{lib_name}-devel
The header files, static libraries and documentation needed for
developing Imlib applications.  Imlib is an image loading and rendering
library for X11R6.

Install the imlib-devel package if you want to develop Imlib applications.
You'll also need to install the imlib and imlib_cfgeditor packages.

%package -n	%{gdk_lib_name}
Summary:	GDK version of the imlib library
Group:          System/Libraries
Requires:       %{name}
Conflicts:	%{lib_name} < 1.9.15

%description -n %{gdk_lib_name}
This package contains the library needed to run programs dynamically
linked with the gdk version of %{name}.

%package -n     %{gdk_lib_name}-devel
Summary:        Includes and other files to develop %{name} applications
Group:          Development/GNOME and GTK+
Requires:       %{gdk_lib_name} = %{version} %{lib_name}-devel = %{version} libjpeg-devel libpng-devel libtiff-devel libungif-devel libgtk+-devel
Provides:       libgdk%{name}-devel = %{version}
Provides:       gdkimlib-devel = %{version}

%description -n %{gdk_lib_name}-devel
The header files, static libraries and documentation needed for
developing gdk_imlib applications.  gdk_imlib is an image loading and rendering
library for X11R6.
	
%package	cfgeditor
Summary:	A configuration editor for the Imlib library
Group:		System/Libraries
Requires:	imlib = %{version}

%description	cfgeditor
The imlib-cfgeditor package contains the imlib_config program, which you
can use to configure the Imlib image loading and rendering library.
Imlib_config can be used to control how Imlib uses color and handles
gamma corrections, etc.

If you're installing the imlib package, you should also install
imlib_cfgeditor.

%prep
%setup  -q
%patch0 -p0 -b .m4ver 
%patch1 -p1 -b .i18n
%patch2 -p1 -b .path
%patch3 -p1 -b .no-locincpth
%patch5 -p1 -b .can-2004-1025_1026
%patch6 -p1 -b .underquoted
autoconf

# this is needed to avoid running libtoolize -- pablo
#define __libtoolize  /bin/true

%build
%configure
%make 

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

# some hand dealing for locale
tar jxvf %{SOURCE1}
for i in po/*.po ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/`basename $i .po`/LC_MESSAGES
  msgfmt -v -o $RPM_BUILD_ROOT%{_datadir}/locale/`basename $i .po`/LC_MESSAGES/imlib.mo $i
done

%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/imlib-config

# (sb) rpmlint
chrpath -d $RPM_BUILD_ROOT%{_bindir}/imlib_config
chrpath -d $RPM_BUILD_ROOT%{_libdir}/*.so*

%{find_lang} %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_name} -p /sbin/ldconfig
%post -n %{gdk_lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig
%postun -n %{gdk_lib_name} -p /sbin/ldconfig

%files 
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/*

%files -n %{lib_name}
%defattr(-, root, root)
%doc README
%attr(755,root,root) %{_libdir}/libImlib.so.*

%files -n %{gdk_lib_name}
%defattr(-, root, root)
%{_libdir}/libgdk_imlib.so.*
%{_libdir}/libimlib-*.so

%files cfgeditor -f %{name}.lang
%defattr(-,root,root)
%doc README
%{_bindir}/imlib_config
%{_mandir}/man1/imlib_config*

%files -n %{lib_name}-devel
%defattr(-, root, root)
%doc doc/*.gif doc/*.html README AUTHORS ChangeLog
%{_bindir}/imlib-config
%multiarch %{multiarch_bindir}/imlib-config
%{_mandir}/man1/imlib-config*
%{_libdir}/libImlib*a
%{_includedir}/Imlib*
%{_datadir}/aclocal/*
%{_libdir}/libImlib.so
%{_libdir}/pkgconfig/imlib.pc

%files -n %{gdk_lib_name}-devel
%defattr(-, root, root)
%{_includedir}/gdk_*
%{_libdir}/pkgconfig/imlibgdk.pc
%{_libdir}/libgdk_imlib.so
%{_libdir}/libgdk_imlib*a
%{_libdir}/libimlib-*a
