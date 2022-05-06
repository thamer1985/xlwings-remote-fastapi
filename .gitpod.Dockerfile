FROM gitpod/workspace-full

USER gitpod

COPY ./requirements.txt ./requirements.txt

RUN pyenv update \
    && pyenv install 3.10.2 \
    && pyenv global 3.10.2 \
    && python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && python -m pip install beautifulsoup4 \
    && python -m pip install playwright \
    && python -m playwright install \
    && playwright install-deps