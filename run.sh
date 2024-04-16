#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el9_amd64_gcc12
cmsrel CMSSW_13_3_0
cd CMSSW_13_3_0/src/
cmsenv
cd ../..
source /cvmfs/cms.cern.ch/common/crab-setup.sh

# replace this with x509up_u<your mit user id>
export X509_USER_PROXY=x509up_u257692

echo "hostname"
hostname

echo "filename"
echo $2


xrdcp root://cmsxrootd.fnal.gov//"$2" "local.root"

echo "ls"
ls
python3 dat_muon_efficiency.py --era "2016"
filename=$(basename "$2")


echo "----- transferring output to scratch :"
echo " ------ THE END (everyone dies !) ----- "

