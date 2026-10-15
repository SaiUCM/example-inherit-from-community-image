# Inherit from an upstream image
#
# To update the base image, look at more recent image tags at
# https://quay.io/repository/jupyter/scipy-notebook?tab=tags&tag=latest
FROM quay.io/jupyter/scipy-notebook:2024-03-31


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

# Python is pinned in environment.yml so the solver sees it as a
# constraint up front rather than re-resolving afterwards.
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