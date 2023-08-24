FROM centos:7
RUN mkdir /myweb
ADD . /myweb/
RUN yum install python3 python3-devel gcc -y --nogpgcheck \
&& ln -sf /usr/share/zoneinfo/Asia/Chongqing /etc/localtime \
&& pip3 --trusted-host files.pythonhosted.org install --user -r /myweb/requirements/require.txt
EXPOSE 8000
WORKDIR /myweb
ENTRYPOINT ["./entrypoint.sh"]
