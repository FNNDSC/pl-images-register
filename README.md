# Multiple image registration

[![Version](https://img.shields.io/docker/v/fnndsc/pl-images-register?sort=semver)](https://hub.docker.com/r/fnndsc/pl-images-register)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-images-register)](https://github.com/FNNDSC/pl-images-register/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-images-register/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-images-register/actions/workflows/ci.yml)

`pl-images-register` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which takes in ...  as input files and
creates ... as output files.

## Abstract

This plugin registers one or more images from its input directory to a single reference or fixed image.

## Installation

`pl-images-register` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can
run from either within _ChRIS_ or the command-line.

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-images-register` as a container:

```shell
apptainer exec docker://fnndsc/pl-images-register images_register [--args values...] input/ output/
```

To print its available options, run:

```shell
apptainer exec docker://fnndsc/pl-images-register images_register --help
```

## Examples

`images_register` requires two positional arguments: a directory containing input images, i.e.
a fixed_image and a moving_image, and a directory where to create output data, i.e. registered_image and 
transform_matrix. First, create the input directory and move input data into it.

```shell
mkdir incoming outgoing
mv fixed_image.nii.gz moving_image.nii.gz incoming
apptainer exec docker://fnndsc/pl-images-register:latest images_register [--args] incoming outgoing
```
If there is only one moving image, it will be registered onto the fixed image. 
All images (fixed, moving, and registered images) should be in `.nii.gz` format.
The registered image and the transform matrix will be saved with these names:

`moving_image.nii.gz` --> `moving_image_registered.nii.gz` and `moving_image_transform.mat`.

Example 1:
```shell 
Inputs: 
    input_dir/fixed_image.nii.gz
    input_dir/moving_image.nii.gz 
    
Outputs:
    output_dir/moving_image_registered.nii.gz
    output_dir/moving_image_transform.mat
```
If there are multiple moving images, each one will be registered to the fixed image separately.
For multiple moving images, all of them should be placed in a folder, and the folder should be passed to the 
parser under `moving_images_folder`.

Example 2:
```shell 
Inputs: 
    input_dir/fixed_image.nii.gz
    input_dir/moving_images_folder/moving_image1.nii.gz, moving_image2.nii.gz, moving_image3.nii.gz, etc.

Outputs:
    output_dir/moving_images_folder/moving_image1_registered.nii.gz, moving_image2_registered.nii.gz, 
        moving_image3.nii.gz, etc.
    output_dir/moving_images_folder/moving_image1_transform.mat, moving_image2_transform.mat, 
        moving_image3_transform.mat, etc.
```
## Development

The registration algorithms are found in images_register.py module.

### Building

Build a local container image:

```shell
docker build -t localhost/fnndsc/pl-images-register .
```

### Running

Mount the source code `images_register.py` into a container to try out changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/images_register.py:/usr/local/lib/python3.12/site-packages/images_register.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-images-register images_register /incoming /outgoing
```

### Testing

Run unit tests using `pytest`.
It's recommended to rebuild the image to ensure that sources are up-to-date.
Use the option `--build-arg extras_require=dev` to install extra dependencies for testing.

```shell
docker build -t localhost/fnndsc/pl-images-register:dev --build-arg extras_require=dev .
docker run --rm -it localhost/fnndsc/pl-images-register:dev pytest
```

## Release

Steps for release can be automated by [Github Actions](.github/workflows/ci.yml).
This section is about how to do those steps manually.

### Increase Version Number

Increase the version number in `setup.py` and commit this file.

### Push Container Image

Build and push an image tagged by the version. For example, for version `1.2.3`:

```
docker build -t docker.io/fnndsc/pl-images-register:1.2.3 .
docker push docker.io/fnndsc/pl-images-register:1.2.3
```

### Get JSON Representation

Run [`chris_plugin_info`](https://github.com/FNNDSC/chris_plugin#usage)
to produce a JSON description of this plugin, which can be uploaded to _ChRIS_.

```shell
docker run --rm docker.io/fnndsc/pl-images-register:1.2.3 chris_plugin_info -d docker.io/fnndsc/pl-images-register:1.2.3 > chris_plugin_info.json
```

Intructions on how to upload the plugin to _ChRIS_ can be found here:
https://chrisproject.org/docs/tutorials/upload_plugin

