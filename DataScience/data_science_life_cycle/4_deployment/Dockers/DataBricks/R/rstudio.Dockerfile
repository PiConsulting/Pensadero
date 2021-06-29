FROM databricksruntime/standard:latest

# update indices
RUN apt update -qq \
    # install two helper packages we need
    && apt install --no-install-recommends software-properties-common dirmngr \
    # import the signing key (by Michael Rutter) for these repo
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 \
    # add the R 4.0 repo from CRAN -- adjust 'focal' to 'groovy' or 'bionic' as needed
    && add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"

RUN apt install --no-install-recommends r-base --yes

# get CRAN Packages
RUN add-apt-repository ppa:c2d4u.team/c2d4u4.0+

COPY libraries-Rstudio.sh .
RUN chmod +x libraries-Rstudio.sh && ./libraries-Rstudio.sh

COPY init-Rstudio.sh .
RUN cat init-Rstudio.sh >> ~/.profile
