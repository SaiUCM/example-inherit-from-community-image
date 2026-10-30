# Inherit from an upstream image
#
# To update the base image, look at more recent image tags at
# https://quay.io/repository/jupyter/scipy-notebook?tab=tags&tag=latest
FROM quay.io/jupyter/scipy-notebook:2026-10-28

# Install chromium outside /home/jovyan so it survives the JupyterHub
# persistent-storage volume mount that shadows the home directory at runtime.
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright

# Switch to root user
USER root

# Command line as root user
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    fonts-dejavu \
    gfortran \
    gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan user
USER ${NB_UID}

COPY environment.yml /tmp/environment.yml

RUN mamba env update --prefix ${CONDA_DIR} --file /tmp/environment.yml && \
    python -m bash_kernel.install && \
    mamba clean --all -y && \
    pip cache purge

# datascience 0.17.5 uses pkg_resources (removed in setuptools 84+).
# Patch maps.py to use importlib.resources instead.
COPY patch_datascience.py /tmp/patch_datascience.py
RUN python /tmp/patch_datascience.py

COPY overrides.json /opt/conda/share/jupyter/lab/settings/overrides.json

# Install Playwright system deps and Chromium browser as root.
# Uses the Python playwright CLI (available after mamba env update above).
# Chromium is placed at PLAYWRIGHT_BROWSERS_PATH outside /home/jovyan so it
# survives the JupyterHub persistent-storage volume mount at runtime.
USER root
RUN playwright install-deps chromium && \
    mkdir -p ${PLAYWRIGHT_BROWSERS_PATH} && \
    playwright install chromium && \
    chmod -R a+rX ${PLAYWRIGHT_BROWSERS_PATH}

# Copy image-tests to /home/jovyan (local docker testing) and /srv/repo
# (repo2docker-action with REPO_DIR=/srv/repo runs pytest from /srv/repo).
RUN mkdir -p /srv/repo
COPY image-tests /home/jovyan/image-tests
COPY image-tests /srv/repo/image-tests
RUN chown -R ${NB_UID}:${NB_GID} /home/jovyan/image-tests /srv/repo

USER ${NB_UID}

