%define lib_major 1
%define libname  %mklibname %{name} %{lib_major}
%define gdk_libname %mklibname gdkimlib %{lib_major}
%define develname %mklibname %{name} -d
%define gdk_develname %mklibname gdkimlib -d

Summary:	An image loading and rendering library
Name:		imlib
Version:	1.9.15
Release:	%mkrel 9
License:	LGPL
Group:		System/Libraries
BuildRequires:	gettext
BuildRequires:	gtk+-devel >= 1.2.1
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libungif-devel 
BuildRequires:	autoconf
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
Patch3:		imlib-1.9.15-no-locincpth.patch
Patch5:		imlib-1.9.13-secfixes.patch.bz2
Patch6:		imlib-1.9.14-fix-underquoted-calls.patch.bz2
Patch7:     imlib-1.9.15-max-24bpp.diff

# Comment to Source1 :
# I don't understand why official imlib dropped i18n support ?! all
# hooks are there though, only the po/ directory has been deleted

%description
Imlib is a display depth independent image loading and rendering library.
Imlib is designed to simplify and speed up the process of loading images
and obtaining X Window System drawables.  Imlib provides many simple
manipulation routines which can be used for common operations.  

Install imlib if you need an image loading and rendering library.
You may also want to install the imlib-cfgeditor package, which will help
you configure Imlib.

%package -n	%{libname}
Summary:	Main library for %{name} 
Group:		System/Libraries
Requires:	%{name}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Summary:	Includes and other files to develop %{name} applications
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version} libjpeg-devel libpng-devel libtiff-devel libungif-devel 
Provides:	lib%{name}-devel = %{version}
Provides:	imlib-devel = %{version}
Obsoletes:	imlib-devel
Obsoletes:	%{_lib}%{name}1-devel

%description -n	%{develname}
The header files, static libraries and documentation needed for
developing Imlib applications.  Imlib is an image loading and rendering
library.

Install the imlib-devel package if you want to develop Imlib applications.
You'll also need to install the imlib and imlib_cfgeditor packages.

%package -n	%{gdk_libname}
Summary:	GDK version of the imlib library
Group:          System/Libraries
Requires:       %{name}
Conflicts:	%{libname} < 1.9.15

%description -n %{gdk_libname}
This package contains the library needed to run programs dynamically
linked with the gdk version of %{name}.

%package -n     %{gdk_develname}
Summary:        Includes and other files to develop %{name} applications
Group:          Development/GNOME and GTK+
Requires:       %{gdk_libname} = %{version} %{develname} = %{version} libjpeg-devel libpng-devel libtiff-devel libungif-devel libgtk+-devel
Provides:       libgdk%{name}-devel = %{version}
Provides:       gdkimlib-devel = %{version}
Obsoletes:	%{_lib}gdkimlib1-devel

%description -n %{gdk_develname}
The header files, static libraries and documentation needed for
developing gdk_imlib applications.  gdk_imlib is an image loading and rendering
library.
	
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
%patch7 -p0

autoconf

%build
export X_LIBS="-lX11"

%define _disable_ld_no_undefined 1
%configure2_5x
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

%files 
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/*

%files -n %{libname}
%defattr(-, root, root)
%doc README
%attr(755,root,root) %{_libdir}/libImlib.so.*

%files -n %{gdk_libname}
%defattr(-, root, root)
%{_libdir}/libgdk_imlib.so.*
%{_libdir}/libimlib-*.so

%files cfgeditor -f %{name}.lang
%defattr(-,root,root)
%doc README
%{_bindir}/imlib_config
%{_mandir}/man1/imlib_config*

%files -n %{develname}
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

%files -n %{gdk_develname}
%defattr(-, root, root)
%{_includedir}/gdk_*
%{_libdir}/pkgconfig/imlibgdk.pc
%{_libdir}/libgdk_imlib.so
%{_libdir}/libgdk_imlib*a
%{_libdir}/libimlib-*a
