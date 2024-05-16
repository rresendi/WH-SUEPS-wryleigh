#!/bin/bash                                                                                                                                                                                                           
source /cvmfs/cms.cern.ch/cmsset_default.sh
export X509_USER_PROXY=x509up_u257692
voms-proxy-info





echo "hostname"
hostname

echo "filename"
echo $2

xrdcp root://cmsxrootd.fnal.gov//$2 local.root


cat /etc/os-release
export SYSTEM_RELEASE=`cat /etc/redhat-release`
if [[ $SYSTEM_RELEASE == *"release 7"* ]]; then
    scram_arch=slc7_amd64_gcc10
    cmssw_version=CMSSW_12_4_8
elif [[ $SYSTEM_RELEASE == *"release 8"* ]]; then
    scram_arch=el8_amd64_gcc10
    cmssw_version=CMSSW_12_4_8

elif [[ $SYSTEM_RELEASE == *"release 9"* ]]; then
    scram_arch=el9_amd64_gcc11
    cmssw_version=CMSSW_13_3_3
else
    echo "No default scram_arch for current OS!"
    return 1;
fi
echo "scram arch:"
echo $scram_arch
echo "cmssw version:"
echo $cmssw_version

export SCRAM_ARCH=$scram_arch
cmsrel $cmssw_version
cd $cmssw_version/src
cmsenv
cd ../..
#source /cvmfs/cms.cern.ch/common/crab-setup.sh                                                                                                                                                                       


echo "ls"

ls

python3 dat_muon_efficiency.py  --era "2016"

filename=$(basename "$2")
echo "basename filename"
echo $filename
xrdcp out.root root://submit50.mit.edu//cmauceri/dat_mu_effs_2016/$filename


echo "----- transferring output to scratch :"
echo " ------ THE END (everyone dies !) ----- "

