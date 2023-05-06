FROM node:19-buster-slim

RUN apt-get update -qq \
  && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
    bash \
    git \
    jq \
    vim \
    libasound2 \
    libgbm-dev \
    libgconf-2-4 \
    libgtk-3-0 \
    libgtk2.0-0 \
    libnotify-dev \
    libnss3 \
    libxss1 \
    libxtst6 \
    ncurses-dev \
    procps \
    xauth \
    xvfb \
  && apt-get clean \
  && rm -rf /var/cache/apt/archives/* \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
  && truncate -s 0 /var/log/*log

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn

ADD . /app

ARG CLIENT_ENV
ARG CLIENT_VERSION
ENV CLIENT_ENV=$CLIENT_ENV
ENV CLIENT_VERSION=$CLIENT_VERSION

ENV EDITOR vim
ENV PS1 "\[\033[38;5;2m\]\t\[$(tput sgr0)\] \[$(tput sgr0)\]\[\033[38;5;2m\][\[$(tput sgr0)\]\[\033[38;5;11m\]cd-frontend\[$(tput sgr0)\]:\[$(tput sgr0)\]\[\033[38;5;6m\]\w\[$(tput sgr0)\]\[\033[38;5;2m\]]\[$(tput sgr0)\]\[\033[38;5;231m\]:\[$(tput sgr0)\] \[$(tput sgr0)\]"

RUN yarn build

VOLUME ["/app/build"]

EXPOSE 3000

CMD yarn start
