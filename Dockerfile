FROM debian:stretch
MAINTAINER Aleksandr Butenko <nigillus42@gmailcom>

#ENV RDKIT_VERSION Release_2018_03_1
#ENV HOME /root
#WORKDIR /root

#RUN dnf clean all && dnf -y update
#RUN dnf install python3-rdkit

#RUN dnf clean all && dnf -y update \
#    && dnf install \
#    python-pip, \
#    python3-rdkit, \
#    python-numpy

# Download dependencies
#RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
#RUN rm -f /usr/bin/python && ln -s /usr/local/bin/python /usr/bin/python

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y python-pip python-rdkit less python-cairocffi


#	apt-get install -y build-essential software-properties-common && \
#	apt-get install -y byobu curl git htop man unzip vim wget less && \
#	apt-get install -y flex bison python-numpy sqlite3 libsqlite3-dev && \
#	apt-get clean && \
#	rm -rf /var/lib/apt/lists/*
#
#RUN	wget https://cmake.org/files/v3.11/cmake-3.11.1.tar.gz && tar xzf cmake-3.11.1.tar.gz && \
#	cd cmake-3.11.1 && ./configure --prefix=/opt/cmake && make && make install && rm ../cmake-3.11.1.tar.gz
#
#RUN cd /usr/local/ && wget https://dl.bintray.com/boostorg/release/1.63.0/source/boost_1_63_0.tar.gz && \
#    tar xzf ./boost_1_63_0.tar.gz
#RUN cd /usr/local/boost_1_63_0 && ./bootstrap.sh --prefix=/usr/local --with-python=python3 --with-libraries=python,serialization && \
#    export CPLUS_INCLUDE_PATH=/usr/local/include/python3.6m/ && ./b2 --debug-configuration && ./b2 install && rm ../boost_1_63_0.tar.gz
#
#
## Compile rdkit
#ADD https://github.com/rdkit/rdkit/archive/$RDKIT_VERSION.tar.gz /root/
#RUN tar xzvf $RDKIT_VERSION.tar.gz && rm $RDKIT_VERSION.tar.gz
#
#RUN cd /root/rdkit-$RDKIT_VERSION/External/INCHI-API && \
#	./download-inchi.sh
#
#RUN mkdir /root/rdkit-$RDKIT_VERSION/build && \
#	cd /root/rdkit-$RDKIT_VERSION/build && \
#	/opt/cmake/bin/cmake -DRDK_BUILD_INCHI_SUPPORT=ON -DBOOST_ROOT=/usr/local/boost_1_63_0 -DBoost_NO_SYSTEM_PATHS=ON \
#	   -D BOOST_LIBRARYDIR=/usr/local/lib/ -D BOOST_INCLUDEDIR=/usr/local/include/ \
#       -DPYTHON_LIBRARY=/usr/local/lib/python3.6/config-3.6m-x86_64-linux-gnu/libpython3.6m.a \
#	   -DPYTHON_INCLUDE_DIR=/usr/local/include/python3.6m/ -DPYTHON_EXECUTABLE=/usr/local/bin/python3.6 .. && \
#	make && \
#	make install
#
## Set environmental variables
#ENV RDBASE /root/rdkit-$RDKIT_VERSION
#ENV LD_LIBRARY_PATH $RDBASE/lib
#ENV PYTHONPATH $PYTHONPATH:$RDBASE
#
WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

RUN pip install https://github.com/JamesRamm/longclaw/zipball/master && \
    pip freeze --local


#FROM python:3.5
#
#ENV RDKIT_VERSION Release_2018_03_1
#ENV HOME /root
#WORKDIR /root
#
#WORKDIR /opt
#
#RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
#	apt-get update && \
#	apt-get -y upgrade && \
#	apt-get install -y build-essential software-properties-common && \
#	apt-get install -y byobu curl git htop man unzip vim wget less
#
#RUN wget https://sourceforge.net/projects/boost/files/boost/1.64.0/boost_1_64_0.tar.bz2 && \
#    tar --bzip2 -xf boost_1_64_0.tar.bz2 && \
#    rm boost_1_64_0.tar.bz2
#
#RUN cd boost_1_64_0/tools/build && \
#    # Symlink the Python header files to the standard location.
#    # This is important as the base image comes with custom Python 3.5 build
#    # and thus the location of the header files is different.
#    ln -s /usr/local/include/python3.5m /usr/local/include/python3.5 && \
#    ./bootstrap.sh && \
#    ./b2 install --prefix=/opt/boost_build && \
#    ln -s /opt/boost_build/bin/b2 /usr/bin/b2 && \
#    ln -s /opt/boost_build/bin/bjam /usr/bin/bjam && \
#    cd /opt/boost_1_64_0 && \
#    # Specify Python version explicitly as solution to https://github.com/boostorg/build/issues/194
#    echo "using python : 3.5 ;" >> /etc/site-config.jam && \
#    b2 --with-python toolset=gcc stage
#
### Compile rdkit
#ADD https://github.com/rdkit/rdkit/archive/$RDKIT_VERSION.tar.gz /opt/
#RUN tar xzvf $RDKIT_VERSION.tar.gz && rm $RDKIT_VERSION.tar.gz
#
#RUN cd /opt/rdkit-$RDKIT_VERSION/External/INCHI-API && \
#	./download-inchi.sh
#
#RUN mkdir /opt/rdkit-$RDKIT_VERSION/build && \
#	cd /opt/rdkit-$RDKIT_VERSION/build && \
#	cmake -DRDK_BUILD_INCHI_SUPPORT=ON -DBOOST_ROOT=/opt/boost_1_64_0 -DBoost_NO_SYSTEM_PATHS=ON \
#	   -D BOOST_INCLUDEDIR=/usr/local/include .. && \
#	make && \
#	make install
#
## Set environmental variables
#ENV RDBASE /root/rdkit-$RDKIT_VERSION
#ENV LD_LIBRARY_PATH $RDBASE/lib
#ENV PYTHONPATH $PYTHONPATH:$RDBASE
#
#WORKDIR /app
#ADD . /app
#
#RUN pip install -r requirements.txt