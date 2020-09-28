set -e # exit on command failure
PYCONFIG=/usr/bin/python3-config
SSTCOREPREFIX=$HOME/local/sst/sstcore-10.0.0
SSTELEMENTSPREFIX=$HOME/local/sst/sstelements-10.0.0
cd sstcore-10.0.0
ls
./configure --prefix=$SSTCOREPREFIX --with-python=$PYCONFIG
make -j4
make install
cd ..
cd sst-elements-library-10.0.0
./configure --prefix=$SSTELEMENTSPREFIX --with-sst-core=$SSTCOREPREFIX --with-python=$PYCONFIG
make -j4
make install
