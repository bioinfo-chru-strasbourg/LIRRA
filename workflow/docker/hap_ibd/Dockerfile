##########################################################################
# Dockerfile Version:   1.0                                              #
# Software:             hap_ibd	                                         #
# Software Version:     1.0                                              #
# Software Website:                                                      #
# Description:          Dockerfile to build hap_ibd     container image  #
##########################################################################


########
# FROM #
########

FROM centos:7
LABEL name="Verin Hameau Elise " \
	Software="hap_ibd" \
	Version="1.0" \
	Description="hap_ibd"

RUN yum -y install sudo make wget bzip2 gcc	
RUN yum -y install  git 

##########
#java    #
##########
RUN yum -y install java java-1.8.0 
RUN yum -y install java-devel


#####################
#install hap_ibd    #
#####################
RUN git clone https://github.com/browning-lab/hap-ibd.git
RUN javac -cp hap-ibd/src/ hap-ibd/src/hapibd/HapIbdMain.java
RUN jar cfe hap-ibd.jar hapibd/HapIbdMain -C hap-ibd/src/ ./
RUN jar -i hap-ibd.jar

CMD [ "/usr/bin/java", "-jar", "/hap-ibd.jar" ] 






