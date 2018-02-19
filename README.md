# face-search
This is a demonstration of a face search system

Work flows:
* Detect faces from the images
* Crop the face to 224x224 pixels
* Align the face
* Feed face images through a feature extractor (I use vgg face feature extractor)
* Save the vector representations into database along with images names and url
* Queries run very fast thanks to Postgres's CUBE extension

This demo works on Ubuntu 16.04 LTS with Python 2.7, my laptop details:
* CPU: Intel core i5-4210U @1.7GHz
* RAM: 8GB DDR3
* GPU: NVIDIA GTX 840M

## Installation 
### OpenCV for python
Details instruction: https://gist.github.com/trungkak/a934e92b3829a025f98a0b3419fad2da

### CUDA, tensorflow, keras installation
Details instruction: https://gist.github.com/trungkak/3d9d0c1b9dda91623488a5e4a3373053

### Postgres installation
Details instruction: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04


## Preparation
Get into src directory
```bash
cd /src
```
Open .env file then enter your config (DBName, USER, PASSWORD)
```bash
vi .env
```

To do things from scratch, download a face dataset like LFW (http://vis-www.cs.umass.edu/lfw/)

```bash
cd ../images
wget http://vis-www.cs.umass.edu/lfw/lfw-funneled.tgz
tar zxvf lfw-funneled.tgz
```

## Running
To index your images data, use:
```bash
python app.py -path <path-to-your-images-directory>
```

To identify a person, use:
```bash
python app.py -image <path-to-your-image>
```

To get help, use:
```bash
python app.py -h
```

## Resources
* Deep Face Recognition: [Link](https://www.robots.ox.ac.uk/~vgg/publications/2015/Parkhi15/parkhi15.pdf)
* Face search at scale, 80 million gallery: [Link](https://arxiv.org/abs/1507.07242)

## Author
* **Trung Le Hoang** (trungkak@gmail.com)


