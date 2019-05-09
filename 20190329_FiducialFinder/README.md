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

Clone the BRAINSia/NiftyNet repo, this is where we will be doing our work to add landmark detection features
```bash
cd ~
git clone git@github.com:BRAINSia/NiftyNet.git
cd NiftyNet && git checkout landmark_app_20190405

```

### Starting your own network
```bash
# setup the structure for your network
cd 20190329_FiducialFinder/
./scripts/add-network.sh my_new_network
```

#### Helpful Docs
[coursera landmark detection video](https://www.coursera.org/lecture/convolutional-neural-networks/landmark-detection-OkD3X)

### Explanation of Project/Next Steps
[Landmark Application PowerPoint](https://docs.google.com/presentation/d/14Jy9_Uk4HuA6hSIgpnmZBGoT7NCk1DFTTiyHCKAQTWE/edit?usp=sharing)
