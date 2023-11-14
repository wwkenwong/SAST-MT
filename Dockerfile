FROM ubuntu:21.10

WORKDIR "/root/"
COPY build_treesitter_parser.py /root/build_treesitter_parser.py
COPY ./src/ /root/fuzzer/

RUN apt-get -y update &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    bison \
    bzip2 \
    cmake \
    creduce \
    curl \
    flex \
    gcc \
    gcc-multilib \
    g++ \
    git \
    libgmp3-dev \
    ninja-build \
    python3-venv \
    python3-pip \
    python3-setuptools \
    python3-dev \
    texinfo \
    wget \ 
    vim \
    unzip \
    screen \
    libev-dev \
    clang-format\
    sudo



RUN wget https://github.com/github/codeql-cli-binaries/releases/download/v2.8.1/codeql-linux64.zip
RUN wget https://github.com/github/codeql/archive/refs/tags/codeql-cli/v2.8.1.zip

RUN unzip codeql-linux64.zip
RUN unzip v2.8.1.zip

RUN apt install -y python-dev wget 
RUN apt install -y python3-dev  
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN apt install -y libev-dev clang-format
RUN pip3 install comby
RUN wget get.comby.dev
RUN mv ./index.html ./get_comby.sh 
RUN chmod +x ./get_comby.sh
RUN /root/get_comby.sh

RUN pip3 install tree-sitter==0.19.0
RUN git clone https://github.com/tree-sitter/tree-sitter-cpp.git
RUN git clone https://github.com/tree-sitter/tree-sitter-c.git
RUN python3 build_treesitter_parser.py

