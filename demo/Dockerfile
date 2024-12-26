FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  curl \
  software-properties-common \
  git \
  \
  # Install Neovim 10
  && add-apt-repository ppa:neovim-ppa/stable && apt-get update && \
  apt-get install -y neovim\
  \
  # Rephrasinator dependencies
  && apt-get install -y python3-pip python3-full pipx \
  # TODO: start ollama server
  && curl -fsSL https://ollama.com/install.sh | sh \
  # Clean up
  && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /root/.config/nvim
COPY ./demo/init.lua /root/.config/nvim/init.lua
COPY ./demo/testfile.md /root/testfile.md

# Install Rephrasinator dependencies
RUN curl -fsSL https://raw.githubusercontent.com/antonkesy/rephrasinator.nvim/main/requirements.txt | \
  xargs -n 1 pip install --break-system-packages --ignore-installed

RUN nvim --headless +PackerSync +qall

# start ollama server and pull phi3:14b
RUN ollama serve & sleep 5 & ollama pull phi3:14b

CMD ["nvim", "/root/testfile.md"]
