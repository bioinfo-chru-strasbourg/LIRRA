#import docker image plink and change her tag
docker pull biocontainers/plink1.9:v1.90b6.6-181012-1-deb_cv1
docker image tag biocontainers/plink1.9:v1.90b6.6-181012-1-deb_cv1 plink:1.9

#import docker images hap-ibd & beagle & variantconvert
docker pull eliseverin/hap-ibd:1.0
docker pull eliseverin/beagle:5.4
docker pull eliseverin/variantconvert:1.2.2