## ruby-1.9.spec
## Copyright (c) 2009 Mu Dynamics, Inc. <http://mudynamics.com>
## Port to CentOS/RHEL4 from the OpenPKG spec file:
## Copyright (c) 2000-2009 OpenPKG Foundation e.V. <http://openpkg.net/>
##
##  Permission to use, copy, modify, and distribute this software for
##  any purpose with or without fee is hereby granted, provided that
##  the above copyright notice and this permission notice appear in all
##  copies.
##
##  THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED
##  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
##  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
##  IN NO EVENT SHALL THE AUTHORS AND COPYRIGHT HOLDERS AND THEIR
##  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
##  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
##  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
##  USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
##  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
##  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
##  OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
##  SUCH DAMAGE.
##

#   package versions
%define       V_dist   1.9.1-p243
%define       V_subdir 1.9.1-p243
%define       V_opkg   1.9.1p243

%define	rubyxver	1.9
%define	rubyver		1.9.1
%define _patchlevel	243
%define dotpatchlevel	%{?_patchlevel:.%{_patchlevel}}
%define patchlevel	%{?_patchlevel:-p%{_patchlevel}}
%define	arcver		%{rubyver}%{?patchlevel}
%define	sitedir		%{_libdir}/ruby%{rubyxver}/site_ruby
%define	_normalized_cpu	%(echo `echo %{_target_cpu} | sed 's/^ppc/powerpc/'`)
%define	sitedir2	%{_prefix}/lib/ruby%{rubyxver}/site_ruby


#   package information
Name:         ruby1.9
Summary:      The Ruby Scripting Language
URL:          http://www.ruby-lang.org/
Vendor:       Yukihiro 'Matz' Matsumoto
Packager:     Mu Dynamics, Inc.
Distribution: MuCOS
#Class:        BASE
Group:        Language
License:      GPL
Version:      %{V_opkg}
Release:      3

#   list of sources
Source0:      ftp://ftp.ruby-lang.org/pub/ruby/ruby-%{V_dist}.tar.gz

#   build information
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildPreReq:  ncurses, openssl, readline, zlib, make, gcc
PreReq:       ncurses, openssl, readline, zlib

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.


%package libs
Summary:	Libraries necessary to run Ruby
Group:		Development/Libraries
Provides:	ruby1.9(abi) = %{rubyxver}
Provides:	libruby1.9 = %{version}-%{release}
Obsoletes:	libruby1.9 <= %{version}-%{release}

%description libs
This package includes the libruby, necessary to run Ruby.


%package devel
Summary:	A Ruby development environment
Group:		Development/Languages
Requires:	libruby1.9 = %{version}-%{release}
Provides:	libruby1.9-static = %{version}-%{release}

%description devel
Header files and libraries for building a extension library for the
Ruby or an application embedded Ruby.


%package tcltk
Summary:	Tcl/Tk interface for scripting language Ruby
Group:		Development/Languages
Requires:	libruby1.9 = %{version}-%{release}

%description tcltk
Tcl/Tk interface for the object-oriented scripting language Ruby.


%package irb
Summary:	The Interactive Ruby
Group:		Development/Languages
Requires:	ruby1.9 = %{version}-%{release}
Provides:	irb1.9 = %{version}-%{release}
Obsoletes:	irb1.9 <= %{version}-%{release}

%description irb
The irb is acronym for Interactive Ruby.  It evaluates ruby expression
from the terminal.


%package rdoc
Summary:	A tool to generate documentation from Ruby source files
Group:		Development/Languages
Requires:	ruby1.9 = %{version}-%{release}
Requires:	irb1.9 = %{version}-%{release}
Provides:	rdoc1.9 = %{version}-%{release}
Obsoletes:	rdoc1.9 <= %{version}-%{release}

%description rdoc
The rdoc is a tool to generate the documentation from Ruby source files.
It supports some output formats, like HTML, Ruby interactive reference (ri),
XML and Windows Help file (chm).


%package docs
Summary:	Manuals and FAQs for scripting language Ruby
Group:		Documentation

%description docs
Manuals and FAQs for the object-oriented scripting language Ruby.


%package ri
Summary:	Ruby interactive reference
Group:		Documentation
Requires:	rdoc1.9 = %{version}-%{release}
Provides:	ri1.9 = %{version}-%{release}
Obsoletes:	ri1.9 <= %{version}-%{release}

%description ri
ri is a command line tool that displays descriptions of built-in
Ruby methods, classes and modules. For methods, it shows you the calling
sequence and a description. For classes and modules, it shows a synopsis
along with a list of the methods the class or module implements.


%prep
%setup -n ruby-%{V_dist}

%build
CFLAGS="$RPM_OPT_FLAGS -Wall"
export CFLAGS

# FIXME: tk/tcl isn't build with thread support, so if you're going to use that with 
# ruby, then you need to disable pthread support
%configure \
  --with-static-linked-ext \
  --enable-shared  \
  --with-ruby-version=full \
  --enable-pthread \
  --program-suffix=%{rubyxver}

make

%install
    rm -rf $RPM_BUILD_ROOT
    make  DESTDIR=$RPM_BUILD_ROOT install

%clean
    rm -rf $RPM_BUILD_ROOT

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc COPYING*
%doc ChangeLog
%doc GPL
%doc LEGAL
%doc LGPL
%doc NEWS 
%doc README
%lang(ja) %doc README.ja
%doc ToDo 
%doc doc/ChangeLog-1.8.0
%doc doc/NEWS-1.8.7
%{_bindir}/ruby1.9
%{_bindir}/gem1.9
%{_bindir}/rake1.9
%{_bindir}/erb1.9
%{_bindir}/testrb1.9
%{_mandir}/man1/ruby1.9.1*
%{_mandir}/man1/erb1.9.1*
%{_mandir}/man1/rake1.9.1*
%{_mandir}/man1/ri1.9.1*

%files devel
%defattr(-, root, root, -)
%doc COPYING*
%doc ChangeLog
%doc GPL
%doc LEGAL
%doc LGPL
%doc README.EXT
%lang(ja) %doc README.EXT.ja
%{_libdir}/libruby%{rubyxver}-static.a
%{_includedir}/ruby%{rubyxver}-%{rubyver}/*.h
%{_includedir}/ruby%{rubyxver}-%{rubyver}/*/*.h
%{_includedir}/ruby%{rubyxver}-%{rubyver}/*/*/*.h

%files libs
%defattr(-, root, root, -)
%doc README COPYING* ChangeLog GPL LEGAL LGPL
%lang(ja) %doc README.ja

%{_libdir}/ruby%{rubyxver}/%{rubyver}/json
#%{_libdir}/ruby%{rubyxver}/%{rubyver}/json/pure
%{_libdir}/ruby%{rubyxver}/%{rubyver}/json/add
%{_libdir}/ruby%{rubyxver}/%{rubyver}/minitest
%{_libdir}/ruby%{rubyxver}/%{rubyver}/rake
%{_libdir}/ruby%{rubyxver}/%{rubyver}/rbconfig
%{_libdir}/ruby%{rubyxver}/%{rubyver}/ripper
%{_libdir}/ruby%{rubyxver}/%{rubyver}/rubygems
%{_libdir}/ruby%{rubyxver}/%{rubyver}/rubygems/commands
%{_libdir}/ruby%{rubyxver}/%{rubyver}/rubygems/ext
%{_libdir}/ruby%{rubyxver}/%{rubyver}/rubygems/indexer
%{_libdir}/ruby%{rubyxver}/%{rubyver}/rubygems/package
%{_libdir}/ruby%{rubyxver}/%{rubyver}/*.rb
%{_libdir}/ruby%{rubyxver}/%{rubyver}/bigdecimal
%{_libdir}/ruby%{rubyxver}/%{rubyver}/cgi
%{_libdir}/ruby%{rubyxver}/%{rubyver}/date
%{_libdir}/ruby%{rubyxver}/%{rubyver}/digest
%{_libdir}/ruby%{rubyxver}/%{rubyver}/dl
%{_libdir}/ruby%{rubyxver}/%{rubyver}/drb
%{_libdir}/ruby%{rubyxver}/%{rubyver}/io
%{_libdir}/ruby%{rubyxver}/%{rubyver}/net
%{_libdir}/ruby%{rubyxver}/%{rubyver}/openssl
%{_libdir}/ruby%{rubyxver}/%{rubyver}/optparse
%{_libdir}/ruby%{rubyxver}/%{rubyver}/racc
%{_libdir}/ruby%{rubyxver}/%{rubyver}/rexml
%{_libdir}/ruby%{rubyxver}/%{rubyver}/rinda
%{_libdir}/ruby%{rubyxver}/%{rubyver}/rss
%{_libdir}/ruby%{rubyxver}/%{rubyver}/shell
%{_libdir}/ruby%{rubyxver}/%{rubyver}/test
%{_libdir}/ruby%{rubyxver}/%{rubyver}/uri
%{_libdir}/ruby%{rubyxver}/%{rubyver}/webrick
%{_libdir}/ruby%{rubyxver}/%{rubyver}/xmlrpc
%{_libdir}/ruby%{rubyxver}/%{rubyver}/yaml
%{_libdir}/libruby%{rubyxver}.so*
%{_libdir}/ruby%{rubyxver}/%{rubyver}/*/*.so
%{_libdir}/ruby%{rubyxver}/%{rubyver}/*/digest
%{_libdir}/ruby%{rubyxver}/%{rubyver}/*/io
%{_libdir}/ruby%{rubyxver}/%{rubyver}/*/racc
%{_libdir}/ruby%{rubyxver}/%{rubyver}/*/rbconfig.rb


# FIXME: Completely not tested!
%ifnarch ppc64 s390x sparc64 x86_64
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/%{_normalized_cpu}-%{_target_os}
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/%{_normalized_cpu}-%{_target_os}/enc
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/%{_normalized_cpu}-%{_target_os}/enc/trans
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/%{_normalized_cpu}-%{_target_os}/json/ext
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/%{_normalized_cpu}-%{_target_os}/mathn
%endif

# FIXME: Completely not tested!
%ifarch ppc64 s390x sparc64 x86_64
#%dir %{_libdir}/ruby
#%dir %{_libdir}/ruby%{rubyxver}/%{rubyver}
#%dir %{_libdir}/ruby%{rubyxver}/%{rubyver}/%{_normalized_cpu}-%{_target_os}
%{sitedir}
%endif

%{sitedir2}
## the following files should goes into ruby-tcltk package.
%exclude %{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/*tk.rb
%exclude %{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/tcltk.rb
%exclude %{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/tk
%exclude %{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/tk*.rb
%exclude %{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/tkextlib
%exclude %{_libdir}/ruby%{rubyxver}/%{rubyver}/*/tcltklib.so
%exclude %{_libdir}/ruby%{rubyxver}/%{rubyver}/*/tkutil.so
## the following files should goes into ruby-rdoc package.
%exclude %{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/rdoc
## the following files should goes into ruby-irb package.
%exclude %{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/irb.rb
%exclude %{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/irb

## files in ruby-libs from here

%files tcltk
%defattr(-, root, root, -)
%doc COPYING*
%doc ChangeLog
%doc GPL
%doc LEGAL
%doc LGPL
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/*-tk.rb
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/tcltk.rb
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/tk
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/tk*.rb
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/tkextlib
%{_libdir}/ruby%{rubyxver}/%{rubyver}/*/tcltklib.so
%{_libdir}/ruby%{rubyxver}/%{rubyver}/*/tkutil.so

%files rdoc
%defattr(-, root, root, -)
%doc COPYING*
%doc ChangeLog
%doc GPL
%doc LEGAL
%doc LGPL
%{_bindir}/rdoc1.9
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/rdoc

%files irb
%defattr(-, root, root, -)
%doc COPYING*
%doc ChangeLog
%doc GPL
%doc LEGAL
%doc LGPL
%{_bindir}/irb1.9
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/irb.rb
%{_prefix}/lib/ruby%{rubyxver}/%{rubyver}/irb
%{_mandir}/man1/irb1*

%files ri
%defattr(-, root, root, -)
%doc COPYING*
%doc ChangeLog
%doc GPL
%doc LEGAL
%doc LGPL
%{_bindir}/ri1.9
%{_datadir}/ri1.9

%files docs
%defattr(-, root, root, -)
%doc COPYING*
%doc ChangeLog
%doc GPL
%doc LEGAL
%doc LGPL


%changelog
* Tue Jun 09 2009 Aaron Turner <aturner@mudynamics.com> 3
  - Change versioning to standard incrementing value rather then date 
  - Change package name to ruby1.9 to prevent conflicts with ruby 1.8 package

* Tue Jun 05 2009 Aaron Turner <aturner@mudynamics.com> 20090605
  - initial release

* Tue May 12 2009 OpenPKG Foundation 20090512
  - Original OpenPKG 
