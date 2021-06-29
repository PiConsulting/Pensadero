#!/bin/bash

set -euxo pipefail
RSTUDIO_BIN="/usr/sbin/rstudio-server"

if [[ ! -f "$RSTUDIO_BIN" && $DB_IS_DRIVER = "TRUE" ]]; then
  apt-get update
  apt-get install -y gdebi-core
  cd /tmp
  # You can find new releases at https://rstudio.com/products/rstudio/download-server/debian-ubuntu/.
  wget https://download2.rstudio.org/server/trusty/amd64/rstudio-server-1.2.5001-amd64.deb
  sudo gdebi -n rstudio-server-1.2.5001-amd64.deb
  rstudio-server restart || true
fi
