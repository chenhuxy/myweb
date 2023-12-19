FROM centos:7
RUN mkdir /myweb
ADD . /myweb/
#RUN yum install python3 python3-devel gcc -y --nogpgcheck \
#&& ln -sf /usr/share/zoneinfo/Asia/Chongqing /etc/localtime \
#&& pip3 --trusted-host files.pythonhosted.org install --user -r /myweb/requirements/require.txt
#RUN rm -rf /etc/yum.repos.d/* \
#&& curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo \
RUN yum install python3 python3-devel gcc -y --nogpgcheck \
&& ln -sf /usr/share/zoneinfo/Asia/Chongqing /etc/localtime \
&& chmod +x /myweb/entrypoint.sh \
&& pip3 install uwsgi==2.0.23 \
&& pip3 --trusted-host pypi.tuna.tsinghua.edu.cn install --user -r /myweb/requirements/require.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8000 8001
WORKDIR /myweb
ENTRYPOINT ["./entrypoint.sh"]
