#!/bin/bash

if [[ $# -ne 2 ]]; then
  echo "Wrong number of arguments ( $# )"
  echo "First Argument is either 1 or 2"
  echo "   1:  Do the initial time consuming build"
  echo "   2:  Do the installation"
  echo "Second argument is a buildname:"
  echo "   i.e. \$(whoami)"
  exit -1
fi

## The anaconda python version can screw up the build
## just use the sytstem python
export PATH=${PATH//anaconda/XXX}

BUILD_MODE=$1
USER_DIR=$2

## If you dont have a scratch directory change USER_BASE to
## the folder that holds your home directory,
## typically either User for OS X or home for linux, but this may
## vary depending on your system

USER_BASE=${HOME}
#USER_BASE=Users

BASE_DIR=${USER_BASE}/local/llvm
mkdir -p ${BASE_DIR}
if [ ! -d ${BASE_DIR} ]; then
  echo "ERROR: ${BASE_DIR} does not exists"
  exit -1
fi

#VERSION="/tags/RELEASE_370/final"
#VERSION=trunk
##  SVN
VERSION=tags/RELEASE_700/final
NAME=llvm_RELEASE_700
INSTALL_DIR=/${USER_BASE}/local #/opt/${NAME}

if [ ${BUILD_MODE} -eq 1 ]; then

 cd ${BASE_DIR} && \
      svn co http://llvm.org/svn/llvm-project/llvm/${VERSION} ${NAME}
 cd ${BASE_DIR}/${NAME}/projects && \
      svn co http://llvm.org/svn/llvm-project/compiler-rt/${VERSION} compiler-rt
      svn co http://llvm.org/svn/llvm-project/openmp/trunk openmp
      svn co http://llvm.org/svn/llvm-project/libcxxabi/${VERSION} libcxxabi
      svn co http://llvm.org/svn/llvm-project/test-suite/${VERSION} test-suite
      svn co http://llvm.org/svn/llvm-project/libcxx/${VERSION} libcxx

 cd ${BASE_DIR}/${NAME}/tools && \
        svn co http://llvm.org/svn/llvm-project/cfe/${VERSION} clang


 cd ${BASE_DIR}/${NAME}/tools/clang/tools && \
        svn co http://llvm.org/svn/llvm-project/clang-tools-extra/${VERSION} extra

 mkdir -p ${BASE_DIR}/${NAME}-build
 cd ${BASE_DIR}/${NAME}-build

 export  CC=/usr/bin/clang
 export  CXX=/usr/bin/clang++

 echo "Configuring via cmake"

 cmake ../${NAME} \
      -DCMAKE_C_COMPILER:PATH=/usr/bin/clang \
      -DCMAKE_CXX_COMPILER:PATH=/usr/bin/clang++ \
      -DCMAKE_BUILD_TYPE:STRING=Release \
      -DCMAKE_INSTALL_PREFIX:PATH=${INSTALL_DIR} \
      -DLLVM_ENABLE_LIBCXX:BOOL=ON \
      -DLLVM_ENABLE_LIBCXXABI:BOOL=ON \
      -DLLVM_BUILD_EXTERNAL_COMPILER_RT:BOOL=ON

 #  autoconf build mechanism ../${NAME}/configure --prefix=${INSTALL_DIR}  --enable-optimized

  echo "starting make"

## Default number of cpus is 2
  NUM_CPU=2

## Try to get num cpu from system
  if [ uname == "Darwin" ] ; then
    NUM_CPU=$(sysctl -n hw.cpu)
  fi

  if [ uname == "Linux" ] ; then
    NUM_CPU=$( lscpu | grep "CPU(s):" | head -1 | awk '{print $2}' )
## get the first line of lscpu that mentions CPU(s): and print the second column
## (that has then number of cpus
  fi
  make -j ${NUM_CPU}

# echo sudo ln -s /Applications/Xcode.app/Contents/Developer/Toolchains//XcodeDefault.xctoolchain/usr/include/c++ ./c++

##  /opt/llvm_trunk/bin/clang-tidy  -fix      -checks=-*,clang-analyzer-*,-clang-analyzer-security.insecureAPI.rand,-clang-analyzer-alpha.core.PointerArithm,-clang-analyzer-alpha.unix.Stream,-clang-analyzer-alpha.security.ReturnPtrRange,-clang-analyzer-security.FloatLoopCounter      -p ~/src/vxl-bld/      ~/src/vxl/contrib/brl/bseg/boxm2/*.cxx |tee /tmp/logger_1 2>&1
fi

if [[ ${BUILD_MODE} -eq 2 ]]; then

if [[ $(id -u) -ne 0 ]]; then
  echo "You may need to run this script with sudo for installiation: ($(id -u))"
  echo "  sudo $0 $@"
#  exit -1
fi
cd ${BASE_DIR}/${NAME}-build
make install
#make install-libcxx install-libcxxabi

echo "Installing ${INSTALL_DIR}/bin/scan-cmake-build"
echo "copying scan-build"
cp ${BASE_DIR}/${NAME}/tools/clang/tools/scan-build/scan-build ${INSTALL_DIR}/bin/scan-build
cat > ${INSTALL_DIR}/bin/scan-cmake-build << EOF
#!/bin/bash
## \author Hans J. Johnson
## Inspired from https://redmine.lighttpd.net/projects/lighttpd2/wiki/ClangAnalyzer
export PATH="${INSTALL_DIR}/bin/:\${PATH}"
${INSTALL_DIR}/bin/scan-build make "\$@"
##/opt/llvm_trunk/bin/scan-build make "\$@"
EOF
chmod oug+x ${INSTALL_DIR}/bin/scan-cmake-build

echo "Installing ${INSTALL_DIR}/bin/scan-cmake-configure"
echo "copying cccanalyzers"
if [[ ! -d "${INSTALL_DIR}/libexec" ]]; then
  mkdir -p ${INSTALL_DIR}/libexec
fi
cp ${BASE_DIR}/${NAME}/tools/clang/tools/scan-build/ccc-analyzer ${INSTALL_DIR}/libexec/ccc-analyzer
cp ${BASE_DIR}/${NAME}/tools/clang/tools/scan-build/c++-analyzer ${INSTALL_DIR}/libexec/c++-analyzer

cp ${BASE_DIR}/${NAME}/tools/clang/tools/scan-build/ccc-analyzer ${INSTALL_DIR}/bin/ccc-analyzer
cp ${BASE_DIR}/${NAME}/tools/clang/tools/scan-build/c++-analyzer ${INSTALL_DIR}/bin/c++-analyzer

cat > ${INSTALL_DIR}/bin/scan-cmake-configure << EOF
#!/bin/bash
## \author Hans J. Johnson
## Inspired from https://redmine.lighttpd.net/projects/lighttpd2/wiki/ClangAnalyzer
export PATH="${INSTALL_DIR}/bin/:\${PATH}"
cmake \
    -DCMAKE_C_COMPILER=${INSTALL_DIR}/libexec/ccc-analyzer \
  -DCMAKE_CXX_COMPILER=${INSTALL_DIR}/libexec/c++-analyzer \
  "\$@"
EOF
chmod oug+x ${INSTALL_DIR}/bin/scan-cmake-configure

echo "DONE"
echo << EOF
   Now to build stuff:

echo "Get a code base"
#cd ~/src
cd /${USER_BASE}/${USER_DIR}/src
git clone http://github.com/vxl/vxl.git
mkdir -p vxl-scanbuild
cd vxl-scanbuild/

echo "USE SUBSTITUTE cmake wrapper"
scan-cmake-configure  \
-DBUILD_CORE_GEOMETRY:BOOL=OFF \
-DBUILD_CORE_IMAGING:BOOL=OFF \
-DBUILD_CORE_SERIALISATION:BOOL=OFF \
-DBUILD_CORE_UTILITIES:BOOL=OFF \
-DBUILD_CORE_VIDEO:BOOL=OFF \
-DBUILD_EXAMPLES:BOOL=OFF \
-DCMAKE_BUILD_TYPE:STRING=Debug \
/${USER_BASE}/${USER_DIR}/src/vxl

echo "USE SUBSTITUTE make wrapper"
scan-cmake-build  -j $(sysctl -n hw.ncpu)

EOF
fi


