%define lib_major 1
%define libname  %mklibname %{name} %{lib_major}
%define gdk_libname %mklibname gdkimlib %{lib_major}
%define develname %mklibname %{name} -d
%define gdk_develname %mklibname gdkimlib -d

Summary:	An image loading and rendering library
Name:		imlib
Version:	1.9.15
Release:	14
License:	LGPL
Group:		System/Libraries
URL:		http://www.enlightenment.org/Libraries/Imlib/	
Source0:	ftp://ftp.gnome.org/pub/GNOME/stable/sources/imlib/1.9/%{name}-%{version}.tar.bz2
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
BuildRequires:	gettext
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(gtk+)
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	ungif-devel
BuildRequires:	autoconf
BuildRequires:	chrpath
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

%package -n	%{develname}
Summary:	Includes and other files to develop %{name} applications
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	imlib-devel = %{version}-%{release}

%description -n	%{develname}
The header files, static libraries and documentation needed for
developing Imlib applications.  Imlib is an image loading and rendering
library.

Install the imlib-devel package if you want to develop Imlib applications.
You'll also need to install the imlib and imlib_cfgeditor packages.

%package -n	%{gdk_libname}
Summary:	GDK version of the imlib library
Group:		System/Libraries
Requires:	%{name}

%description -n %{gdk_libname}
This package contains the library needed to run programs dynamically
linked with the gdk version of %{name}.

%package -n	%{gdk_develname}
Summary:	Includes and other files to develop %{name} applications
Group:		Development/GNOME and GTK+
Requires:	%{gdk_libname} = %{version}-%{release}
Requires:	%{develname} = %{version}-%{release}
Provides:	libgdk%{name}-devel = %{version}-%{release}
Provides:	gdkimlib-devel = %{version}-%{release}

%description -n %{gdk_develname}
The header files, static libraries and documentation needed for
developing gdk_imlib applications.  gdk_imlib is an image loading and rendering
library.
	
%package	cfgeditor
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
%patch0 -p0 -b .m4ver
%patch1 -p1 -b .i18n
%patch2 -p1 -b .path
%patch3 -p1 -b .no-locincpth
%patch5 -p1 -b .can-2004-1025_1026
%patch6 -p1 -b .underquoted
%patch7 -p0
%patch8 -p1 -b .link
%patch9 -p1 -b .libpng15

%build
autoreconf -fi
%configure2_5x --disable-gtktest --disable-static
%make

%install
%makeinstall_std

# some hand dealing for locale
tar jxvf %{SOURCE1}
for i in po/*.po ; do
  mkdir -p %{buildroot}%{_datadir}/locale/`basename $i .po`/LC_MESSAGES
  msgfmt -v -o %{buildroot}%{_datadir}/locale/`basename $i .po`/LC_MESSAGES/imlib.mo $i
done

%multiarch_binaries %{buildroot}%{_bindir}/imlib-config

# (sb) rpmlint
chrpath -d %{buildroot}%{_bindir}/imlib_config
chrpath -d %{buildroot}%{_libdir}/*.so*

%find_lang %{name}

%files
%doc README AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/*

%files -n %{libname}
%doc README
%attr(755,root,root) %{_libdir}/libImlib.so.%{lib_major}*

%files -n %{gdk_libname}
%{_libdir}/libgdk_imlib.so.%{lib_major}*

%files cfgeditor -f %{name}.lang
%doc README
%{_bindir}/imlib_config
%{_mandir}/man1/imlib_config*

%files -n %{develname}
%doc doc/*.gif doc/*.html README AUTHORS ChangeLog
%{_bindir}/imlib-config
%multiarch %{multiarch_bindir}/imlib-config

%{_mandir}/man1/imlib-config*
# note, the blank line above is needed due to some borked rpm5 macro
%{_includedir}/Imlib*
%{_datadir}/aclocal/*
%{_libdir}/libImlib.so
%{_libdir}/pkgconfig/imlib.pc

%files -n %{gdk_develname}
%{_includedir}/gdk_*
%{_libdir}/pkgconfig/imlibgdk.pc
%{_libdir}/libgdk_imlib.so


%changelog
* Tue Dec 06 2011 Götz Waschk <waschk@mandriva.org> 1.9.15-13mdv2012.0
+ Revision: 738277
- rebuild

* Tue Oct 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.9.15-12
+ Revision: 702709
- "fix" build
- fix build against libpng-1.5.x (gentoo)

* Sat Feb 05 2011 Funda Wang <fwang@mandriva.org> 1.9.15-11
+ Revision: 636087
- bunzip2 the patches
- fix linkage of share libs and pkg-config files

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.9.15-10mdv2011.0
+ Revision: 611183
- rebuild

* Mon Feb 15 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 1.9.15-9mdv2010.1
+ Revision: 506174
- Add patch fixing Imlib render

* Sun Aug 16 2009 Götz Waschk <waschk@mandriva.org> 1.9.15-8mdv2010.0
+ Revision: 416903
- rediff patch 3
- fix build

* Fri Jul 11 2008 Oden Eriksson <oeriksson@mandriva.com> 1.9.15-7mdv2009.0
+ Revision: 233959
- fix build

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 1.9.15-5mdv2008.1
+ Revision: 150285
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Jul 09 2007 Andreas Hasenack <andreas@mandriva.com> 1.9.15-4mdv2008.0
+ Revision: 50584
- fix gdk devel requires

* Sat Jul 07 2007 Adam Williamson <awilliamson@mandriva.org> 1.9.15-3mdv2008.0
+ Revision: 49520
- rebuild for 2008
- unversion autoconf dependency (works fine with current version)
- new devel policy
- clean descriptions a little
- Import imlib



* Fri Aug 11 2006 Stew Benedict <sbenedict@mandriva.com> 1.9.15-2mdv2007.0
- gdk library needs to conflict with old libimlib1

* Tue Aug 01 2006 Cris B <cris AT beebgames DOT org> 1.9.15-1mdv2007.0
- New version
- Drop patch 4 (merged upstream)
- Split gdk and non_gdk version of library
- (sb) rpmlint

* Wed Jun 21 2006 Götz Waschk <waschk@mandriva.org> 1.9.14-14mdk
- Rebuild

* Wed Jan 25 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.9.14-13mdk
- fix underquoted calls (P6)
- %%mkrel

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.9.14-12mdk
- Rebuild

* Mon Jan 31 2005 Frederic Lepied <flepied@mandrakesoft.com> 1.9.14-11mdk
- security fixes for CAN-2004-1025 and CAN-2004-1026

* Fri Oct 08 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.9.14-10mdk
- Patch4: security fix for CAN-2004-0817

* Tue Jun 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.9.14-9mdk
- fix buildrequires
- cosmetics

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.9.14-8mdk
- mklibname

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.9.14-7mdk
- Rebuild

* Fri May 23 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 1.9.14-6mdk
- rebuild with ta.po in UTF-8
- new translations

* Thu Sep  5 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 1.9.14-5mdk
- rebuild to include latest translations

* Wed Jul 31 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.9.14-4mdk
- Update patch3 to remove -L/usr/lib to ldflags

* Sat Jun 22 2002 Stefan van der Eijk <stefan@eijk.nu> 1.9.14-3mdk
- BuildRequires

* Mon Apr 29 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.9.14-2mdk
- Re-enable parallel build, it's fine now
- Patch3: Fix build with gcc-3.1+. Don't include known system dirs
  into include search path. That would have caused the configury to
  fail for some checks.

* Fri Apr 19 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.9.14-1mdk
- Release 1.9.14

* Wed Mar 20 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.9.13-1mdk
- Release 1.9.13
- Disable parallel compilation, it is broken

* Thu Feb 14 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 1.9.11-9mdk
- added various new translations

* Mon Dec  3 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.9.11-8mdk
- Remove Stefan hack, it causes bad .la files

* Wed Oct 10 2001 Jesse Kuang <kjx@mandrakesoft.com> 1.9.11-7mdk
- rebuilt against libpng.so.3

* Mon Oct 08 2001 Stefan van der Eijk <stefan@eijk.nu> 1.9.11-6mdk
- add hack to allow imlib to build without itself installed
- Removed redundantBuildRequires

* Wed Aug 22 2001 dam's <damien@mandrakesoft.com> 1.9.11-5mdk
- added provides

* Thu Aug 16 2001 dam's <damien@mandrakesoft.com> 1.9.11-4mdk
- removed useless menu entry for imlib_config_editor

* Sat Aug 11 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 1.9.11-3mdk
- added various new translations

* Sat Aug 04 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.9.11-2mdk
- Add a list of Requires for the development package (Abel).

* Fri Aug  3 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.9.11-1mdk
- Release 1.9.11
- Regenerate patch1
- Fix menu entry

* Mon May 28 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.9.10-7mdk
- Force generation of configure with latest libtool
- Add libimlib-*.so back. They must stay in main package
- Add pkgconfig files

* Sat May 26 2001 Stefan van der Eijk <stefan@eijk.nu> 1.9.10-6mdk
- remove %%{_libdir}/libimlib-*.so --> typo + duplicates the line above.

* Thu Apr 12 2001 Fran�ois Pons <fpons@mandrakesoft.com> 1.9.10-5mdk
- Add patch to take care of environment GDK_IMLIB_PATH.

* Tue Apr 10 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.9.10-4mdk
- Fix the %%postun script. Stupid typo.

* Tue Apr 10 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.9.10-3mdk
- Correct obsoletes for smooth upgrade

* Mon Apr  9 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.9.10-2mdk
- Add menu entry to cfgeditor (from gnome-core)

* Tue Apr  3 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.9.10-1mdk
- Release 1.9.10

* Tue Mar 27 2001 dam's <damien@mandrakesoft.com> 1.9.9-2mdk
- added require on imlib for libimlib

* Sat Feb 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.9.9-1mdk
- Imlib 1.9.9 is out for general consumption.
- make %%setup quiet so we don't get a whole crapload of stuff to the output.

* Thu Jan 18 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 1.9.8.1-10mdk
- Added new languages (Gaeilge, Azeri, Afrikaans, Japanese, Serbian, Brazilian,
  Latvian, Russian, Lituanian, Turkish)

* Fri Jan 12 2001 dam's <damien@mandrakesoft.com> 1.9.8.1-9mdk
- corrected bad version.

* Thu Dec 07 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.9.8.1-8mdk
- add provides: imlib-devel.

* Tue Nov 28 2000 dam's <damien@mandrakesoft.com> 1.9.8.1-7mdk
- imlib-profiles sourced
- new lib policy

* Sat Sep 30 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.9.8.1-6mdk
- added gtk+-devel BuildRequires.

* Mon Sep 11 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.9.8.1-5mdk
- rebuilt to have the correct provides.

* Mon Sep 11 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 1.9.8.1-4mdk
- Added new languages (Slovak, Czech, Hungarian, Esperanto, Bulgarian,
  Vietnamese and Russian) 

* Fri Sep  8 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 1.9.8.1-3mdk
- Correct build dependency (Thanks Pedro Rosa)
- Use find_lang macro

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.9.8.1-2mdk
- automatically added BuildRequires

* Fri Jul 21 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 1.9.8.1-1mdk
- release 1.9.8.1
- BM, macroszification
- clean spec

* Tue May 02 2000 Warly <warly@mandrakesoft.com> 1.9.8-10mdk
- rebuild to have good provides

* Sat Apr 29 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 1.9.8-9mdk
- Added new langs: Lithuanian, Esperanto, Finnish, Slovakian, Norwegian,
  Bulgarian, Galician, Danish and Croatian

* Wed Mar 22 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 1.9.8-8mdk
- new Groups: naming
- rebuild with new gtk+/glib libs
- added German, Bulgarian, Dutch and Chinese interfaces

* Fri Feb 25 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 7mdk
- several new and improved translations

* Mon Jan 24 2000 Pablo Saratxaga <pablo@mandrakesoft.com>
- added Portuguese interface

* Tue Jan 18 2000 Pablo Saratxaga <pablo@mandrakesoft.com>
- added da, ca languages

* Fri Nov 05 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- added hu, id, it, pl, ro, uk translations

* Sun Oct 31 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Sane SMP build

* Sun Oct 24 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 1.9.8

* Fri Sep 24 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 1.9.7

* Tue Jul 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix bug with palettes reported by Rudi Pittman
(famewolf@georgia.army.net).

* Mon Jul 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Building release (3mdk).

* Thu Jul 08 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- imlib_config has i18n support; simply it isn't used (I don't knwo why);
  I just enabled it back and included the spanish translation file

* Mon Jun 28 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add patch to upgrade the imlib.m4 to the proper version.
- we strip binary with our macros.
- 1.9.5 version.

* Fri Apr 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adpatations.

* Tue Apr 06 1999 Michael Fulbright <drmike@redhat.com>
- quiet imlib when initializing

* Sun Mar 28 1999 Michael Fulbright <drmike@redhat.com>
- added development requirements for imlib-devel

* Fri Mar 19 1999 Michael Fulbright <drmike@redhat.com>
- strip binaries

* Thu Feb 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.9.4, moved %%{_sysconfdir} to %%{_sysconfdir}

* Fri Feb 12 1999 Michael Fulbright <drmike@redhat.com>
- version 1.9.3

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- build against gtk+ 1.1.14

* Mon Jan 25 1999 Michael Fulbright <drmike@redhat.com>
- fixed file list to include lib_imlib*.so in main pkg, not devel pkg

* Wed Jan 20 1999 Michael Fulbright <drmike@redhat.com>
- moved to version 1.9.2

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- moved to version 1.9.1, main feature - dyn loading of image
  support libs - saves memory and speeds startup of apps.

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- moved imlib-config moved to devel package
- new version of gtk+ forced us to rebuild imlib

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- up to 1.8.2 in prep for GNOME freeze

* Wed Sep 23 1998 Carsten Haitzler <raster@redhat.com>
- up to 1.8.1

* Tue Sep 22 1998 Cristian Gafton <gafton@redhat.com>
- yet another build for today (%%defattr and %%attr in the files lists)
- devel docs are back on the spec file

* Tue Sep 22 1998 Carsten Haitzler <raster@redhat.com>
- Added minor patch for ps saving code.

* Mon Sep 21 1998 Cristian Gafton <gafton@redhat.com>
- updated to version 1.8

* Fri Sep 11 1998 Cristian Gafton <gafton@redhat.com>
- take out imlib_config from devel package

* Wed Sep 9 1998 Michael Fulbright <msf@redhat.com>
- upgraded to 1.7
- changed name so it will persist if user later install devel imlib
- added subpackage for imlib_config

* Fri Apr 3 1998 Michael K. Johnson <johnsonm@redhat.com>
- fixed typo

* Fri Mar 13 1998 Marc Ewing <marc@redhat.com>
- Added -k, Obsoletes
- Integrate into CVS source tree
