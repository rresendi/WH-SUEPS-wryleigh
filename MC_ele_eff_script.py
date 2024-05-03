import uproot
import os
import argparse

import numpy as np
import ROOT

from array import array

input_file = "/eos/user/j/jreicher/SUEP/WH_private_signals/merged/WHleptonicpythia_leptonic_M125.0_MD1.00_T0.25_HT-1_UL16_NANOAOD.root"

# Sets batch mode so no popup window
ROOT.gROOT.SetBatch(True)

import argparse, types


# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("--input", help = "Name of input file", type = str)
args = vars(parser.parse_args())

# Name of sample
sample_name= args["input"]

output_file="MC_e_efficiencies.root"
input_file= "/eos/user/j/jreicher/SUEP/WH_private_signals/merged/"+sample_name + ".root"

# suep decay type
if "generic" in sample_name:
    decay_type = "generic"
elif "hadronic" in sample_name:
    decay_type = "hadronic"
else:
    decay_type = "leptonic"


    # conditions for what year

if "UL18" in sample_name:
    year = "2018 conditions"
    folder = "ele_eff_outputs_2018/"
elif "UL17" in sample_name:
    year = "2017 conditions"
    folder = "ele_eff_outputs_2017/"
elif "UL16APV" in sample_name:
    year = "2016 APV conditions"
    folder = "ele_eff_outputs_2016APV/"
else:
    year = "2016 conditions"
    folder = "ele_eff_outputs_2016/"

    
    # dark meson (phi) mass

if "MD2.00" in sample_name:
    md = "2.00 [GeV]"
elif "MD4.00" in sample_name:
    md = "4.00 [GeV]"
elif "MD3.00" in sample_name:
    md = "3.00 [GeV]"
elif "MD8.00" in sample_name:
    md = "8.00 [GeV]"
elif "MD1.00" in sample_name:
    md = "1.00 [GeV]"
else:
    md = "1.40 [GeV]"
    
    # temperature
    
if "T0.25" in sample_name:
    temp = "0.25"
if "T0.35" in sample_name:
    temp = "0.35"
if "T0.50" in sample_name:
    temp = "0.50"
elif "T0.75" in sample_name:
    temp = "0.75"
elif "T1.00" in sample_name:
    temp = "1.00"
elif "T1.50" in sample_name:
    temp = "1.50"
elif "T2.00" in sample_name:
    temp = "2.00"
elif "T3.00" in sample_name:
    temp = "3.00"
elif "T4.00" in sample_name:
    temp = "4.00"
elif "T8.00" in sample_name:
    temp = "8.00"
elif "T12.00" in sample_name:
    temp = "12.00"
elif "T16.00" in sample_name:
    temp = "16.00"
elif "T32.00" in sample_name:
    temp = "32.00"
else:
    temp = "6.00"
    
# Gets relevant variables from file
def Events(f):
    evs = f['Events'].arrays(['HLT_Ele32_WPTight_Gsf',
                'HLT_Ele115_CaloIdVT_GsfTrkId',
                'Electron_pt',
                'Electron_eta',
                'Electron_dz',
                'Electron_dxy',
                'Electron_pfRelIso03_all',
                'Electron_pfRelIso03_chg',
                'Electron_cutBased'])
    return evs

# Gets medium ID electrons from file

evs = f['Events'].arrays(['Electron_cutBased','Electron_pt'])
elpt = evs['Electron_pt']
idevs = elpt[(evs["Electron_cutBased"][3])]
    
# Defines binning and histograms
ele_bin_edges=array('d',[0,2,4,6,8,10,12,
                         14,16,18,20,22,
                         24,26,28,30,32,
                         34,36,38,40,50,
                         60,70,80,90,100,
                         120,140,160,180,200])
# Histograms for overall efficiency
ele_totalhist=ROOT.TH1D("total_events","Total Events",len(ele_bin_edges)-1,ele_bin_edges)
ele_filthist=ROOT.TH1D("filt_events","Filtered Events",len(ele_bin_edges)-1,ele_bin_edges)

# Split into three regions of eta
eta1_ele_totalhist=ROOT.TH1D("total_events","Total Events",len(ele_bin_edges)-1,ele_bin_edges)
eta1_ele_filthist=ROOT.TH1D("filt_events","Filtered Events",len(ele_bin_edges)-1,ele_bin_edges)
eta2_ele_totalhist=ROOT.TH1D("total_events","Total Events",len(ele_bin_edges)-1,ele_bin_edges)
eta2_ele_filthist=ROOT.TH1D("filt_events","Filtered Events",len(ele_bin_edges)-1,ele_bin_edges)
eta3_ele_totalhist=ROOT.TH1D("total_events","Total Events",len(ele_bin_edges)-1,ele_bin_edges)
eta3_ele_filthist=ROOT.TH1D("filt_events","Filtered Events",len(ele_bin_edges)-1,ele_bin_edges)
# Function for filling the histograms

def ele_hists(events,etas,hists):
    ele_totalhist = hists[0]
    ele_filthist = hists[1]
    eta_min = etas[0]
    eta_max = etas[1]
    # trigger
    triggerSingleElectron = (
            events["HLT_Ele32_WPTight_Gsf"]
            | events["HLT_Ele115_CaloIdVT_GsfTrkIdT"]
        )
    # quality requirements for electrons
    ele_quality_check = (
                (events["Electron_cutBased"][3])
                & (events["Electron_pt"] > 35)
                & (np.abs(events["Electron_eta"]) < 2.5)
                & (np.abs(events["Electron_dz"]) < 0.1)
                & (np.abs(events["Electron_dxy"]) < 0.05)
                & (events["Electron_pfRelIso03_chg"] < 0.25)
                & (events["Electron_pfRelIso03_all"] < 0.25)
            )
    # cut on eta
    eta_split = (
        (np.abs(events["Electron_eta"]) >= eta_min)
        & (np.abs(events["Electron_eta"]) < eta_max )
    )
    # Select based on trigger
    ele = events["Electron_pt"]
    evs = ele[ele_quality_check & eta_split]
    tr_evs = evs[triggerSingleElectron]

    #Fill histograms
    for ev in evs:
        for entry in ev:
            ele_totalhist.Fill(entry)
    for ev in tr_evs:
        for entry in ev:
            ele_filthist.Fill(entry)

    return 0

with uproot.open(input_file) as f:
    evs = Events(f)
    eta_split = [[0.0,2.4],[0.0,0.9],[0.9,2.1],[2.1,2.4]]
    eta_hists = [[ele_totalhist,ele_filthist],[eta1_ele_totalhist,eta1_ele_filthist],[eta2_ele_totalhist,eta2_ele_filthist],[eta3_ele_totalhist,eta3_ele_filthist]]
    for (etas,hists) in zip(eta_split,eta_hists):
        ele_hists(evs,etas,hists)
# Fills efficiency
eta1_effs = ROOT.TEfficiency(eta1_ele_filthist,eta1_ele_totalhist)
eta2_effs = ROOT.TEfficiency(eta2_ele_filthist,eta2_ele_totalhist)
eta3_effs = ROOT.TEfficiency(eta3_ele_filthist,eta3_ele_totalhist)
c1 = ROOT.TCanvas ("canvas","",800,600)

# Get overall Efficiency:
ele_eff = mu_filthist.Clone()

ele_eff.SetName(sample_name)
ele_eff.Sumw2()
ele_eff.Divide(ele_totalhist)


ele_eff.Sumw2()
ele_eff.Divide(ele_totalhist)
    

# Creates Efficiency Plot w legend

eta1_effs.SetTitle("Electron Trigger Efficiency in bins of pT;Electron pT [GeV];Efficiency")
legend = ROOT.TLegend(0.5,0.1,0.9,0.4)
legend.AddEntry(eta1_effs,"|#eta|<0.9","")
legend.AddEntry(eta2_effs,"0.9<|#eta|<2.1","")
legend.AddEntry(eta3_effs,"2.1<|#eta|<2.4","")
legend.AddEntry(ROOT.nullptr, temp+" [GeV], "+year,"")
legend.AddEntry(ROOT.nullptr,"SUEP decay type: "+decay_type,"")
legend.AddEntry(ROOT.nullptr,"Dark meson mass = "+ md+ " SUEP mass = 125.0 GeV","")
legend.SetTextColor(ROOT.kBlack)
legend.SetTextFont(42)
legend.SetTextSize(0.03)

# Draw plot

eta1_effs.Draw()
eta2_effs.SetLineColor(ROOT.kRed)
eta2_effs.Draw("same")
eta3_effs.SetLineColor(ROOT.kBlue)
eta3_effs.Draw("same")
legend.Draw("same")
c1.Update()
# Saves to pdf
c1.SaveAs(folder+sample_name+"_Efficiency.pdf")

# Saves overall efficiency


root_file = ROOT.TFile(output_file,"UPDATE")
root_file.cd()

eff_dir=root_file.Get("Efficiencies")
if not eff_dir:
    eff_dir=root_file.mkdir("Efficiencies")
eff_dir.cd()
ele_eff.Write()

root_file.Close()
    

try:
    root_file = uproot.update(output_file)
    root_file[sample_name] = ele_eff
except (OSError, IOError) as e:
    root_file = uproot.create(output_file)
    root_file[sample_name] = ele_eff



print("sample "+sample_name+" complete")
