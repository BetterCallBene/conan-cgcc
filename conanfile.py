from conans import ConanFile, CMake, tools

import tarfile
import os, sys

class GCCCrossCompilerConan(ConanFile):
    name = "GCCCrossCompiler"
    version = "5.4.0"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "Create a GCC Cross-Compiler"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    binutils_version = "2.26.1"
    gcc_version = "5.4.0"
    glibc_version = "2.23"
    linux_major = "4"
    linux_version = "4.4.119"
    mpfr_version = "4.0.1"
    gmp_version = "6.1.2"
    mpc_version = "1.1.0"

    exports_sources=["src/*"]

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
        self.cpp_info.libs = ["GCCCrossCompiler"]

