#!/bin/bash

# if you need cvmfs or a given architecture
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_10_6_30_patch1/src/;
cmsenv;
source /cvmfs/cms.cern.ch/common/crab-setup.sh;
cd ~/condor_start
export SCRAM_ARCH=slc7_amd64_gcc820
export HOME=.
export X509_USER_PROXY=x509up_u257692
use_x509userproxy=true
echo "hostname"
hostname

echo "filename"
echo $2
voms-proxy-info
input_file="TEST_filelist.txt"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "File $input_file does not exist."
    exit 1
fi

# Loop through each line in the input file
while IFS= read -r filename; do
    # Check if the filename is not empty
    if [ -n "$filename" ]; then
        xrdcp root://cmsxrootd.fnal.gov//"$filename" local.root
        # Run the Python script with the current filename as input
        python2 dat_muon_efficiency.py --input "$filename"
        rm local.root
    fi
    done < "$input_file"




echo "----- transferring output to scratch :"
echo " ------ THE END (everyone dies !) ----- "
