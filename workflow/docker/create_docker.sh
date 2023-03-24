#import docker image plink and change her tag
docker pull biocontainers/plink1.9:v1.90b6.6-181012-1-deb_cv1
docker image tag biocontainers/plink1.9:v1.90b6.6-181012-1-deb_cv1 plink:1.9
docker rmi biocontainers/plink1.9:v1.90b6.6-181012-1-deb_cv1