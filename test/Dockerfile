FROM centos/systemd
ENV container docker
RUN yum clean all
RUN yum install -y sudo openssh-server openssh-clients which curl ansible; yum clean all
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''
RUN ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N ''

RUN if ! getent passwd kitchen; then                 useradd -d /home/kitchen -m -s /bin/bash -p '*' kitchen;               fi
RUN echo "kitchen ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN echo "Defaults !requiretty" >> /etc/sudoers
RUN mkdir -p /home/kitchen/.ssh
RUN chown -R kitchen /home/kitchen/.ssh
RUN chmod 0700 /home/kitchen/.ssh
RUN touch /home/kitchen/.ssh/authorized_keys
RUN chown kitchen /home/kitchen/.ssh/authorized_keys
RUN chmod 0600 /home/kitchen/.ssh/authorized_keys
RUN echo '<%= IO.read(@public_key).strip %>' >> /home/kitchen/.ssh/authorized_keys
RUN sed -i.kitchen '/UsePAM/d'  /etc/ssh/sshd_config
RUN echo 'UsePrivilegeSeparation no' >> /etc/ssh/sshd_config
RUN echo 'UsePAM no' >> /etc/ssh/sshd_config
RUN systemctl enable sshd.service
