FROM almalinux:9

RUN dnf -y install epel-release
RUN dnf -y install gcc wget git procps htop && dnf clean all

# docker
RUN dnf -y install dnf-plugins-core
RUN dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
RUN dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# not tested yet : use bioinfo user
# the docker group seems to be created already, but bioinfo needs to be in a group with the same ID as the docker group outside of the container (991)
RUN groupadd -g 1000 bioinfo && \
    groupadd -g 991 docker2 && \
    useradd -m -u 1000 -g bioinfo bioinfo && \
    usermod -aG docker2 bioinfo && \
    usermod -aG wheel bioinfo
USER bioinfo

# install conda from miniforge
RUN wget https://github.com/conda-forge/miniforge/releases/download/25.3.0-3/Miniforge3-25.3.0-3-Linux-x86_64.sh && \
    chmod +x Miniforge3-25.3.0-3-Linux-x86_64.sh && \
    ./Miniforge3-25.3.0-3-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniforge3-25.3.0-3-Linux-x86_64.sh && \
    /opt/conda/bin/conda init && \
    ln -s /opt/conda/bin/conda /usr/local/bin/conda
ENV PATH="/opt/conda/bin:$PATH"
