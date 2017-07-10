#!/bin/bash
#Install nginx server

if [ -d /usr/local/Pnginx ];then
  echo "Nginx already is Installed"
  exit 1
fi

basePath="/data/tools"
 cd ${basePath}/soft
  mv /usr/local/src/ /tmp/src/
  mkdir -p /usr/local/src/
  unzip  master.zip -d /usr/local/src/ 
  tar zxf nginx-1.10.1.tar.gz
  cd nginx-1.10.1
patch -p0 < /usr/local/src/nginx_upstream_check_module-master/check_1.11.1+.patch
./configure --user=nobody --group=nobody --prefix=/usr/local/Pnginx/  \
--with-http_stub_status_module \
--with-http_gzip_static_module \
--with-pcre \
--with-http_secure_link_module \
--with-http_random_index_module \
--with-http_addition_module \
--with-http_sub_module \
--with-http_dav_module \
--with-http_flv_module \
--with-http_stub_status_module \
--with-http_gunzip_module \
--with-http_gzip_static_module \
--with-http_ssl_module \
--with-http_realip_module \
--with-file-aio \
--with-stream \
--add-module=/usr/local/src/nginx_upstream_check_module-master

make && make install 
  if [ $? = 0 ];then
      echo -e "\e[32mInstall Nginx Success!\e[0m"
  else
      echo -e "\e[31mInstall Nginx Error!\e[0m"
      exit
  fi


#gpasswd -a hhlyadmin nobody >/dev/null 2>&1
#setfacl -R -m hhlyadmin:rwx /usr/local/Pnginx

