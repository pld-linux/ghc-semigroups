#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	semigroups
Summary:	Anything that associates
Summary(pl.UTF-8):	Wszystko, co łączne
Name:		ghc-%{pkgname}
Version:	0.12.1
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/semigroups
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	2c55dd7fc53559a7e2495e329fc6eebc
URL:		http://hackage.haskell.org/package/semigroups
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-bytestring < 0.11
BuildRequires:	ghc-containers >= 0.3
BuildRequires:	ghc-containers < 0.6
BuildRequires:	ghc-hashable >= 1.1
BuildRequires:	ghc-hashable < 1.3
BuildRequires:	ghc-nats >= 0.1
BuildRequires:	ghc-nats < 1
BuildRequires:	ghc-text >= 0.10
BuildRequires:	ghc-text < 1.1
BuildRequires:	ghc-unordered-containers >= 0.2
BuildRequires:	ghc-unordered-containers < 0.3
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-bytestring-prof < 0.11
BuildRequires:	ghc-containers-prof >= 0.3
BuildRequires:	ghc-containers-prof < 0.6
BuildRequires:	ghc-hashable-prof >= 1.1
BuildRequires:	ghc-hashable-prof < 1.3
BuildRequires:	ghc-nats-prof >= 0.1
BuildRequires:	ghc-nats-prof < 1
BuildRequires:	ghc-text-prof >= 0.10
BuildRequires:	ghc-text-prof < 1.1
BuildRequires:	ghc-unordered-containers-prof >= 0.2
BuildRequires:	ghc-unordered-containers-prof < 0.3
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3
Requires:	ghc-base < 5
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-bytestring < 0.11
Requires:	ghc-containers >= 0.3
Requires:	ghc-containers < 0.6
Requires:	ghc-hashable >= 1.1
Requires:	ghc-hashable < 1.3
Requires:	ghc-nats >= 0.1
Requires:	ghc-nats < 1
Requires:	ghc-text >= 0.10
Requires:	ghc-text < 1.1
Requires:	ghc-unordered-containers >= 0.2
Requires:	ghc-unordered-containers < 0.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
In mathematics, a semigroup is an algebraic structure consisting of a
set together with an associative binary operation. A semigroup
generalizes a monoid in that there might not exist an identity
element. It also (originally) generalized a group (a monoid with all
inverses) to a type where every element did not have to have an
inverse, thus the name semigroup.

%description -l pl.UTF-8
W matematyce półgrupa (semigroup) to struktura algebraiczna składająca
się ze zbioru wraz z działaniem dwuargumentowym łącznym. Półgrupa jest
uogólnieniem monoidu, w którym może nie istnieć element neutralny.
Pierwotnie była także uogólnieniem grupy (monoidu ze wszystkimi
elementami odwrotnymi) do typu, w którym każdy element nie musiał mieć
elementu odwrotnego - stąd nazwa półgrupa.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3
Requires:	ghc-base-prof < 5
Requires:	ghc-bytestring-prof >= 0.9
Requires:	ghc-bytestring-prof < 0.11
Requires:	ghc-containers-prof >= 0.3
Requires:	ghc-containers-prof < 0.6
Requires:	ghc-hashable-prof >= 1.1
Requires:	ghc-hashable-prof < 1.3
Requires:	ghc-nats-prof >= 0.1
Requires:	ghc-nats-prof < 1
Requires:	ghc-text-prof >= 0.10
Requires:	ghc-text-prof < 1.1
Requires:	ghc-unordered-containers-prof >= 0.2
Requires:	ghc-unordered-containers-prof < 0.3

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE README.markdown
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSsemigroups-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSsemigroups-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Semigroup.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List/NonEmpty.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSsemigroups-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Semigroup.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List/NonEmpty.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
