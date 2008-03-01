# TODO: rc.init,R

Summary:	OSSIM Agent
Summary(pl.UTF-8):	OSSIM Agent
Name:		ossim-agent
Version:	0.9.9
Release:	0.1
License:	BSD
Group:		Applications
Source0:	http://dl.sourceforge.net/os-sim/%{name}-%{version}.tar.gz
# Source0-md5:	711b2dec7bade734417bbdee4ac9ae2a
URL:		http://www.ossim.net/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OSSIM Agent - An agent in OSSIM is set of python script that gathers
and sends the output of the different plugin or tool to the
correlation engine for further process.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{ossim/agent,sysconfig,rc.d/init.d,logrotate.d}

python setup.py install --root=$RPM_BUILD_ROOT

install contrib/fedora/init.d/ossim-agent $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install etc/logrotate.d/ossim-agent $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install contrib/fedora/sysconfig/ossim-agent $RPM_BUILD_ROOT/etc/sysconfig/%{name}

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc doc/{ChangeLog,INSTALL,LICENSE,Leeme.ossim.snort.rtf,README.plugins,TODO,ossim-agent.xml}
# common OSSIM dir
%dir %{_sysconfdir}/ossim/agent
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ossim/agent/*.cfg
%dir %{_sysconfdir}/ossim/agent/plugins
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ossim/agent/plugins/*.cfg
%{_datadir}/%{name}/
%{_mandir}/man8/%{name}.*
%attr(755,root,root) %{_bindir}/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{py_sitescriptdir}/*.egg-info
