# WH-SUEPS-wryleigh
Hi! I made a little repository for the SUEP stuff, basically a place where we can share code with each other as we're working on it. 
So far I've added a little tutorial/intro to pyroot, and a root file you can use for the tutorial. It's just one of the signal samples we're looking at for WH (simulated data), you can access it through LXplus when your cern accounts are all set up but in the meantime you'll want to download it from here and just upload it to wherever you are running the Jupyter notebook from.
I need to clean it up a bit but soon I'll add the code I have for muon trigger efficiencies and you can read through it and start thinking about what would need to be modified to do the same for electrons.


For logging into LXPLus: 
```
$ ssh -X -Y your_cern_user@lxplus.cern.ch
 ```
 (we need lxplus 7)
 ```
$ ssh lxplus723.cern.ch
```
 to build environment:
 ```
$ sh setup.sh
```


To run the efficiency scripts: 
```
$python MC_muon_efficiency.py --input "signal_sample_file_name"
```
for example, if I am running it on /eos/user/j/jreicher/SUEP/WH_private_signals/merged/WHleptonicpythia_hadronic_M125.0_MD4.00_T1.00_HT-1_UL16APV_NANOAOD.root, I would type 
```--input "WHleptonicpythia_hadronic_M125.0_MD4.00_T1.00_HT-1_UL16APV_NANOAOD"```
