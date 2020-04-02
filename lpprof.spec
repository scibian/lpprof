%define name lpprof
%define version 0.2.2
%define unmangled_version 0.2.2
%define unmangled_version 0.2.2
%define release 1
%define debug_package %{nil}
%define __plugin lpprof
%define __lib_dir %{_prefix}/lib

Summary: Lightweight Performance profiler using Linux perf_events.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPLv3
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}
#BuildArch: noarch
Vendor: EDF CCN HPC <dsp-cspito-ccn-hpc@edf.fr>
Url: https://github.com/scibian/%{__plugin}

%if 0%{?rhel} >= 8
BuildRequires: git python36 slurm-devel python3-setuptools
Requires: python36 python3-jinja2
%else
BuildRequires: git python36 slurm-devel python36-setuptools
Requires: python36 python36-jinja2
%endif

%description
This package provides Lpprof software.
Lpprof is a parrallel profiling software using perf.

%prep
%setup -q
#[ -f %{_sourcedir}/%{name}-%{version}.tar.gz ] &&
##|| {
#    [ -d %{name}-%{version} ] || git clone %{url}.git %{name}-%{version}
#    cd %{name}-%{version} # for git
##}

%build
python3 setup.py build
cd spank
make

%install
#rm -rf %{buildroot} # for git
#cd %{name}-%{version} # for git
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot} --record=INSTALLED_FILES
#
install -d %{buildroot}%{__lib_dir}/slurm
#install -d %{buildroot}%{_sysconfdir}/slurm/plugstack.conf.d # for git
install -m 755 spank/%{__plugin}.so %{buildroot}%{__lib_dir}/slurm/
#install -m 644 plugstack.conf \ # for git
#    %%{buildroot}%{_sysconfdir}/slurm/plugstack.conf.d/%{__plugin}.conf

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root,-)

%package -n slurm-spank-plugin-%{__plugin}
Summary: Slurm SPANK plugin for parrallel profiling using perf
Requires: slurm lpprof
#BuildArch: x86-64

%description -n slurm-spank-plugin-%{__plugin}
This package provides Lpprof Slurm Spank plugin.
This plugin makes it easy to use Lpprof with SLURM
scheduler by providing --lpprof_f and --lpprof_r srun
arguments.

%files -n slurm-spank-plugin-%{__plugin}
%doc LICENSE
%defattr(-,root,root,-)
%{__lib_dir}/slurm/%{__plugin}.so
#%%config %{_sysconfdir}/slurm/plugstack.conf.d/%{__plugin}.conf

%changelog
* Fri Jan 28 2020 Kwame Amedodji <kamedodji@yahoo.fr> - 0.2.2-1
- port to centos of debian release
