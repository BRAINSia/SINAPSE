# Fiducial Finder
> Alex Powers and Chase Johnson

#### Project Motivation
The goal of this project is to identify the left and right eye from an MRI of the human head.

#### Technologies
| Framework  |   Docs  | Usage |
| :-------:  | :------:| :----:|  
| NiftyNet   | [docs](https://niftynet.readthedocs.io/en/dev/) | Deep Learning for Medical Images| 
| Tensorflow | [docs](https://www.tensorflow.org/api_docs/python/tf)| Base of NiftyNet |  

#### Environment
TODO: figure out how to get the optimized deep-learning env into a environment.yml file

```bash
# Get the NiftyNet Submodule for the first time
git submodule update --init --recursive 
cd 20190329_FiducialFinder/NiftyNet/
git checkout dev && git pull
# otherwise
cd 20190329_FiducialFinder/NiftyNet/ && git pull
```

### Starting your own network
```bash
# setup the structure for your network
cd 20190329_FiducialFinder/
./scripts/add-network.sh my_new_network
```

#### Helpful Docs
[git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) .
[coursera landmark detection video](https://www.coursera.org/lecture/convolutional-neural-networks/landmark-detection-OkD3X)
