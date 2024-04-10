# Inherit from an upstream image
#
# To update the base image, look at more recent image tags at
# https://quay.io/repository/jupyter/scipy-notebook?tab=tags&tag=latest
#
# FIXME: for any tag later than 2023-10-20, the image should be
#        quay.io/jupyter/scipy-notebook and not just jupyter/scipy-notebook
#        as they have migrated from dockerhub to quay.io.
#
FROM jupyter/scipy-notebook:2023-06-26

COPY environment.yml /tmp/environment.yml

RUN mamba env update --prefix ${CONDA_DIR} --file /tmp/environment.yml

COPY image-tests image-tests
RUN ls
