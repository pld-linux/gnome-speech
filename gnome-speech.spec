
# TODO:
#	java package?
#	build other speech plugins?

Summary:	GNOME Speech - text-to-speech convertion
Summary(pl):	GNOME Speech - przekszta�canie tekstu na mow�
Name:		gnome-speech
Version:	0.2.7
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/0.2/%{name}-%{version}.tar.bz2
# Source0-md5:	63669571096af17e495abbde890d19c6
Patch0:		%{name}-nojava.patch
Patch1:		%{name}-am.patch
URL:		http://developer.gnome.org/projects/gap/
BuildRequires:	ORBit2-devel >= 1:2.7.6
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-common
BuildRequires:	libbonobo-devel >= 2.3.6
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
Celem GNOME Speech jest udost�pnienie prostego, og�lnego API do
przekszta�cania tekstu na mow�.

%package devel
Summary:	Development files for gnome_speech
Summary(pl):	Pliki programistyczne dla gnome_speech
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	libbonobo-devel >= 2.3.6
Provides:	gnome_speech-devel
Obsoletes:	gnome_speech-devel

%description devel
GNOME Speech files needed for development.

%description devel -l pl
Pliki GNOME Speech potrzebne do programowania.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
%{__autoheader}
%{__automake}
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	orbittypelibdir=%{_libdir}/orbit-2.0 \
	DESTDIR=$RPM_BUILD_ROOT

# no *.la for orbit modules
rm -f $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/festival-synthesis-driver
%attr(755,root,root) %{_bindir}/test-speech
%attr(755,root,root) %{_libdir}/libgnomespeech.so.*.*.*
%{_libdir}/bonobo/servers/*.server
%{_libdir}/orbit-2.0/*.so*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnomespeech.so
%{_libdir}/libgnomespeech.la
%{_includedir}/gnome-speech-1.0
%{_datadir}/idl/gnome-speech-1.0
%{_pkgconfigdir}/*.pc
