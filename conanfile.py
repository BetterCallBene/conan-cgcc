from conans import ConanFile, tools, __version__ as conan_version
from conans.model.version import Version

import tarfile
import os, sys

class CrossGccConan(ConanFile):
    name = "CrossGccConan"
    version = "5.4.0"
    url = "https://github.com/BetterCallBene/conan-cgcc"
    description = "Create a GCC cross-compiler"
    author="Benedikt König"
    license="gcc License"

    settings = {"os_build" : ["Linux"],
                "arch_build" : ["x86_64"],
                "arch" : ["armv8"],
                "compiler" : {"gcc" : { "version" : "5",
                                        "libcxx" : ["libstdc++"]}}}
    binutils_version = "2.26.1"
    gcc_version = "5.4.0"
    glibc_version = "2.23"
    linux_major = "4"
    linux_version = "4.4.119"
    mpfr_version = "4.0.1"
    gmp_version = "6.1.2"
    mpc_version = "1.1.0"

    target_host = "aarch64-unknown-linux-gnu"
    cc_compiler="gcc"
    cxx_compiler="g++"
    fortran_compiler="gfortran"

    exports_sources=["src/*"]

    def configure(self):
        if self.settings.os_build != "Linux":
            raise Exception("Only Linux supported for cross compiler")
    @property
    def arch(self):
        return self.settings.get_safe("arch_build") or self.settings.get_safe("arch")
    def source(self):
        print("wget binutils")
        tools.download("http://ftpmirror.gnu.org/binutils/binutils-%s.tar.gz" %
                   (self.binutils_version), "src/binutils.tar.gz")
        print("\nwget gcc")
        tools.download("http://ftpmirror.gnu.org/gcc/gcc-%s/gcc-%s.tar.gz" %
                       (self.gcc_version, self.gcc_version), "src/gcc.tar.gz")
        print("\nwget glibc")
        tools.download("http://ftpmirror.gnu.org/glibc/glibc-%s.tar.xz" %
                       (self.glibc_version), "src/glibc.tar.xz")
        print("\nwget linux")

        tools.download("https://www.kernel.org/pub/linux/kernel/v%s.x/linux-%s.tar.xz"
                       %(self.linux_major, self.linux_version), "src/linux.tar.xz", verify=False)
        print("\nwget mpfr")
        tools.download("http://ftpmirror.gnu.org/mpfr/mpfr-%s.tar.xz" %
                       (self.mpfr_version), "src/mpfr.tar.xz")
        print("\nwget gmp")
        tools.download("http://ftpmirror.gnu.org/gmp/gmp-%s.tar.xz" %
                       (self.gmp_version), "src/gmp.tar.xz" )
        print("\nwget mpc")
        tools.download("http://ftpmirror.gnu.org/mpc/mpc-%s.tar.gz" %
                       (self.mpc_version), "src/mpc.tar.gz")
        with(tools.chdir("./src")):

            print("unzip binutils")
            tools.unzip("binutils.tar.gz")

            print("unzip gcc")
            tools.unzip("gcc.tar.gz")

            print("unzip glibc")
            tar = tarfile.open("glibc.tar.xz", 'r:xz')
            tar.extractall()
            tar.close()


            print("unzip linux")
            tar = tarfile.open("linux.tar.xz", 'r:xz')
            tar.extractall()
            tar.close()

            print("unzip mpfr")
            tar = tarfile.open("mpfr.tar.xz", 'r:xz')
            tar.extractall()
            tar.close()

            print("unzip gmp")
            tar = tarfile.open("gmp.tar.xz", 'r:xz')
            tar.extractall()
            tar.close()


            print("unzip mpc ")
            tools.unzip("mpc.tar.gz")

            with tools.chdir('gcc-%s' % (self.gcc_version)):
                os.symlink('../gmp-%s' % (self.gmp_version), 'gmp')
                os.symlink('../mpfr-%s' % (self.mpfr_version), 'mpfr')
                os.symlink('../mpc-%s' % (self.mpc_version), 'mpc')

    def build(self):
        self.run('gcc --version')
        self.run('g++ --version')
        self.run('gfortran --version')
        with tools.chdir('./src'):
            with tools.environment_append({'package_folder' : self.package_folder,
                                           'binutils_version' : self.binutils_version,
                                           'gcc_version' : self.gcc_version,
                                           'glibc_version' : self.glibc_version,
                                           'linux_major' : self.linux_major,
                                           'linux_version' : self.linux_version,
                                           'mpfr_version' : self.mpfr_version,
                                           'gmp_version' : self.gmp_version,
                                           'mpc_version' : self.mpc_version}):
                self.run('./make-aarch64-toolchain.sh')

    def package(self):
        pass

    def package_info(self):
        bin_folder=os.path.join(self.package_folder, "bin")
        self.env_info.CONAN_CMAKE_GENERATOR ="Unix Makefiles"
        self.env_info.CONAN_CMAKE_FIND_ROOT_PATH = os.path.join(self.package_folder, self.target_host, "sysroot")
        self.env_info.path.append(bin_folder)
        self.env_info.CHOST=self.target_host
        self.env_info.AR="%s-ar" % (self.target_host)
        self.env_info.AS="%s-as" % (self.target_host)
        self.env_info.RANLIB="%s-ranlib" % (self.target_host)
        self.env_info.CC="%s-%s" % (self.target_host, self.cc_compiler)
        self.env_info.FC="%s-%s" % (self.target_host, self.fortran_compiler)
        self.env_info.CXX="%s-%s" % (self.target_host, self.cxx_compiler)
        self.env_info.LD ="%s-ld" % (self.target_host)
        self.env_info.STRIP="%s-strip" % (self.target_host)
