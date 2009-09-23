%define	rubyxver	1.8
%define	rubyver		1.8.7
%define _patchlevel	174
%define dotpatchlevel	%{?_patchlevel:.%{_patchlevel}}
%define patchlevel	%{?_patchlevel:-p%{_patchlevel}}
%define	arcver		%{rubyver}%{?patchlevel}
%define	sitedir		%{_libdir}/ruby/site_ruby
# This is required to ensure that noarch files puts under /usr/lib/... for
# multilib because ruby library is installed under /usr/{lib,lib64}/ruby anyway.
%define	sitedir2	%{_prefix}/lib/ruby/site_ruby
%define	_normalized_cpu	%(echo `echo %{_target_cpu} | sed 's/^ppc/powerpc/' | sed -e 's|i.86|i386|'`)

# emacs sitelisp directory
%{!?_emacs_sitelispdir: %global _emacs_sitelispdir %{_datadir}/emacs/site-lisp}
%{!?_emacs_sitestartdir: %global _emacs_sitestartdir %{_datadir}/emacs/site-lisp/site-start.d}

Name:		ruby
Version:	%{rubyver}%{?dotpatchlevel}
Release:	1%{?dist}
License:	Ruby or GPLv2
URL:		http://www.ruby-lang.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	readline readline-devel ncurses ncurses-devel gdbm gdbm-devel glibc-devel tcl-devel tk-devel libX11-devel autoconf gcc unzip openssl-devel db4-devel byacc
BuildRequires:	emacs

Source0:	ftp://ftp.ruby-lang.org/pub/%{name}/%{rubyxver}/%{name}-%{arcver}.tar.bz2
## Dead link
##Source1:	http://www7.tok2.com/home/misc/files/%{name}/%{name}-refm-rdp-1.8.1-ja-html.tar.gz
#Source1:	%{name}-refm-rdp-1.8.1-ja-html.tar.gz
# Needed in 1.8.6-p287, no longer needed in 1.8.6-p368?
#Patch25:	ruby-1.8.6.111-gcc43.patch

Summary:	An interpreter of object-oriented scripting language
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.


%package libs
Summary:	Libraries necessary to run Ruby
Group:		Development/Libraries
# ext/bigdecimal/bigdecimal.{c,h} are under (GPL+ or Artistic) which
# are used for bigdecimal.so
License:	(Ruby or GPLv2) and (GPL+ or Artistic)
Provides:	ruby(abi) = %{rubyxver}
Provides:	libruby = %{version}-%{release}
Obsoletes:	libruby <= %{version}-%{release}

%description libs
This package includes the libruby, necessary to run Ruby.


%package devel
Summary:	A Ruby development environment
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Provides:	%{name}-libs-static = %{version}-%{release}

%description devel
Header files and libraries for building a extension library for the
Ruby or an application embedded Ruby.


%package tcltk
Summary:	Tcl/Tk interface for scripting language Ruby
Group:		Development/Languages
# Many files under ext/tk/sample/ are under TCL
License:	(Ruby or GPLv2) and TCL
Requires:	%{name}-libs = %{version}-%{release}

%description tcltk
Tcl/Tk interface for the object-oriented scripting language Ruby.


%package irb
Summary:	The Interactive Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Provides:	irb = %{version}-%{release}
Obsoletes:	irb <= %{version}-%{release}

%description irb
The irb is acronym for Interactive Ruby.  It evaluates ruby expression
from the terminal.


%package rdoc
Summary:	A tool to generate documentation from Ruby source files
Group:		Development/Languages
# generators/template/html/html.rb is under CC-BY
License:	(GPLv2 or Ruby) and CC-BY
## ruby-irb requires ruby
#Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-irb = %{version}-%{release}
Provides:	rdoc = %{version}-%{release}
Obsoletes:	rdoc <= %{version}-%{release}

%description rdoc
The rdoc is a tool to generate the documentation from Ruby source files.
It supports some output formats, like HTML, Ruby interactive reference (ri),
XML and Windows Help file (chm).


%package docs
Summary:	Manuals and FAQs for scripting language Ruby
Group:		Documentation

%description docs
Manuals and FAQs for the object-oriented scripting language Ruby.


%package mode
Summary:	Emacs Lisp for the scripting language Ruby
Group:		Applications/Editors
Requires:	emacs-common

%description mode
Emacs Lisp ruby-mode for the object-oriented scripting language Ruby.


%package ri
Summary:	Ruby interactive reference
Group:		Documentation
## ruby-irb requires ruby, which ruby-rdoc requires
#Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-rdoc = %{version}-%{release}
Provides:	ri = %{version}-%{release}
Obsoletes:	ri <= %{version}-%{release}

%description ri
ri is a command line tool that displays descriptions of built-in
Ruby methods, classes and modules. For methods, it shows you the calling
sequence and a description. For classes and modules, it shows a synopsis
along with a list of the methods the class or module implements.


%prep
%setup -q -c 
pushd %{name}-%{arcver}
popd

%build
pushd %{name}-%{arcver}
for i in config.sub config.guess; do
	test -f %{_datadir}/libtool/$i && cp %{_datadir}/libtool/$i .
done
autoconf

rb_cv_func_strtod=no
export rb_cv_func_strtod
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CFLAGS
%configure \
  --with-sitedir='%{sitedir}' \
  --with-default-kcode=utf8 \
  --with-bundled-sha1 \
  --with-bundled-md5 \
  --with-bundled-rmd160 \
  --enable-shared \
  --enable-ipv6 \
  --enable-pthread \
  --with-lookup-order-hack=INET \
  --disable-rpath \
  --with-ruby-prefix=%{_prefix}/lib

make RUBY_INSTALL_NAME=ruby %{?_smp_mflags} COPY="cp -p" %{?_smp_mflags}
%ifarch ia64
# Miscompilation? Buggy code?
rm -f parse.o
make OPT=-O0 RUBY_INSTALL_NAME=ruby %{?_smp_mflags}
%endif

popd

%check
pushd %{name}-%{arcver}
%ifarch ppc64
make test || :
%else
make test
%endif
popd

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_emacs_sitelispdir}/ruby-mode
mkdir -p $RPM_BUILD_ROOT%{_emacs_sitestartdir}

# installing documents and exapmles...
rm -rf tmp-ruby-docs
mkdir tmp-ruby-docs
cd tmp-ruby-docs

# for ruby.rpm
mkdir ruby ruby-libs ruby-devel ruby-tcltk ruby-docs irb
cd ruby
(cd ../../%{name}-%{arcver} && tar cf - sample) | tar xvf -
cd ..

# for ruby-libs
cd ruby-libs
(cd ../../%{name}-%{arcver} && tar cf - lib/README*) | tar xf -
(cd ../../%{name}-%{arcver}/doc && tar cf - .) | tar xf -
(cd ../../%{name}-%{arcver} &&
 tar cf - `find ext \
  -mindepth 1 \
  \( -path '*/sample/*' -o -path '*/demo/*' \) -o \
  \( -name '*.rb' -not -path '*/lib/*' -not -name extconf.rb \) -o \
  \( -name 'README*' -o -name '*.txt*' -o -name 'MANUAL*' \)`) | tar xf -
cd ..

# for irb
cd irb
mv ../ruby-libs/irb/* .
rmdir ../ruby-libs/irb
cd ..

# for ruby-devel
cd ruby-devel

cd ..

# for ruby-tcltk
cd ruby-tcltk
for target in tcltklib tk
do
 (cd ../ruby-libs &&
  tar cf - `find . -path "*/$target/*"`) | tar xf -
 (cd ../ruby-libs &&
  rm -rf `find . -name "$target" -type d`)
done
cd ..

# for ruby-docs
cd ruby-docs
mkdir refm-ja faq-en faq-ja
(cd ../../ruby-refm-ja && tar cf - .) | (cd refm-ja && tar xf -)
(cd ../../rubyfaq && tar cf - .) | (cd faq-en && tar xf -)
(cd ../../rubyfaq-jp && tar cf - .) | (cd faq-ja && tar xf -)

(cd faq-ja &&
 for f in rubyfaq-jp*.html
 do
  sed -e 's/\(<a href="rubyfaq\)-jp\(\|-[0-9]*\)\(.html\)/\1\2\3/g' \
   < $f > `echo $f | sed -e's/-jp//'`
  rm -f $f; \
 done)
cd ..

# fixing `#!' paths
for f in `find . -type f`
do
  sed -e 's,^#![ 	]*\([^ 	]*\)/\(ruby\|wish\|perl\|env\),#!/usr/bin/\2,' < $f > $f.n
  if ! cmp $f $f.n
  then
    mv -f $f.n $f
  else
    rm -f $f.n
  fi
done

# make sure that all doc files are the world-readable
find -type f | xargs chmod 0644

# convert to utf-8
for i in `find -type f ! -name "*.gif"`; do
    status=0
    iconv -f utf-8 -t utf-8 $i >/dev/null || { iconv -f euc-jp -t utf-8 $i > $i.new && mv $i.new $i || status=1 ; }
    if [ $status = 0 ]; then
        if dirname $i | grep -q refm-ja ; then
          sed -i -e '/encoding/s|EUC-JP|UTF-8|' -e '/charset/s|EUC-JP|UTF-8|' $i
        fi
    else
        iconv -f iso8859-1 -t utf-8 $i > $.new && mv $i.new $i || rm -f $i.new
    fi
done

# done
cd ..

# installing binaries ...
make -C $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{arcver} DESTDIR=$RPM_BUILD_ROOT install

# generate ri doc
rubybuilddir=$RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{arcver}
rm -rf %{name}-%{arcver}/.ext/rdoc
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} RUBYLIB=$RPM_BUILD_ROOT%{_libdir}/ruby/%{rubyxver}:$RPM_BUILD_ROOT%{_libdir}/ruby/%{rubyxver}/%{_normalized_cpu}-%{_target_os} make -C $rubybuilddir DESTDIR=$RPM_BUILD_ROOT install-doc
#DESTDIR=$RPM_BUILD_ROOT LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_bindir}/ruby -I $rubybuilddir -I $RPM_BUILD_ROOT%{_libdir}/ruby/%{rubyxver}/%{_normalized_cpu}-%{_target_os}/ -I $rubybuilddir/lib $RPM_BUILD_ROOT%{_bindir}/rdoc --all --ri-system $rubybuilddir

mkdir -p $RPM_BUILD_ROOT%{sitedir2}/%{rubyxver}
mkdir -p $RPM_BUILD_ROOT%{sitedir}/%{rubyxver}/%{_normalized_cpu}-%{_target_os}


# installing ruby-mode
cd %{name}-%{arcver}
cp -p misc/*.el $RPM_BUILD_ROOT%{_emacs_sitelispdir}/ruby-mode

## for ruby-mode
pushd $RPM_BUILD_ROOT%{_emacs_sitelispdir}/ruby-mode
cat <<EOF > path.el
(setq load-path (cons "." load-path) byte-compile-warnings nil)
EOF
emacs --no-site-file -q -batch -l path.el -f batch-byte-compile *.el
rm -f path.el*
popd

cd ..

# remove shebang
for i in $RPM_BUILD_ROOT%{_prefix}/lib/ruby/1.8/{abbrev,generator,irb/{cmd/subirb,ext/save-history},matrix,rdoc/{markup/sample/rdoc2latex,parsers/parse_rb},set,tsort}.rb; do
	sed -i -e '/^#!.*/,1D' $i
done

find $RPM_BUILD_ROOT/ -name "*.so" -exec chmod 755 {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%doc %{name}-%{arcver}/LGPL
%doc %{name}-%{arcver}/NEWS
%doc %{name}-%{arcver}/README
%lang(ja) %doc %{name}-%{arcver}/README.ja
%doc %{name}-%{arcver}/ToDo
%doc %{name}-%{arcver}/doc/ChangeLog-1.8.0
%doc %{name}-%{arcver}/doc/NEWS-1.8.0
%doc tmp-ruby-docs/ruby/*
%{_bindir}/ruby
%{_bindir}/erb
%{_bindir}/testrb
%{_mandir}/man1/ruby.1*

%files devel
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%doc %{name}-%{arcver}/LGPL
%doc %{name}-%{arcver}/README.EXT
%lang(ja) %doc %{name}-%{arcver}/README.EXT.ja
%{_libdir}/libruby.so
%{_libdir}/libruby-static.a
%{_libdir}/ruby/%{rubyxver}/*/*.h

%files libs
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/README
%lang(ja) %doc %{name}-%{arcver}/README.ja
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%doc %{name}-%{arcver}/LGPL
%dir %{_prefix}/lib/ruby
%dir %{_prefix}/lib/ruby/%{rubyxver}
%ifnarch ppc64 s390x sparc64 x86_64
%if "%{_gnu}" == "-gnueabi"
%dir %{_prefix}/lib/ruby/%{rubyxver}/%{_normalized_cpu}-%{_target_os}-eabi
%else
%dir %{_prefix}/lib/ruby/%{rubyxver}/%{_normalized_cpu}-%{_target_os}
%endif
%endif
%ifarch ppc64 s390x sparc64 x86_64
%dir %{_libdir}/ruby
%dir %{_libdir}/ruby/%{rubyxver}
%dir %{_libdir}/ruby/%{rubyxver}/%{_normalized_cpu}-%{_target_os}
%{sitedir}
%endif
%{sitedir2}
## the following files should goes into ruby-tcltk package.
%exclude %{_prefix}/lib/ruby/%{rubyxver}/*tk.rb
%exclude %{_prefix}/lib/ruby/%{rubyxver}/tcltk.rb
%exclude %{_prefix}/lib/ruby/%{rubyxver}/tk
%exclude %{_prefix}/lib/ruby/%{rubyxver}/tk*.rb
%exclude %{_prefix}/lib/ruby/%{rubyxver}/tkextlib
%exclude %{_libdir}/ruby/%{rubyxver}/*/tcltklib.so
%exclude %{_libdir}/ruby/%{rubyxver}/*/tkutil.so
## the following files should goes into ruby-rdoc package.
%exclude %{_prefix}/lib/ruby/%{rubyxver}/rdoc
## the following files should goes into ruby-irb package.
%exclude %{_prefix}/lib/ruby/%{rubyxver}/irb.rb
%exclude %{_prefix}/lib/ruby/%{rubyxver}/irb
## files in ruby-libs from here
%{_prefix}/lib/ruby/%{rubyxver}/*.rb
%{_prefix}/lib/ruby/%{rubyxver}/bigdecimal
%{_prefix}/lib/ruby/%{rubyxver}/cgi
%{_prefix}/lib/ruby/%{rubyxver}/date
%{_prefix}/lib/ruby/%{rubyxver}/digest
%{_prefix}/lib/ruby/%{rubyxver}/dl
%{_prefix}/lib/ruby/%{rubyxver}/drb
%{_prefix}/lib/ruby/%{rubyxver}/io
%{_prefix}/lib/ruby/%{rubyxver}/net
%{_prefix}/lib/ruby/%{rubyxver}/openssl
%{_prefix}/lib/ruby/%{rubyxver}/optparse
%{_prefix}/lib/ruby/%{rubyxver}/racc
%{_prefix}/lib/ruby/%{rubyxver}/rexml
%{_prefix}/lib/ruby/%{rubyxver}/rinda
%{_prefix}/lib/ruby/%{rubyxver}/rss
%{_prefix}/lib/ruby/%{rubyxver}/runit
%{_prefix}/lib/ruby/%{rubyxver}/shell
%{_prefix}/lib/ruby/%{rubyxver}/soap
%{_prefix}/lib/ruby/%{rubyxver}/test
%{_prefix}/lib/ruby/%{rubyxver}/uri
%{_prefix}/lib/ruby/%{rubyxver}/webrick
%{_prefix}/lib/ruby/%{rubyxver}/wsdl
%{_prefix}/lib/ruby/%{rubyxver}/xmlrpc
%{_prefix}/lib/ruby/%{rubyxver}/xsd
%{_prefix}/lib/ruby/%{rubyxver}/yaml
%{_libdir}/libruby.so.*
%{_libdir}/ruby/%{rubyxver}/*/*.so
%{_libdir}/ruby/%{rubyxver}/*/digest
%{_libdir}/ruby/%{rubyxver}/*/io
%{_libdir}/ruby/%{rubyxver}/*/racc
%{_libdir}/ruby/%{rubyxver}/*/rbconfig.rb

%files tcltk
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%doc %{name}-%{arcver}/LGPL
%doc tmp-ruby-docs/ruby-tcltk/ext/*
%{_prefix}/lib/ruby/%{rubyxver}/*-tk.rb
%{_prefix}/lib/ruby/%{rubyxver}/tcltk.rb
%{_prefix}/lib/ruby/%{rubyxver}/tk
%{_prefix}/lib/ruby/%{rubyxver}/tk*.rb
%{_prefix}/lib/ruby/%{rubyxver}/tkextlib
%{_libdir}/ruby/%{rubyxver}/*/tcltklib.so
%{_libdir}/ruby/%{rubyxver}/*/tkutil.so

%files rdoc
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%doc %{name}-%{arcver}/LGPL
%{_bindir}/rdoc
%{_prefix}/lib/ruby/%{rubyxver}/rdoc

%files irb
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%doc %{name}-%{arcver}/LGPL
%doc tmp-ruby-docs/irb/*
%{_bindir}/irb
%{_prefix}/lib/ruby/%{rubyxver}/irb.rb
%{_prefix}/lib/ruby/%{rubyxver}/irb

%files ri
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%doc %{name}-%{arcver}/LGPL
%{_bindir}/ri
%{_datadir}/ri

%files docs
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%doc %{name}-%{arcver}/LGPL
%doc tmp-ruby-docs/ruby-docs/*
%doc tmp-ruby-docs/ruby-libs/*

%files mode
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%doc %{name}-%{arcver}/LGPL
%doc %{name}-%{arcver}/misc/README
%{_emacs_sitelispdir}/ruby-mode

%changelog
* Sat Jun 20 2009  Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.8.6.369-1
- New patchlevel fixing CVE-2009-1904
- Fix directory on ARM (#506233, Kedar Sovani)

* Sun May 31 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 1.8.6.368-1
- New upstream release (p368)

* Sat Apr 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.287-8
- Merge Review fix (#226381)

* Wed Mar 18 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 1.8.6.287-7
- Fix regression in CVE-2008-3790 (#485383)

* Mon Mar 16 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.287-6
- Again use -O2 optimization level
- i586 should search i386-linux directory (on <= F-11)

* Thu Mar 05 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.8.6.287-5
- Rebuild for gcc4.4

* Fri Feb 27 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.8.6.287-3
- CVE-2008-5189: CGI header injection.

* Wed Oct  8 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.287-2
- CVE-2008-3790: DoS vulnerability in the REXML module.

* Sat Aug 23 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.287-1
- New upstream release.
- Security fixes.
  - CVE-2008-3655: Ruby does not properly restrict access to critical
                   variables and methods at various safe levels.
  - CVE-2008-3656: DoS vulnerability in WEBrick.
  - CVE-2008-3657: Lack of taintness check in dl.
  - CVE-2008-1447: DNS spoofing vulnerability in resolv.rb.
  - CVE-2008-3443: Memory allocation failure in Ruby regex engine.
- Remove the unnecessary backported patches.

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.8.6.230-5
- rebuild against db4-4.7

* Tue Jul  1 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.230-4
- Backported from upstream SVN to fix a segfault issue with Array#fill.

* Mon Jun 30 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.230-3
- Backported from upstream SVN to fix a segfault issue. (#452825)
- Backported from upstream SVN to fix an integer overflow in rb_ary_fill.

* Wed Jun 25 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.230-2
- Fix a segfault issue. (#452810)

* Tue Jun 24 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.230-1
- New upstream release.
- Security fixes. (#452295)
  - CVE-2008-1891: WEBrick CGI source disclosure.
  - CVE-2008-2662: Integer overflow in rb_str_buf_append().
  - CVE-2008-2663: Integer overflow in rb_ary_store().
  - CVE-2008-2664: Unsafe use of alloca in rb_str_format().
  - CVE-2008-2725: Integer overflow in rb_ary_splice().
  - CVE-2008-2726: Integer overflow in rb_ary_splice().
- ruby-1.8.6.111-CVE-2007-5162.patch: removed.
- Build ruby-mode package for all archtectures.

* Tue Mar  4 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.114-1
- Security fix for CVE-2008-1145.
- Improve a spec file. (#226381)
  - Correct License tag.
  - Fix a timestamp issue.
  - Own a arch-specific directory.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.8.6.111-9
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-8
- Rebuild for gcc-4.3.

* Tue Jan 15 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-7
- Revert the change of libruby-static.a. (#428384)

* Fri Jan 11 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-6
- Fix an unnecessary replacement for shebang. (#426835)

* Fri Jan  4 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-5
- Rebuild.

* Fri Dec 28 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-4
- Clean up again.

* Fri Dec 21 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-3
- Clean up the spec file.
- Remove ruby-man-1.4.6 stuff. this is entirely the out-dated document.
  this could be replaced by ri.
- Disable the static library building.

* Tue Dec 04 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.8.6.111-2
 - Rebuild for openssl bump

* Wed Oct 31 2007 Akira TAGOH <tagoh@redhat.com>
- Fix the dead link.

* Mon Oct 29 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-1
- New upstream release.
- ruby-1.8.6.111-CVE-2007-5162.patch: Update a bit with backporting the changes
   at trunk to enable the fix without any modifications on the users' scripts.
   Note that Net::HTTP#enable_post_connection_check isn't available anymore.
   If you want to disable this post-check, you should give OpenSSL::SSL::VERIFY_NONE
   to Net::HTTP#verify_mode= instead of.

* Mon Oct 15 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.110-2
- Enable pthread support for ppc too. (#201452)
- Fix unexpected dependencies appears in ruby-libs. (#253325)

* Wed Oct 10 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.110-1
- New upstream release.
  - ruby-r12567.patch: removed.
- ruby-1.8.6-CVE-2007-5162.patch: security fix for Net::HTTP that is
  insufficient verification of SSL certificate.

* Thu Aug 23 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.36-4
- Rebuild

* Fri Aug 10 2007 Akira TAGOH <tagoh@redhat.com>
- Update License tag.

* Mon Jul 25 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.36-3
- ruby-r12567.patch: backport patch from upstream svn to get rid of
  the unnecessary declarations. (#245446)

* Wed Jul 20 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.36-2
- New upstream release.
  - Fix Etc::getgrgid to get the correct gid as requested. (#236647)

* Wed Mar 28 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6-2
- Fix search path breakage. (#234029)

* Thu Mar 15 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6-1
- New upstream release.
- clean up a spec file.

* Tue Feb 13 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.5.12-2
- Rebuild

* Mon Feb  5 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.5.12-1
- New upstream release.

* Mon Dec 11 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.5.2-1
- security fix release.

* Fri Oct 27 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.5-4
- security fix release.
- ruby-1.8.5-cgi-CVE-2006-5467.patch: fix a CGI multipart parsing bug that
  causes the denial of service. (#212396)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.8.5-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.5-2
- fixed rbconfig.rb to refer to DESTDIR for sitearchdir. (#207311)

* Mon Aug 28 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.5-1
- New upstream release.
- removed the unnecessary patches:
  - ruby-1.8.4-no-eaccess.patch
  - ruby-1.8.4-64bit-pack.patch
  - ruby-1.8.4-fix-insecure-dir-operation.patch
  - ruby-1.8.4-fix-insecure-regexp-modification.patch
  - ruby-1.8.4-fix-alias-safe-level.patch
- build with --enable-pthread except on ppc.
- ruby-1.8.5-hash-memory-leak.patch: backported from CVS to fix a memory leak
  on Hash. [ruby-talk:211233]

* Mon Aug  7 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-12
- owns sitearchdir. (#201208)

* Thu Jul 20 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-11
- security fixes [CVE-2006-3694]
  - ruby-1.8.4-fix-insecure-dir-operation.patch:
  - ruby-1.8.4-fix-insecure-regexp-modification.patch: fixed the insecure
    operations in the certain safe-level restrictions. (#199538)
  - ruby-1.8.4-fix-alias-safe-level.patch: fixed to not bypass the certain
    safe-level restrictions. (#199543)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.8.4-10.fc6.1
- rebuild

* Mon Jun 19 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-10
- fixed the wrong file list again. moved tcltk library into ruby-tcltk.
  (#195872)

* Thu Jun  8 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-8
- ruby-deprecated-sitelib-search-path.patch: correct the order of search path.

* Wed Jun  7 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-7
- exclude ppc64 to make ruby-mode package. right now emacs.ppc64 isn't provided
  and buildsys became much stricter.
- ruby-deprecated-sitelib-search-path.patch: applied to add more search path
  for backward compatiblity.
- added byacc to BuildReq. (#194161)

* Wed May 17 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-6
- ruby-deprecated-search-path.patch: added the deprecated installation paths
  to the search path for the backward compatibility.
- added a Provides: ruby(abi) to ruby-libs.
- ruby-1.8.4-64bit-pack.patch: backport patch from upstream to fix unpack("l")
  not working on 64bit arch and integer overflow on template "w". (#189350)
- updated License tag to be more comfortable, and with a pointer to get more
  details, like Python package does. (#179933)
- clean up.

* Wed Apr 19 2006 Akira TAGOH <tagoh@redhat.com>
- ruby-rubyprefix.patch: moved all arch-independent modules under /usr/lib/ruby
  and keep arch-dependent modules under /usr/lib64/ruby for 64bit archs.
  so 'rubylibdir', 'sitelibdir' and 'sitedir' in Config::CONFIG points to
  the kind of /usr/lib/ruby now. (#184199)

* Mon Apr 17 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-4
- correct sitelibdir. (#184198)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.8.4-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.8.4-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb  6 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-3
- ruby-1.8.4-no-eaccess.patch: backported from ruby CVS to avoid conflict
  between newer glibc. (#179835)

* Wed Jan  4 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-2
- ruby-tcltk-multilib.patch: fixed a typo.

* Tue Dec 27 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.4-1
- New upstream release.
  - fixed a missing return statement. (#140833)
  - fixed an use of uninitialized variable. (#144890)

* Fri Dec 16 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.4-0.4.preview2
- updates to 1.8.4-preview2.
- renamed the packages to ruby-* (#175765)
  - irb  -> ruby-irb
  - rdoc -> ruby-rdoc
  - ri   -> ruby-ri
- added tcl-devel and tk-devel into BuildRequires.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.4-0.3.preview1
- rebuilt against the latest openssl.

* Tue Nov  1 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.4-0.2.preview1
- build-deps libX11-devel instead of xorg-x11-devel.

* Mon Oct 31 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.4-0.1.preview1
- New upstream release.
- ruby-1.8.2-strscan-memset.patch: removed because it's no longer needed.

* Tue Oct  4 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.3-4
- moved the documents from ruby-libs to ruby-docs, which contains the arch
  specific thing and to be multilib support. (#168826)

* Mon Oct  3 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.3-3
- fixed the wrong file list. the external library for tcl/tk was included
  in ruby-libs unexpectedly.

* Mon Sep 26 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.3-2
- ruby-multilib.patch: added another chunk for multilib. (#169127)

* Wed Sep 21 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.3-1
- New upstream release.
- Build-Requires xorg-x11-devel instead of XFree86-devel.
- ruby-multilib.patch: applied for only 64-bit archs.
- ruby-1.8.2-xmlrpc-CAN-2005-1992.patch: removed. it has already been in upstream.

* Tue Jun 21 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-9
- ruby-1.8.2-xmlrpc-CAN-2005-1992.patch: fixed the arbitrary command execution
  on XMLRPC server. (#161096)

* Thu Jun 16 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-8
- ruby-1.8.2-tcltk-multilib.patch: applied to get tcltklib.so built. (#160194)

* Thu Apr  7 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-7
- ruby-1.8.2-deadcode.patch: removed the dead code from the source. (#146108)
- make sure that all documentation files in ruby-docs are the world-
  readable. (#147279)

* Tue Mar 22 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-6
- ruby-1.8.2-strscan-memset.patch: fixed an wrong usage of memset(3).

* Tue Mar 15 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-5
- rebuilt

* Tue Jan 25 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-4
- fixed the wrong generation of file manifest. (#146055)
- spec file clean up.

* Mon Jan 24 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-3
- separated out to rdoc package.
- make the dependency of irb for rdoc. (#144708)

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> - 1.8.2-2
- Rebuilt for new readline.

* Wed Jan  5 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-1
- New upstream release.
- ruby-1.8.1-ia64-stack-limit.patch: removed - it's no longer needed.
- ruby-1.8.1-cgi_session_perms.patch: likewise.
- ruby-1.8.1-cgi-dos.patch: likewise.
- generated Ruby interactive documentation - senarated package.
  it's now provided as ri package. (#141806)

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 1.8.1-10
- rebuild against db-4.3.21.

* Wed Nov 10 2004 Akira TAGOH <tagoh@redhat.com> - 1.8.1-9
- ruby-1.8.1-cgi-dos.patch: security fix [CAN-2004-0983]
- ruby-1.8.1-cgi_session_perms.patch: security fix [CAN-2004-0755]

* Fri Oct 29 2004 Akira TAGOH <tagoh@redhat.com> - 1.8.1-8
- added openssl-devel and db4-devel into BuildRequires (#137479)

* Wed Oct  6 2004 Akira TAGOH <tagoh@redhat.com> - 1.8.1-7
- require emacs-common instead of emacs.

* Wed Jun 23 2004 Akira TAGOH <tagoh@redhat.com> 1.8.1-4
- updated the documentation.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 04 2004 Akira TAGOH <tagoh@redhat.com> 1.8.1-1
- New upstream release.
- don't use any optimization for ia64 to avoid the build failure.
- ruby-1.8.1-ia64-stack-limit.patch: applied to fix SystemStackError when the optimization is disabled.

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 1.8.0-3
- rebuild against db-4.2.52.

* Thu Sep 25 2003 Jeff Johnson <jbj@jbj.org> 1.8.0-2
- rebuild against db-4.2.42.

* Tue Aug  5 2003 Akira TAGOH <tagoh@redhat.com> 1.8.0-1
- New upstream release.

* Thu Jul 24 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-9.1
- rebuilt

* Thu Jul 24 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-9
- ruby-1.6.8-castnode.patch: handling the nodes with correct cast.
  use this patch now instead of ruby-1.6.8-fix-x86_64.patch.

* Fri Jul 04 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-8
- rebuilt

* Fri Jul 04 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-7
- fix the gcc warnings. (#82192)
- ruby-1.6.8-fix-x86_64.patch: correct a patch.
  NOTE: DON'T USE THIS PATCH FOR BIG ENDIAN ARCHITECTURE.
- ruby-1.6.7-long2int.patch: removed.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb  7 2003 Jens Petersen <petersen@redhat.com> - 1.6.8-5
- rebuild against ucs4 tcltk

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-3
- ruby-1.6.8-multilib.patch: applied to fix the search path issue on x86_64

* Tue Jan 21 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-2
- ruby-1.6.8-require.patch: applied to fix the search bug in require.
- don't apply long2int patch to s390 and s390x. it doesn't work.

* Wed Jan 15 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-1
- New upstream release.
- removed some patches. it's no longer needed.
  - ruby-1.6.7-100.patch
  - ruby-1.6.7-101.patch
  - ruby-1.6.7-102.patch
  - ruby-1.6.7-103.patch
  - 801_extmk.rb-shellwords.patch
  - 801_mkmf.rb-shellwords.patch
  - 804_parse.y-new-bison.patch
  - 805_uri-bugfix.patch
  - ruby-1.6.6-900_XXX_strtod.patch
  - ruby-1.6.7-sux0rs.patch
  - ruby-1.6.7-libobj.patch

* Wed Jan 15 2003 Jens Petersen <petersen@redhat.com> 1.6.7-14
- rebuild to update tcltk deps

* Mon Dec 16 2002 Elliot Lee <sopwith@redhat.com> 1.6.7-13
- Remove ExcludeArch: x86_64
- Fix x86_64 ruby with long2int.patch (ruby was assuming that sizeof(long)
  == sizeof(int). The patch does not fix the source of the problem, just
  makes it a non-issue.)
- _smp_mflags

* Tue Dec 10 2002 Tim Powers <timp@redhat.com> 1.6.7-12
- rebuild to fix broken tcltk deps

* Tue Oct 22 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-11
- use %%configure macro instead of configure script.
- use the latest config.{sub,guess}.
- get archname from rbconfig.rb for %%dir
- applied some patches from Debian:
  - 801_extmk.rb-shellwords.patch: use Shellwords
  - 801_mkmf.rb-shellwords.patch: mkmf.rb creates bad Makefile. the Makefile
    links libruby.a to the target.
  - 803_sample-fix-shbang.patch: all sample codes should be
    s|/usr/local/bin|/usr/bin|g
  - 804_parse.y-new-bison.patch: fix syntax warning.
  - 805_uri-bugfix.patch: uri.rb could not handle correctly broken mailto-uri.
- add ExcludeArch x86_64 temporarily to fix Bug#74581. Right now ruby can't be
  built on x86_64.

* Tue Aug 27 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-10
- moved sitedir to /usr/lib/ruby/site_ruby again according as our perl and
  python.
- ruby-1.6.7-resolv1.patch, ruby-1.6.7-resolv2.patch: applied to fix 'Too many
  open files - "/etc/resolv.conf"' issue. (Bug#64830)

* Thu Jul 18 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-9
- add the owned directory.

* Fri Jul 12 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-8
- fix typo.

* Thu Jul 04 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-7
- removed the ruby-mode-xemacs because it's merged to the xemacs sumo.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-5
- fix the stripped binary.
- use the appropriate macros.

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-3
- ruby-1.6.7-libobj.patch: applied to fix autoconf2.53 error.

* Mon Mar 18 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-2
- ruby-man-1.4.6-jp.tar.bz2: removed.
- ruby-refm-rdp-1.4.7-ja-html.tar.bz2: uses it instead of.
- ruby-1.6.7-500-marshal-proc.patch, ruby-1.6.7-501-class-var.patch:
  removed.
- ruby-1.6.7-100.patch: applied a bug fix patch.
  (ruby-dev#16274: patch for 'wm state')
  (PR#206ja: SEGV handle EXIT)
- ruby-1.6.7-101.patch: applied a bug fix patch.
  (ruby-list#34313: singleton should not be Marshal.dump'ed)
  (ruby-dev#16411: block local var)
- ruby-1.6.7-102.patch: applied a bug fix patch.
  (handling multibyte chars is partially broken)
- ruby-1.6.7-103.patch: applied a bug fix patch.
  (ruby-dev#16462: preserve reference for GC, but link should be cut)

* Fri Mar  8 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-1
- New upstream release.
- ruby-1.6.6-100.patch, ruby-1.6.6-501-ruby-mode.patch:
  removed. these patches no longer should be needed.
- ruby-1.6.7-500-marshal-proc.patch: applied a fix patch.
  (ruby-dev#16178: Marshal::dump should call Proc#call.)
- ruby-1.6.7-501-class-var.patch: applied a fix patch.
  (ruby-talk#35157: class vars broken in 1.6.7)

* Wed Feb 27 2002 Akira TAGOH <tagoh@redhat.com> 1.6.6-5
- Disable alpha because nothing is xemacs for alpha now.

* Tue Feb  5 2002 Akira TAGOH <tagoh@redhat.com> 1.6.6-3
- Fixed the duplicate files.

* Tue Feb  5 2002 Akira TAGOH <tagoh@redhat.com> 1.6.6-2
- Fixed the missing %%defattr

* Fri Feb  1 2002 Akira TAGOH <tagoh@redhat.com> 1.6.6-1
- New upstream release.
- Applied bug fix patches:
  - ruby-1.6.6-501-ruby-mode.patch: ruby-talk#30479: disables font-lock
    coloring.
  - ruby-1.6.6-100.patch: ruby-talk#30203: Ruby 1.6.6 bug and fix
                          ruby-list#33047: regex bug
                          PR#230: problem with -d in 1.6.6
- Added ruby-mode and ruby-mode-xemacs packages.
- Ruby works fine for ia64. so re-enable to build with ia64.
  (probably it should be worked for alpha)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jul 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.6.4-2
- Remove Japanese description and summaries; they belong in specspo and
  break rpm
- Clean up specfile
- Mark language specific files (README.jp) as such
- bzip2 sources
- rename the libruby package to ruby-libs for consistency
- Exclude ia64 (doesn't build - the code doesn't seem to be 64-bit clean
  [has been excluded on alpha forever])

* Tue Jul 17 2001 Akira TAGOH <tagoh@redhat.com> 1.6.4-1
- rebuild for Red Hat 7.2

* Mon Jun 04 2001 akira yamada <akira@vinelinux.org>
- upgrade to nwe upstream version 1.6.4.

* Mon Apr 02 2001 akira yamada <akira@vinelinux.org>
- applied patch:
  - fixed method cache bug. etc. (Patch103, Patch104)

* Tue Mar 27 2001 akira yamada <akira@vinelinux.org>
- applied patch:
  - fixed marshal for bignum bug.
  - fixed scope of constant variables bug.

* Tue Mar 20 2001 akira yamada <akira@vinelinux.org>
- upgraded to new upstream version 1.6.3.

* Fri Feb 09 2001 akira yamada <akira@vinelinux.org>
- fixed bad group for libruby.
- Applied patch: upgraded to cvs version (2001-02-08):
  fixed minor bugs.

* Thu Jan 18 2001 akira yamada <akira@vinelinux.org>
- Applied patch: upgraded to cvs version (2001-01-15):
  fixed minor bugs(e.g. ruby makes extention librares too large...).

* Wed Jan 10 2001 akira yamada <akira@vinelinux.org>
- Applied patch: upgraded to cvs version (2001-01-09):
  fixed minor bugs.

* Sat Dec 30 2000 akira yamada <akira@vinelinux.org>
- Applied bug fix patch.

* Mon Dec 25 2000 akira yamada <akira@vinelinux.org>
- Updated to new upstream version 1.6.2.

* Fri Dec 22 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000122019.patch, added ruby_cvs.2000122215.patch
  (upgraded ruby to latest cvs version, 1.6.2-preview4).

* Wed Dec 20 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000121413.patch, added ruby_cvs.2000122019.patch
  (upgraded ruby to latest cvs version).
- new package: libruby

* Thu Dec 14 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000101901.patch, added ruby_cvs.2000121413.patch
  (upgraded ruby to latest cvs version).
- Removed ruby-dev.11262.patch, ruby-dev.11265.patch,
  and ruby-dev.11268.patch (included into above patch).

* Sun Nov 12 2000 MACHINO, Satoshi <machino@vinelinux.org> 1.6.1-0vl9
- build on gcc-2.95.3

* Thu Oct 19 2000 akira yamada <akira@vinelinux.org>
- Added ruby-dev.11268.patch.

* Thu Oct 19 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000101117.patch and added ruby_cvs.2000101901.patch
  (upgraded ruby to latest cvs version).
- Added ruby-dev.11262.patch.
- Added ruby-dev.11265.patch.

* Wed Oct 11 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000100313.patch and added ruby_cvs.2000101117.patch
  (upgraded ruby to latest cvs version).

* Mon Oct 09 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000100313.patch and added ruby_cvs.2000100313.patch
  (upgraded ruby to latest cvs version).

* Tue Oct 03 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000100218.patch and added ruby_cvs.2000100313.patch
  (upgraded ruby to latest cvs version).

* Mon Oct 02 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000092718.patch and added ruby_cvs.2000100218.patch
  (upgraded ruby to latest cvs version).

* Thu Sep 27 2000 akira yamada <akira@vinelinux.org>
- Updated to upstream version 1.6.1.
- Removed ruby_cvs.2000082901.patch and added ruby_cvs.2000092718.patch
  (upgraded ruby to latest cvs version).

* Tue Aug 29 2000 akira yamada <akira@redhat.com>
- Updated to version 1.4.6.
- removed ruby-dev.10123.patch(included into ruby-1.4.6).
- Added ruby_cvs.2000082901.patch(upgraded ruby to latest cvs version).

* Tue Jun 27 2000 akira yamada <akira@redhat.com>
- Updated manuals to version 1.4.5.

* Sun Jun 25 2000 akira yamada <akira@redhat.com>
- Added ruby-dev.10123.patch.

* Sat Jun 24 2000 akira yamada <akira@redhat.com>
- Updated to version 1.4.5.
- Removed ruby_cvs.2000062401.patch(included into ruby-1.4.5).

* Thu Jun 22 2000 akira yamada <akira@redhat.com>
- Updated to version 1.4.4(06/22/2000 CVS).
- Removed ruby-dev.10054.patch(included into ruby_cvs.patch).

* Thu Jun 22 2000 akira yamada <akira@redhat.com>
- Renamed to ruby_cvs20000620.patch from ruby_cvs.patch.

* Tue Jun 20 2000 akira yamada <akira@redhat.com>
- Updated to version 1.4.4(06/20/2000 CVS).
- Removed ruby-list.23190.patch(included into ruby_cvs.patch).
- Added ruby-dev.10054.patch.

* Tue Jun 15 2000 akira yamada <akira@redhat.com>
- Updated to version 1.4.4(06/12/2000 CVS).
- Added manuals and FAQs.
- Split into ruby, ruby-devel, ruby-tcltk, ruby-docs, irb.

* Tue Jun 13 2000 Mitsuo Hamada <mhamada@redhat.com>
- Updated to version 1.4.4

* Wed Dec 08 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.4.3

* Mon Sep 20 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.4.2 (Sep 18)

* Fri Sep 17 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.4.2

* Tue Aug 17 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.4.0

* Fri Jul 23 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- 2nd release
- Updated to version 1.2.6(15 Jul 1999)
- striped %%{prefix}/bin/ruby

* Mon Jun 28 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.2.6(21 Jun 1999)

* Wed Apr 14 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.2.5

* Fri Apr 09 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.2.4

* Fri Dec 25 1998 Toru Hoshina <hoshina@best.com>
- Version up to 1.2 stable.

* Fri Nov 27 1998 Toru Hoshina <hoshina@best.com>
- Version up to 1.1c9.

* Thu Nov 19 1998 Toru Hoshina <hoshina@best.com>
- Version up to 1.1c8, however it appear short life :-P

* Fri Nov 13 1998 Toru Hoshina <hoshina@best.com>
- Version up.

* Mon Sep 22 1998 Toru Hoshina <hoshina@best.com>
- To make a libruby.so.

* Mon Sep 21 1998 Toru Hoshina <hoshina@best.com>
- Modified SPEC in order to install libruby.a so that it should be used by
  another ruby entention.
- 2nd release.

* Mon Mar 9 1998 Shoichi OZAWA <shoch@jsdi.or.jp>
- Added a powerPC arch part. Thanks, MURATA Nobuhiro <nob@makioka.y-min.or.jp>
