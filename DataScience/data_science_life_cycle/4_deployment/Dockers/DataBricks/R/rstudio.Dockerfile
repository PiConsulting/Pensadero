FROM databricksruntime/standard:latest

## update indices
RUN apt-get update -qq \
    # install two helper packages we need
    && apt-get install --no-install-recommends software-properties-common dirmngr gpg-agent --yes\
    # import the signing key (by Michael Rutter) for these repo
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 \
    # add the R 4.0 repo from CRAN -- adjust 'focal' to 'groovy' or 'bionic' as needed
    && add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"

# get CRAN Packages
RUN add-apt-repository ppa:c2d4u.team/c2d4u4.0+
# install R
RUN apt-get install --no-install-recommends r-base make gdebi-core --yes
# install R-studio
RUN wget https://download2.rstudio.org/server/trusty/amd64/rstudio-server-1.2.5001-amd64.deb \
    && gdebi -n rstudio-server-1.2.5001-amd64.deb \
    && rm rstudio-server-1.2.5001-amd64.deb

COPY libraries-Rstudio.sh .
RUN chmod +x libraries-Rstudio.sh && ./libraries-Rstudio.sh

RUN printf "rstudio-server restart || exit 1\nexit0" >> /etc/rc.local

EXPOSE 8787
