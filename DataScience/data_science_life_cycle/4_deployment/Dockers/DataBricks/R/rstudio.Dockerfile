FROM databricksruntime/R:latest

COPY *-Rstudio*.sh .
RUN chmod +x *-Rstudio*.sh

#RUN DB_DOMAIN=<domain> && LICENSE_URL=<license_server> && ./install-Rstudio.sh
RUN ./install-Rstudio.sh

RUN ./libraries-Rstudio.sh
