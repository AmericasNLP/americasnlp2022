#! /bin/bash

HOME_DIR=${1}
URL=https://rcweb.dartmouth.edu/homes/f00458c/americasnlp2/
DOWNLOAD_DIR=${HOME_DIR}/downloads
mkdir -p ${DOWNLOAD_DIR}\

for lang in Bribri Guarani Kotiria Quechua Waikhana
do

  wget -nc ${URL}${lang}TrainDev.tar.gz -P ${DOWNLOAD_DIR}
  tar -xzf ${DOWNLOAD_DIR}/${lang}TrainDev.tar.gz -C ${HOME_DIR}
  echo Finished downloading ${lang}
done
