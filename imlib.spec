%bcond_with gtk1
%define url_ver %(echo %{version}|cut -d. -f1,2)

%define major 1
%define libname  %mklibname %{name} %{major}
%define libgdkname %mklibname gdkimlib %{major}
%define devname %mklibname %{name} -d
%define devgdkname %mklibname gdkimlib -d

Summary:	An image loading and rendering library
Name:		imlib
Version:	1.9.15
Release:	16
License:	LGPLv2
Group:		System/Libraries
Url:		http://www.enlightenment.org/Libraries/Imlib/	
Source0:	http://ftp.gnome.org/pub/GNOME/sources/imlib/%{url_ver}/%{name}-%{version}.tar.gz
Source1:	imlib-pofiles.tar.bz2
Patch0:		imlib-1.9-m4.patch
Patch1:		imlib-1.9.11-i18n.patch
Patch2:		imlib-1.9.10-path.patch
Patch3:		imlib-1.9.15-no-locincpth.patch
Patch5:		imlib-1.9.13-secfixes.patch
Patch6:		imlib-1.9.14-fix-underquoted-calls.patch
Patch7:		imlib-1.9.15-max-24bpp.diff
Patch8:		imlib-1.9.15-link.patch
Patch9:		imlib-1.9.15-libpng15.diff
Patch10:	PrintGifError_renamed_to_GifErrorString_4.2.1.patch
Patch11:	imlib-1.9.15-giflib5.patch
Patch12:	imlib-1.9.15-no-gtk1.patch

BuildRequires:	chrpath
BuildRequires:	gettext
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	ungif-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(x11)
Provides:	Imlib

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

%package -n	%{devname}
Summary:	Includes and other files to develop %{name} applications
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
The header files, static libraries and documentation needed for
developing Imlib applications.  Imlib is an image loading and rendering
library.

Install the imlib-devel package if you want to develop Imlib applications.
You'll also need to install the imlib and imlib_cfgeditor packages.

%package -n	%{libgdkname}
Summary:	GDK version of the imlib library
Group:		System/Libraries
Requires:	%{name}

%description -n %{libgdkname}
This package contains the library needed to run programs dynamically
linked with the gdk version of %{name}.

%package -n	%{devgdkname}
Summary:	Includes and other files to develop %{name} applications
Group:		Development/GNOME and GTK+
Requires:	%{libgdkname} = %{version}-%{release}
Requires:	%{devname} = %{version}-%{release}
Provides:	gdkimlib-devel = %{version}-%{release}

%description -n %{devgdkname}
The header files, static libraries and documentation needed for
developing gdk_imlib applications.  gdk_imlib is an image loading and rendering
library.
	
%package cfgeditor
Summary:	A configuration editor for the Imlib library
Group:		System/Libraries
Requires:	%{name}

%description	cfgeditor
The imlib-cfgeditor package contains the imlib_config program, which you
can use to configure the Imlib image loading and rendering library.
Imlib_config can be used to control how Imlib uses color and handles
gamma corrections, etc.

If you're installing the imlib package, you should also install
imlib_cfgeditor.

%prep
%setup  -q
%apply_patches
autoreconf -fi

%build
%configure2_5x \
	--disable-gtktest \
	--disable-static
%make LIBS="-lgif"

%install
%makeinstall_std

# some hand dealing for locale
tar jxvf %{SOURCE1}
for i in po/*.po ; do
  mkdir -p %{buildroot}%{_datadir}/locale/`basename $i .po`/LC_MESSAGES
  msgfmt -v -o %{buildroot}%{_datadir}/locale/`basename $i .po`/LC_MESSAGES/imlib.mo $i
done

%if %{without gtk1}
# Locales are only for the cfgeditor
rm -rf %buildroot%_datadir/locale
# And the pkgconfig file for imlibgdk shouldn't be installed either
rm -f %buildroot%_libdir/pkgconfig/imlibgdk.pc
%endif

%multiarch_binaries %{buildroot}%{_bindir}/imlib-config

# (sb) rpmlint
%if %{with gtk1}
chrpath -d %{buildroot}%{_bindir}/imlib_config
%endif
chrpath -d %{buildroot}%{_libdir}/*.so*

%find_lang %{name} || touch %name.lang

%files
%config(noreplace) %{_sysconfdir}/*

%if %{with gtk1}
%files cfgeditor -f %{name}.lang
%{_bindir}/imlib_config
%{_mandir}/man1/imlib_config*

%files -n %{libgdkname}
%{_libdir}/libgdk_imlib.so.%{major}*

%files -n %{devgdkname}
%{_includedir}/gdk_*
%{_libdir}/pkgconfig/imlibgdk.pc
%{_libdir}/libgdk_imlib.so
%endif

%files -n %{libname}
%{_libdir}/libImlib.so.%{major}*

%files -n %{devname}
%doc doc/*.gif doc/*.html README AUTHORS ChangeLog
%{_bindir}/imlib-config
%{multiarch_bindir}/imlib-config
%{_includedir}/Imlib*
%{_datadir}/aclocal/*
%{_libdir}/libImlib.so
%{_libdir}/pkgconfig/imlib.pc
%{_mandir}/man1/imlib-config*
