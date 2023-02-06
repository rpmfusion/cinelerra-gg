%global git_tag 2023-01
%global tag_version %(c=%{git_tag}; echo "${c}" | tr '-' '.')

Name:           cinelerra-gg
Version:        5.1%{?tag_version:.%{tag_version}}
Release:        1%{?dist}
Summary:        A non linear video editor and effects processor
# The Cinelerra-GG codebase is licensed GPLv2+
# The GREYcstoration plugin is licensed CeCILL v2.0
# The Google SHA1 implementation is licensed BSD 3-clause
# The Neophyte theme is licensed Creative Commons CC-BY 4.0
# The freeverb components and the Tapeworm font are in the public Domain
License:        GPLv2+ and CeCILL and BSD and CC-BY and Public Domain
Url:            https://cinelerra-gg.org/
Source0:        https://git.cinelerra-gg.org/git/?p=goodguy/cinelerra.git;a=snapshot;sf=tgz;h=refs/tags/%{git_tag}#/%{name}-%{git_tag}.tar.gz

# CrystalHD is fouling the ffmpeg build
Patch0:         cinelerra-gg-Disable-crystalhd-in-ffmpeg.patch

# Only tested on x86_64
ExclusiveArch:  x86_64

BuildRequires:  autoconf-archive
BuildRequires:  cmake
BuildRequires:  ctags
BuildRequires:  curl
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  libtool
BuildRequires:  nasm
BuildRequires:  perl-interpreter
BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python-unversioned-command
BuildRequires:  texinfo
BuildRequires:  udftools
BuildRequires:  wget
BuildRequires:  yasm

BuildRequires:  CImg-devel
BuildRequires:  jbigkit-devel
BuildRequires:  kernel-headers
BuildRequires:  lame-devel
BuildRequires:  pulseaudio-utils
BuildRequires:  perl(XML::LibXML)
BuildRequires:  perl(XML::Parser)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(aom)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(dav1d)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(IlmBase)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libdv)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(lilv-0)
BuildRequires:  pkgconfig(lv2)
BuildRequires:  pkgconfig(mjpegtools)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(numa)
#BuildRequires:  pkgconfig(opencv)
BuildRequires:  pkgconfig(OpenEXR)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(serd-0)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(sord-0)
BuildRequires:  pkgconfig(sratom-0)
BuildRequires:  pkgconfig(suil-0)
BuildRequires:  pkgconfig(theora)
BuildRequires:  pkgconfig(twolame)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(x264)
BuildRequires:  pkgconfig(x265)
BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xv)

#Disabled until opencv_contrib-freeworld is introduced
#Requires: python2-opencv

# Obsolete cinelerra(-cv)
Obsoletes: cinelerra < %{version}-%{release}
Provides: cinelerra = %{version}-%{release}
Obsoletes: cinelerra-cv < %{version}-%{release}
Provides: cinelerra-cv = %{version}-%{release}

# Require HTML documentation
Requires: %{name}-doc = %{version}-%{release}

%global _description\
Non-linear audio/video authoring tool Cinelerra-GG is a complete audio and\
video authoring tool. It understands a lot of multimedia formats as quicktime,\
avi, ogg also audio/video compression codecs divx, xvid, mpeg2.\
\
This is the "goodguy" version of Cinelerra.

%description %_description


%package doc
Summary:        Documentation files for %{name}
BuildArch:      noarch

%description doc %_description


%prep
%autosetup -p1 -n cinelerra-%{git_tag}

cd cinelerra-5.1
./autogen.sh

%build

# Temporarily turn off hardening (just for the configure step), as
# it breaks OpenEXR detection. It'll be re-enabled before building.
%undefine _hardened_build

cd cinelerra-5.1
%configure \
  --with-exec-name=%{name} \
  --disable-static-build \
  --enable-a52dec=yes \
  --enable-dav1d=auto \
  --enable-flac=yes \
  --enable-fftw=auto \
  --enable-ilmBase=shared \
  --enable-lame=auto \
  --enable-libaom=auto \
  --enable-libdv=auto \
  --enable-libjpeg=auto \
  --enable-libogg=auto \
  --enable-libsndfile=auto \
  --enable-libtheora=auto \
  --enable-libvorbis=auto \
  --enable-libvpx=auto \
  --enable-libwebp=auto \
  --enable-lilv=shared \
  --enable-lv2=shared \
  --enable-openjpeg=auto \
  --enable-openexr=shared \
  --enable-openExr=shared \
  --enable-opus=auto \
  --enable-serd=shared \
  --enable-sord=shared \
  --enable-sratom=shared \
  --enable-suil=shared \
  --enable-tiff=auto \
  --enable-twolame=auto \
  --enable-x264=auto \
  --enable-x265=auto \
  --with-browser=xdg-open \
  --without-cuda \
  --without-firewire \
  --without-ladspa-build \
  --with-ladspa-dir=%{_libdir}/ladspa \
  --without-opencv \
  --with-openexr \
  --with-pulse \

# WIP
#  --with-dv=no \
#  --enable-giflib=no \
#  --enable-flac=no \
#  --enable-libuuid=no \
#  --with-opencv=sys \
#  --with-thirdparty=no \
#  --with-commercial=no \
#  --with-libzmpeg=no \

# Re-enable hardening
%define _hardened_build 1

%make_build V=0


%install
pushd cinelerra-5.1
%make_install V=0
popd

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%files -f %{name}.lang
%license cinelerra-5.1/COPYING
%license cinelerra-5.1/plugins/theme_neophyte/Neophyte_License.txt
%doc cinelerra-5.1/README
%{_bindir}/%{name}
%{_bindir}/zmpeg3cc2txt
%{_bindir}/zmpeg3ifochk
%{_bindir}/bdwrite
%{_datadir}/%{name}/
%exclude %{_datadir}/%{name}/doc
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.svg
%{_datadir}/pixmaps/%{name}.xpm

%files doc
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/doc


%changelog
* Mon Feb 06 2023 Leigh Scott <leigh123linux@gmail.com> - 5.1.2023.01-1
- Update to latest monthly release

* Mon Feb 06 2023 Nicolas Chauvet <kwizart@gmail.com> - 5.1.2022.11-3
- Add missing autoconf-archive - rhbz#6570

* Fri Dec 16 2022 Leigh Scott <leigh123linux@gmail.com> - 5.1.2022.11-2
- Add missing build requires

* Fri Dec 16 2022 Leigh Scott <leigh123linux@gmail.com> - 5.1.2022.11-1
- Update to latest monthly release

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 5.1.2022.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Jun 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 5.1.2022.05-2
- Rebuilt for new AOM and libavif

* Mon Jun 13 2022 Leigh Scott <leigh123linux@gmail.com> - 5.1.2022.05-1
- Update to latest monthly release

* Fri May 27 2022 Leigh Scott <leigh123linux@gmail.com> - 5.1.2022.04-1
- Update to latest monthly release

* Tue Apr 26 2022 Leigh Scott <leigh123linux@gmail.com> - 5.1.2022.03-1
- Update to latest monthly release

* Mon Feb 07 2022 Leigh Scott <leigh123linux@gmail.com> - 5.1.2020.10-6
- Rebuild for libvpx

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.1.2020.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jun 13 2021 Robert-André Mauchin <zebob.m@gmail.com> - 5.1.2020.10-4
- Rebuild for new aom

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.1.2020.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Leigh Scott <leigh123linux@gmail.com> - 5.1.2020.10-2
- Actually do the dav1d rebuild

* Sat Dec 05 2020 FeRD (Frank Dana) <ferdnyc@gmail.com> - 5.1.2020.10-1
- New upstream monthly release
- Add GCC 11 patch for internal OpenEXR

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.1.2020.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Aug 04 2020 FeRD (Frank Dana) <ferdnyc@gmail.com> - 5.1.2020.07-1
- Update to latest monthly release
- Drop upstreamed patch

* Tue Jul 07 2020 FeRD (Frank Dana) <ferdnyc@gmail.com> - 5.1.2020.06-3
- Update configure.ac patch to fix all interdependency checks
- Use shared libs for some parts of IlmBase (OpenEXR dependency)
- Enable pulseaudio support

* Tue Jul 07 2020 FeRD (Frank Dana) <ferdnyc@gmail.com> - 5.1.2020.06-2
- Switch to shared liblilv (also removes its build dependencies from
  the build: serd, sord, sratom, suil)

* Sat Jul 04 2020 FeRD (Frank Dana) <ferdnyc@gmail.com> - 5.1.2020.06-1
- New upstream release, migrate to new package versioning
- Patch all bundled Python code to run with python3

* Sun May 24 2020 Leigh Scott <leigh123linux@gmail.com> - 5.1-59.20191231git3878a69
- Rebuild for dav1d SONAME bump

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.1-58.20191231git3878a69
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 01 2020 FeRD (Frank Dana) <ferdnyc@gmail.com> - 5.1-56.20191231git3878a69
- New upstream 2019-12 snapshot release, switch to .tar.bz2 archives
- Drop upstreamed patches, rebase crystalhd patch
- Enable LV2 plugin support

* Fri Aug 30 2019 FeRD (Frank Dana) <ferdnyc@gmail.com> - 5.1-56.20190801gitb8cd5c4
- Update to 2019-08 snapshot version
- Add libusb build req
- Remove crystalhd from ffmpeg (build fails), turn off CUDA checks (no compiler) 
- Replace 'python' command with 'python3' in guicast Makefile
- Add patch for glibc >= 2.30 gettid() (submitted upstream)

* Mon Aug 26 2019 FeRD (Frank Dana) <ferdnyc@gmail.com> - 5.1-55.20181217gitd5a0afb
- Update to 5.1 snapshot with python3 build process
- Switch to -gg
- ExclusiveArch x86_64
- Add -doc subpackage

* Thu Feb 18 2016 Sérgio Basto <sergio@serjux.com> - 2.3-9.20160216git5aa9bc2
- Fix undefined-non-weak-symbols on libguicast.so .
- Add 0001-Do-not-ask-for-specific-Microsoft-fonts.patch is what left from
  patch: "Remove bundle fonts and fix font search path" and was not accepted
  upstream.

* Fri Jan 15 2016 Sérgio Basto <sergio@serjux.com> - 2.3-8.20160216git5aa9bc2
- AutoTools replace the obsoleted AC_PROG_LIBTOOL, patch7.
- To fix hardened linkage, patch8.
- More reviews like replace RPM_BUILD_ROOT, own directories, more documentation,
  description-line-too-long errors.

* Thu Jan 14 2016 Sérgio Basto <sergio@serjux.com> - 2.3-7.20160114git454be60
- Update license tag.
- Add license macro.
- use macro make_build .
- use macro make_install .
- Improve conditional builds.

* Mon Oct 26 2015 Sérgio Basto <sergio@serjux.com> - 2.3-6.20151026git99d2887
- Update to git 99d2887, drop cinelerra-cv-remove-fonts.patch is was applied upstream.

* Mon Oct 05 2015 Sérgio Basto <sergio@serjux.com> - 2.3-5.20151005gitd189a04
- Update to git d189a04

* Tue Sep 29 2015 Sérgio Basto <sergio@serjux.com> - 2.3-4.20150929git2c849c6
- Drop upstreamed cinelerra-cv-intltoolize.patch

* Tue Sep 15 2015 Sérgio Basto <sergio@serjux.com> - 2.3-3.20150912gitc25d3b1
- Applied cinelerra-cv-intltoolize.patch

* Mon Sep 14 2015 Sérgio Basto <sergio@serjux.com> - 2.3-2.20150912gitc25d3b1
- Enabled findobject plugin using OpenCV 2.0 .
- Fix unknown freetype2 option, an configure warning.

* Sun Sep 13 2015 Sérgio Basto <sergio@serjux.com> - 2.3-1.20150912gitc25d3b1
- Update cinelerra-cv to 2.3 more a few commits.

* Wed Dec 24 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.9.20141224git70b8c14
- Update to 20141224git70b8c14

* Sun Oct 12 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1.20141012git623e87e-1
- Update to git623e87e

* Sat Sep 27 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.8.20140927git9cbf7f0
- Update to cinelerra-cv-2.2.1-20140927git9cbf7f0

* Sun Jul 27 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.7.20140727git92dba16
- Update to 20140727 git 92dba16 .

* Sun May 25 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.5.20140525gitef4fddb
- Update to git ef4fddb
- Added cinelerra-cv-ffmpeg_api2.2.patch and cinelerra-cv-ffmpeg2.0.patch and build with external ffmpeg.
- make it work --with or --without libmpeg3_system and ffmpeg_system.

* Wed Apr 30 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.3.20140426git9154825
- Added imlib2-devel as BR to build vhook/imlib2.so

* Tue Apr 29 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.2.20140426git9154825
- Drop a file in /etc/sysctl.d instead to tweaking /etc/sysctl.conf
- Removed gcc-g++ as BR
- Use libmpeg3 from system
- Remove bundle fonts and fix font search path
- Scriptlet for desktop-database
- Disabled 3dnow
- Program-suffix -cv

* Mon Apr 28 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.1
- Initial spec, copied from David Vasquez and changed based on
  cinelerra-f15.spec from Atrpms and also changed based on
  openmamba/devel/specs/cinelerra-cv.spec

* Mon Sep 30 2013 David Vasquez <davidjeremias82@gmail.com> - 2.2-1
- Initial package creation for Fedora 19
- Spec inspirated in PKGBUILD Arch Linux
- Add freeing more shared memory from RPM Fusion
