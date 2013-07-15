Summary:	An open-source cross-platform IP TV player
Name:		tano
Version:	1.2.1
Release:	2
License:	GPLv3+
Group:		Video
Url:		http://projects.tano.si/
# Generated by github https://github.com/ntadej/tano
Source0:	%{name}-%{version}.tar.gz
# Fix SOVERSION and VERSION wrong usage
Patch0:		tano-1.2.1-soname.patch
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(libvlc-qt)
BuildRequires:	pkgconfig(libvlc-qt-qml)
BuildRequires:	pkgconfig(libvlc-qt-widgets)
# In fact, it needs only plugins but they are packaged into main vlc package
Requires:	vlc

%description
Tano is an open-source cross-platform IP TV player. It features full IP TV
playback with EPG and recorder. Project started because of a need of a simple
IP TV player on Linux providing EPG.

Two network cards are recommended, one for TV and one for internet. One of
them must be wired. Connect TV to first, wired network card (eth0). Use second
network card that can be wireless for internet or ethernet. Classic Standard
Definition TV channels should play normally on any newer processors, but High
Definition TV channels need dual-core processor like Intel Core 2 or a graphics
card capable of hardware acceleration.

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png

#----------------------------------------------------------------------------

%define libtanocore_major 1
%define libtanocore %mklibname tanocore %{libtanocore_major}

%package -n %{libtanocore}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libtanocore}
Shared library for %{name}.

%files -n %{libtanocore}
%{_libdir}/libtanocore.so.%{libtanocore_major}*

#----------------------------------------------------------------------------

%define libtanowgt_major 1
%define libtanowgt %mklibname tanowidgets %{libtanowgt_major}

%package -n %{libtanowgt}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libtanowgt}
Shared library for %{name}.

%files -n %{libtanowgt}
%{_libdir}/libtanowidgets.so.%{libtanowgt_major}*

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1

%build
%cmake \
	-DDISABLE_UPDATE_CHECK:BOOL=ON \
	-DCMAKE_BUILD_TYPE=RelWithDebugInfo
# Parallel build is broken in 1.2.1
make

%install
%makeinstall_std -C build

# Remove wrong and not needed stuff
rm -rf %{buildroot}%{_iconsdir}/*
rm -f %{buildroot}%{_libdir}/libtanocore.so
rm -f %{buildroot}%{_libdir}/libtanowidgets.so

# install menu icons
for N in 48 64 128;
do
install -D -m 0644 data/logo/${N}x${N}/logo.png %{buildroot}%{_iconsdir}/hicolor/${N}x${N}/apps/%{name}.png
done
for N in 16 22 24 32;
do
convert data/logo/128x128/logo.png -resize ${N}x${N} $N.png;
install -D -m 0644 $N.png %{buildroot}%{_iconsdir}/hicolor/${N}x${N}/apps/%{name}.png
done

