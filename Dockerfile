# Inherit from an upstream image
#
# To update the base image, look at more recent image tags at
# https://quay.io/repository/jupyter/scipy-notebook?tab=tags&tag=latest
FROM quay.io/jupyter/scipy-notebook:2024-03-31

COPY environment.yml /tmp/environment.yml

RUN mamba env update --prefix ${CONDA_DIR} --file /tmp/environment.yml

RUN mkdir -p /opt/conda/share/jupyter/lab/settings \
 && cp overrides.json /opt/conda/share/jupyter/lab/settings

COPY image-tests image-tests
RUN ls
