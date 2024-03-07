# [[file:../org/Docker.org::+BEGIN_SRC dockerfile][No heading:1]]
FROM alpine:3.18.4
# No heading:1 ends here

# [[file:../org/Docker.org::+BEGIN_SRC dockerfile][No heading:2]]
RUN apk add --no-cache bash=5.2.15-r5 && \
    apk add --no-cache emacs=28.2-r8 && \
    apk add --no-cache graphviz=8.0.5-r1 && \
    apk add --no-cache ttf-dejavu=2.37-r5 && \
    apk add --no-cache git=2.40.1-r0 && \
    apk add --no-cache plantuml=1.2023.6-r0 && \
    mkdir ~/.emacs.d
# No heading:2 ends here

# [[file:../org/Docker.org::+BEGIN_SRC dockerfile][No heading:3]]
# Set the working directory within the container
WORKDIR /root/.emacs.d

# Copy necessary files to the container
COPY resources/install.el .
COPY resources/site-start.el .
# No heading:3 ends here

# [[file:../org/Docker.org::+BEGIN_SRC dockerfile][No heading:4]]
# Set the working directory within the container
RUN emacs --load /root/.emacs.d/install.el --batch
# No heading:4 ends here
