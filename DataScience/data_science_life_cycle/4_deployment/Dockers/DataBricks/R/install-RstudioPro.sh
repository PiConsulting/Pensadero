#!/bin/bash

set -euxo pipefail

if [[ $DB_IS_DRIVER = "TRUE" ]]; then
  sudo apt-get update
  sudo dpkg --purge rstudio-server # in case open source version is installed.
  sudo apt-get install -y gdebi-core alien

  ## Installing RStudio Server Pro
  cd /tmp

  # You can find new releases at https://rstudio.com/products/rstudio/download-commercial/debian-ubuntu/.
  wget https://download2.rstudio.org/server/trusty/amd64/rstudio-server-pro-1.2.5001-3-amd64.deb
  sudo gdebi -n rstudio-server-pro-1.2.5001-3-amd64.deb

  ## Configuring authentication
  sudo echo 'auth-proxy=1' >> /etc/rstudio/rserver.conf
  sudo echo 'auth-proxy-user-header-rewrite=^(.*)$ $1' >> /etc/rstudio/rserver.conf
  sudo echo 'auth-proxy-sign-in-url=$DB_DOMAIN/login.html' >> /etc/rstudio/rserver.conf
  sudo echo 'admin-enabled=1' >> /etc/rstudio/rserver.conf
  sudo echo 'export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' >> /etc/rstudio/rsession-profile

  # Enabling floating license
  sudo echo 'server-license-type=remote' >> /etc/rstudio/rserver.conf

  # Session configurations
  sudo echo 'session-rprofile-on-resume-default=1' >> /etc/rstudio/rsession.conf
  sudo echo 'allow-terminal-websockets=0' >> /etc/rstudio/rsession.conf

  sudo rstudio-server license-manager license-server <"$LICENSE_URL">
  sudo rstudio-server restart || true
fi
