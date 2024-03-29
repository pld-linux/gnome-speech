# TODO:
# - build other speech plugins? (freetts, proprietary: viavoice, loquendo, dectalk, swift, theta, eloquence)
#
# Conditional build:
%bcond_without	festival	# Festival plugin
%bcond_without	java		# java subpackage
%bcond_without	static_libs	# static library

# requires Java >= 1.4 < 10 (idlj removed in Java 11, javah in Java 10)
%define		use_jdk		openjdk8

Summary:	GNOME Speech - text-to-speech convertion
Summary(pl.UTF-8):	GNOME Speech - przekształcanie tekstu na mowę
Name:		gnome-speech
Version:	0.4.25
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.gnome.org/sources/gnome-speech/0.4/%{name}-%{version}.tar.bz2
# Source0-md5:	89cbc23fc131c33396c0346085759f63
Patch0:		%{name}-jar_dir.patch
Patch1:		%{name}-common.patch
URL:		https://www.gnome.org/
BuildRequires:	ORBit2-devel >= 1:2.14.7
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	espeak-devel
BuildRequires:	gnome-common >= 2.18.0
BuildRequires:	gtk-doc >= 1.8
%if %{with java}
BuildRequires:	java-access-bridge >= 1.18.0
%buildrequires_jdk
%endif
BuildRequires:	libbonobo >= 2.18.0
BuildRequires:	libbonobo-devel >= 2.18.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.021
Requires:	gnome-speech-driver
Provides:	gnome_speech
Obsoletes:	gnome_speech < 0.2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Speech purpose is to provide a simple general API for producing
text-to-speech output.

%description -l pl.UTF-8
Celem GNOME Speech jest udostępnienie prostego, ogólnego API do
przekształcania tekstu na mowę.

%package driver-espeak
Summary:	Espeak TTS Speech Driver
Summary(pl.UTF-8):	Sterownik mowy ESpeak TTS
Group:		Libraries
Requires:	espeak
Provides:	gnome-speech-driver

%description driver-espeak
Provides text to speech services using the Espeak Speech Synthesis
System.

%description driver-espeak -l pl.UTF-8
Ten pakiet udostępnia usługę przekształcania tekstu na mowę przy
użyciu systemu syntezy mowy Espeak.

%package driver-festival
Summary:	Festival TTS Speech Driver
Summary(pl.UTF-8):	Sterownik mowy Festival TTS
Group:		Libraries
Requires:	festival
Provides:	gnome-speech-driver

%description driver-festival
Provides the text to speech services using the Festival Speech
Synthesis System.

%description driver-festival -l pl.UTF-8
Ten pakiet udostępnia usługę przekształcania tekstu na mowę przy
użyciu systemu syntezy mowy Festival.

%package driver-speech-dispatcher
Summary:	Speech Dispatcher driver
Summary(pl.UTF-8):	Sterownik mowy Speech Dispatcher
Group:		Libraries
Provides:	gnome-speech-driver

%description driver-speech-dispatcher
Provides the text to speech services using Speech Dispatcher.

%description driver-speech-dispatcher -l pl.UTF-8
Ten pakiet udostępnia usługę przekształcania tekstu na mowę przy
użyciu systemu Speech Dispatcher.

%package devel
Summary:	Development files for gnome_speech
Summary(pl.UTF-8):	Pliki programistyczne dla gnome_speech
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libbonobo-devel >= 2.18.0
Provides:	gnome_speech-devel
Obsoletes:	gnome_speech-devel < 0.2.2

%description devel
GNOME Speech files needed for development.

%description devel -l pl.UTF-8
Pliki GNOME Speech potrzebne do programowania.

%package static
Summary:	Static gnome-speech library
Summary(pl.UTF-8):	Statyczna biblioteka gnome-speech
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gnome-speech library.

%description static -l pl.UTF-8
Statyczna biblioteka gnome-speech.

%package java
Summary:	Java classes for gnome-speech
Summary(pl.UTF-8):	Klasy Java dla gnome-speech
Group:		Development/Languages/Java
Requires:	jpackage-utils

%description java
Java classes for gnome-speech.

%description java -l pl.UTF-8
Klasy Java dla gnome-speech.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--enable-gtk-doc \
	%{?with_static_libs:--enable-static} \
	--with-festival%{!?with_festival:=no} \
	%{?with_java:--with-jab-dir=%{_javadir}} \
	--with-java-home=%{java_home} \
	--with-speech-dispatcher

%{__make} \
	espeak_LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	orbittypelibdir=%{_libdir}/orbit-2.0 \
	DESTDIR=$RPM_BUILD_ROOT

# no *.la for orbit modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.a
%endif
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgnomespeech.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/test-speech
%attr(755,root,root) %{_libdir}/libgnomespeech.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnomespeech.so.7
%attr(755,root,root) %{_libdir}/orbit-2.0/GNOME_Speech_module.so

%files driver-espeak
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/espeak-synthesis-driver
%{_libdir}/bonobo/servers/GNOME_Speech_SynthesisDriver_Espeak.server

%if %{with festival}
%files driver-festival
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/festival-synthesis-driver
%{_libdir}/bonobo/servers/GNOME_Speech_SynthesisDriver_Festival.server
%endif

%files driver-speech-dispatcher
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/speechd-synthesis-driver
%{_libdir}/bonobo/servers/GNOME_Speech_SynthDriver_Speech_Dispatcher.server

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnomespeech.so
%{_includedir}/gnome-speech-1.0
%{_datadir}/idl/gnome-speech-1.0
%{_pkgconfigdir}/gnome-speech-1.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgnomespeech.a

%if %{with java}
%files java
%defattr(644,root,root,755)
%{_javadir}/*.jar
%endif
