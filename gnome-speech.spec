
# TODO:
#	java package?
#	build other speech plugins?

%define	_snap	20030801
Summary:	GNOME Speech - text-to-speech convertion
Summary(pl):	GNOME Speech - przekszta³canie tekstu na mowê
Name:		gnome-speech
Version:	0.2.5
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/0.2/%{name}-%{version}.tar.bz2
# Source0-md5:	796ed911321d78813e3c9b740d1ff70b
#Source0:	%{name}-%{version}-%{_snap}.tar.bz2
Patch0:		%{name}-configure.patch
Patch1:		%{name}-nojava.patch
Patch2:		%{name}-am.patch
URL:		http://developer.gnome.org/projects/gap/
BuildRequires:	ORBit2-devel >= 2.7.6
BuildRequires:	autoconf
BuildRequires:	bonobo-activation-devel >= 0.9.1
BuildRequires:	libbonobo-devel >= 2.3.6
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
Requires:	%{name} = %{version}
Provides:	gnome_speech-devel
Obsoletes:	gnome_speech-devel

%description devel
Gnome speech files needed for development.

%description devel -l pl
Pliki Gnome speech potrzebne do programowania.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

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
