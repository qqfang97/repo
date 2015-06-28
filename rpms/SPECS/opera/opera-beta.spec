%global debug_package %{nil}

Name: opera-beta
Version: 30.0.1835.26
Release: 1%{?dist}
Summary: Fast and secure web browser
Summary(ru): Быстрый и безопасный Веб-браузер
Summary(zh_CN): 快速安全的欧朋浏览器

Group: Applications/Internet
License: Proprietary
URL: http://www.opera.com/browser
Source0: http://ftp.opera.com/pub/%{name}/%{version}/linux/%{name}_%{version}_amd64.deb

ExclusiveArch: x86_64
BuildRequires: desktop-file-utils
BuildRequires: dpkg

%description
 Opera is a fast, secure, and user-friendly web browser.
 It includes web developer tools, news aggregation, and the ability
 to compress data via Opera Turbo on congested networks.

%description -l ru
 Opera — это быстрый, безопасный и дружественный к пользователю
 веб-браузер. Он включает средства веб-разработки и сбора новостей,
 а также возможность сжимать трафик в перегруженных сетях
 посредством технологии Opera Turbo.

%description -l zh_CN
 Opera 是一款快速, 安全, 友好的 web 浏览器.
 它包含 web 开发工具, 新闻聚合, 通过 Opera Turbo 技术
 在低速网络中传输经过压缩的数据.

%prep
%build

%install
# Extract DEB package
dpkg-deb -X %{SOURCE0} %{buildroot}

# Move /usr/lib/x86_64-linux-gnu/#{name} to #{_libdir}
mv %{buildroot}/usr/lib/*-linux-gnu/%{name} %{buildroot}/usr/lib/
rm -rf %{buildroot}/usr/lib/*-linux-gnu
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}

# Modify desktop file:
sed -i '/Unity/s|^|#|' %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install *.desktop file:
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category Network \
  --add-category WebBrowser \
  --delete-original \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# Fix symlink
rm -f %{buildroot}%{_bindir}/*
ln -sfv %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}

# Clean files
rm -rf %{buildroot}%{_datadir}/menu
rm -rf %{buildroot}%{_datadir}/lintian

%post
chown root:root "%{_libdir}/%{name}/opera_sandbox"
chmod 4755 "%{_libdir}/%{name}/opera_sandbox"

update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/%{name}/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*
%{_defaultdocdir}/%{name}

%changelog
* Tue May 26 2015 mosquito <sensor.wen@gmail.com> -30.0.1835.26-1
- Update version 30.0.1835.26
* Tue Dec 23 2014 mosquito <sensor.wen@gmail.com> -27.0.1689.33-1
- Initial built