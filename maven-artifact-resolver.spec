Name:           maven-artifact-resolver
Version:        1.0
Release:        9%{?dist}
# Epoch is added because the original package's version in maven-shared is 1.1-SNAPSHOT
Epoch:          1
Summary:        Maven Artifact Resolution API
License:        ASL 2.0
URL:            http://maven.apache.org/shared/%{name}
Source0:        http://central.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildArch:      noarch

BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  maven-local
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  plexus-containers-component-metadata
BuildRequires:  maven-artifact-manager
BuildRequires:  maven-project
BuildRequires:  maven-shared


%description
Provides a component for plugins to easily resolve project dependencies.


%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q
# use plexus-component-metadata instead of old plugin
%pom_remove_plugin :plexus-maven-plugin
%pom_add_plugin org.codehaus.plexus:plexus-component-metadata pom.xml "
         <executions>
           <execution>
             <id>create-component-descriptor</id>
             <phase>generate-resources</phase>
             <goals>
              <goal>generate-metadata</goal>
             </goals>
           </execution>
         </executions>
"

%pom_add_dep org.apache.maven:maven-compat:1.0

# Incompatible method invocation
rm src/test/java/org/apache/maven/shared/artifact/resolver/DefaultProjectDependenciesResolverIT.java

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc DEPENDENCIES LICENSE NOTICE
%dir %{_javadir}/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Fri Aug 16 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:1.0-9
- Migrate away from mvn-rpmbuild (#997444)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-8
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Tue Feb 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:1.0-7
- Add maven-shared to BR/R
- Add few other missing BRs

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1:1.0-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Sep 14 2012 Tomas Radej <tradej@redhat.com> - 1:1.0-4
- Installing folders separately with -m 755
- Installing NOTICE in javadoc subpackage
- Fixed changelog

* Wed Sep 12 2012 Tomas Radej <tradej@redhat.com> - 1:1.0-3
- Really fixed Provides/Obsoletes by introducing epoch

* Thu Sep 06 2012 Tomas Radej <tradej@redhat.com> - 1.0-2
- Fixed Provides/Obsoletes

* Tue Jul 31 2012 Tomas Radej <tradej@redhat.com> - 1.0-1
- Initial version
