%global optflags %{optflags} -Wno-incompatible-function-pointer-types
%global optflags %{optflags} -O2

# "fix" underlinking:
%define _disable_ld_no_undefined 1

%define up_name		freerdp2

%define winpr_major	2
%define uwac_major	0
%define major		2
%define libname		%mklibname %{name}
%define develname	%mklibname %{name} -d

%define oname		FreeRDP
%define tarballver	%{version}
%define tarballdir	v%{version}

# Momentarily disable GSS support
# https://github.com/FreeRDP/FreeRDP/issues/4348
%bcond_with	gss

# Use only one of this
%bcond_with	mbedtls
%bcond_without	openssl

# disable packages in restricted repo
%bcond_with	faac
%bcond_with	faad
%bcond_with	x264

Name:		freerdp2
Version:	2.11.7
Release:	3
Summary:	A free remote desktop protocol client
License:	Apache License
Group:		Networking/Remote access
Url:		https://www.freerdp.com/
Source0:	https://github.com/FreeRDP/FreeRDP/archive/%{tarballver}/%{oname}-%{tarballver}.tar.gz
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	docbook-style-xsl
BuildRequires:	xmlto
BuildRequires:	cups-devel
%if %{with faac}
BuildRequires:	faac-devel
%endif
BuildRequires:	ffmpeg-devel
BuildRequires:	gsm-devel
BuildRequires:	lame-devel
%if %{with mbedtls}
BuildRequires:	mbedtls-devel
%endif
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(alsa)
%if %{with faac}
BuildRequires:	pkgconfig(faad2)
%endif
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-base-1.0)
BuildRequires:	pkgconfig(gstreamer-app-1.0)
BuildRequires:	pkgconfig(gstreamer-audio-1.0)
BuildRequires:	pkgconfig(gstreamer-fft-1.0)
BuildRequires:	pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:	pkgconfig(gstreamer-video-1.0)
BuildRequires:	pkgconfig(icu-i18n)
%if %{with gss}
BuildRequires:  pkgconfig(krb5) >= 1.13
%endif
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libpcsclite)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(OpenCL)
BuildRequires:	pkgconfig(openh264)
%if %{with openssl}
BuildRequires:	pkgconfig(openssl)
%endif
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sox)
BuildRequires:	pkgconfig(soxr)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-scanner)
%if %{with x264}
BuildRequires:	pkgconfig(x264)
%endif
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(zlib)

%description
FreeRDP is a fork of the rdesktop project.

#----------------------------------------------------

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
# ease for update
Conflicts:	%{mklibname freerdp 1} < 1.2.0-5
Conflicts:	%{mklibname freerdp 2}

%description -n %{libname}
Shared libraries for %{name}.

%files -n %{libname}
%{_libdir}/%{name}*/
%{_libdir}/lib*%{name}*.so.%{major}*
%{_libdir}/libfreerdp-client2.so.%{major}*
%{_libdir}/libwinpr*.so.%{winpr_major}*
%{_libdir}/libuwac*.so.%{uwac_major}*

#----------------------------------------------------

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{develname}
Development files and headers for %{name}.

%files -n %{develname}
%{_libdir}/*.so
%{_includedir}/%{up_name}/
%{_includedir}/winpr*/
%{_includedir}/uwac*/
%{_libdir}/pkgconfig/freerdp-client2.pc
%{_libdir}/pkgconfig/%{name}*.pc
%{_libdir}/pkgconfig/winpr*.pc
%{_libdir}/pkgconfig/uwac*.pc
%{_libdir}/cmake/FreeRDP*/
%{_libdir}/cmake/WinPR*/
%{_libdir}/cmake/uwac*/

#----------------------------------------------------

%prep
%setup -qn FreeRDP-%{tarballver}
%autopatch -p1

%build
%cmake \
	-DWITH_ALSA:BOOL=ON \
	-DWITH_CUPS:BOOL=ON \
	-DWITH_CHANNELS:BOOL=ON \
	-DBUILTIN_CHANNELS:BOOL=OFF \
	-DWITH_CLIENT:BOOL=OFF \
        -DWITH_CLIENT_SDL:BOOL=OFF \
	-DWITH_DIRECTFB:BOOL=OFF \
	-DWITH_FAAC:BOOL=%{?with_faac:ON}%{?!with_faac:OFF} \
	-DWITH_FAAD2:BOOL=%{?with_faad:ON}%{?!with_faad:OFF} \
	-DWITH_FFMPEG:BOOL=ON \
	-DWITH_GSM:BOOL=ON \
	-DWITH_GSSAPI:BOOL=%{?_with_gss:ON}%{?!_with_gss:OFF} \
	-DWITH_GSTREAMER_1_0:BOOL=ON -DWITH_GSTREAMER_0_10:BOOL=OFF \
	-DGSTREAMER_1_0_INCLUDE_DIRS=%{_includedir}/gstreamer-1.0 \
	-DWITH_ICU:BOOL=ON \
	-DWITH_IPP:BOOL=OFF \
	-DWITH_JPEG:BOOL=ON \
	-DWITH_LAME:BOOL=ON \
	-DWITH_MANPAGES:BOOL=OFF \
	-DWITH_OPENCL:BOOL=ON \
	-DWITH_OPENH264:BOOL=ON \
	-DWITH_OPENSSL:BOOL=%{?with_openssl:ON}%{?!with_openssl:OFF} \
	-DWITH_MBEDTLS:BOOL=%{?with_mbedtls:ON}%{?!with_mbedtls:OFF} \
	-DWITH_PCSC:BOOL=ON \
	-DWITH_PULSE:BOOL=ON \
	-DWITH_SERVER:BOOL=OFF -DWITH_SERVER_INTERFACE:BOOL=OFF \
	-DWITH_SHADOW_X11:BOOL=ON -DWITH_SHADOW_MAC:BOOL=ON \
	-DWITH_SOXR:BOOL=ON \
%ifarch %{x86_64}
	-DWITH_SSE2:BOOL=ON \
%else
	-DWITH_SSE2:BOOL=OFF \
%endif
	-DWITH_WAYLAND:BOOL=ON \
	-DWITH_VAAPI:BOOL=ON \
	-DWITH_X264:BOOL=%{?with_x264:ON}%{?!with_x264:OFF} \
	-DWITH_X11:BOOL=ON \
	-DWITH_XCURSOR:BOOL=ON \
	-DWITH_XEXT:BOOL=ON \
	-DWITH_XKBFILE:BOOL=ON \
	-DWITH_XI:BOOL=ON \
	-DWITH_XINERAMA:BOOL=ON \
	-DWITH_XRENDER:BOOL=ON \
	-DWITH_XTEST:BOOL=OFF \
	-DWITH_XV:BOOL=ON \
	-DWITH_ZLIB:BOOL=ON \
%ifarch armv7hl
	-DARM_FP_ABI=hard \
	-DWITH_NEON:BOOL=OFF \
%endif
%ifarch armv7hnl
	-DARM_FP_ABI=hard \
	-DWITH_NEON:BOOL=ON \
%endif
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# we don't want these
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

# Delete executables we do not need
rm -rfv %{buildroot}%{_bindir}

