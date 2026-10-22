# Inherit from an upstream image but keeping the python version as 3.11
FROM quay.io/jupyter/scipy-notebook:python-3.11
#FROM quay.io/jupyter/scipy-notebook:2026-03-09 
# You can also inherit from pangeo base image instead. Remove the
# previous line and uncomment the next line
# FROM pangeo/pangeo-notebook:2026.01.30

# We copy the `environment.yml` file in this repo, only adding in extra
# packages that aren't in our base image.
COPY environment.yml /tmp/environment.yml
RUN mamba env update --prefix ${CONDA_DIR} --file /tmp/environment.yml && \
    mamba clean --all --force-pkgs-dirs --yes

# Writes the Jupyter Kernelspec. The Conda package alone does not 
# register Bash in the launcher.
RUN python -m bash_kernel.install

# `playwright install-deps` only pulls OS libraries; the browser itself
# is a separate install. Browsers default to ~/.cache/ms-playwright,
# which the hub's persistent home volume mounts over at runtime, so
# they go outside $HOME.

ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright
USER root
RUN playwright install --with-deps chromium && \
    chmod -R a+rX /opt/playwright
USER ${NB_UID}

COPY overrides.json /opt/conda/share/jupyter/lab/settings/overrides.json

COPY image-tests image-tests
