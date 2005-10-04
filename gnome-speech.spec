# TODO:
# - build other speech plugins?
#
# Conditional build:
%bcond_with	java		# build java subpackage
#
Summary:	GNOME Speech - text-to-speech convertion
Summary(pl):	GNOME Speech - przekszta³canie tekstu na mowê
Name:		gnome-speech
Version:	0.3.8
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-speech/0.3/%{name}-%{version}.tar.bz2
# Source0-md5:	b5e85e71d24babe169cb1a37e4fbcae2
Patch0:		%{name}-jar_dir.patch
URL:		http://developer.gnome.org/projects/gap/
BuildRequires:	ORBit2-devel >= 1:2.12.1
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gtk-doc >= 1.3
%if %{with java}
BuildRequires:	jar
BuildRequires:	java
BuildRequires:	java-access-bridge
%endif
BuildRequires:	libbonobo-devel >= 2.8.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	festival >= 1.4.2
Provides:	gnome_speech
Obsoletes:	gnome_speech
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Speech purpose is to provide a simple general API for producing
text-to-speech output.

%description -l pl
Celem GNOME Speech jest udostêpnienie prostego, ogólnego API do
przekszta³cania tekstu na mowê.

%package devel
Summary:	Development files for gnome_speech
Summary(pl):	Pliki programistyczne dla gnome_speech
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libbonobo-devel >= 2.8.1
Provides:	gnome_speech-devel
Obsoletes:	gnome_speech-devel

%description devel
GNOME Speech files needed for development.

%description devel -l pl
Pliki GNOME Speech potrzebne do programowania.

%package static
Summary:	Static gnome-speech library
Summary(pl):	Statyczna biblioteka gnome-speech
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gnome-speech library.

%description static -l pl
Statyczna biblioteka gnome-speech.

%package java
Summary:	Java classes for gnome-speech
Summary(pl):	Klasy Java dla gnome-speech
Group:		Development/Libraries

%description java
Java classes for gnome-speech.

%description java -l pl
Klasy Java dla gnome-speech.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--enable-static \
	--enable-gtk-doc \
	%{?with_java:--with-jab-dir=%{_datadir}/java}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	orbittypelibdir=%{_libdir}/orbit-2.0 \
	DESTDIR=$RPM_BUILD_ROOT

# no *.la for orbit modules
rm -f $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/festival-synthesis-driver
%attr(755,root,root) %{_bindir}/test-speech
%attr(755,root,root) %{_libdir}/libgnomespeech.so.*.*.*
%attr(755,root,root) %{_libdir}/orbit-2.0/*.so*
%{_libdir}/bonobo/servers/*.server

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnomespeech.so
%{_libdir}/libgnomespeech.la
%{_includedir}/gnome-speech-1.0
%{_datadir}/idl/gnome-speech-1.0
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{with java}
%files java
%defattr(644,root,root,755)
%{_datadir}/java/*.jar
%endif
