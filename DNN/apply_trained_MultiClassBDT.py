#!/usr/bin/env python

# Select Theano as backend for Keras
import ROOT
from os import environ

from ROOT import TMVA, TFile, TString, TLegend, THStack, TTree, TBranch
from array import array
from subprocess import call
from os.path import isfile

def main():
    # Setup TMVA
    TMVA.Tools.Instance()
    TMVA.PyMethodBase.PyInitialize()
    reader = TMVA.Reader("Color:!Silent")

    # Check files exist
    if not isfile('samples/DiLepTR_ttH_bInclude.root'):
        print 'No such input file: samples/DiLepTR_ttH_bInclude.root'
    if not isfile('samples/DiLepTR_ttJets_bInclude.root'):
        print 'No such input file: samples/DiLepTR_ttJets_bInclude.root'
    if not isfile('samples/DiLepTR_ttV_bInclude.root'):
        print 'No such input file: samples/DiLepTR_ttV_bInclude.root'

    # Open files and load ttrees
    data_ttH = TFile.Open('samples/DiLepTR_ttH_bInclude.root')
    data_ttV = TFile.Open('samples/DiLepTR_ttV_bInclude.root')
    data_ttJets = TFile.Open('samples/DiLepTR_ttJets_bInclude.root')
    data_ttH_tree = data_ttH.Get('BOOM')
    data_ttV_tree = data_ttV.Get('BOOM')
    data_ttJets_tree = data_ttJets.Get('BOOM')

    #variable_list = [('Jet_numLoose'), ('maxeta'), ('mindrlep1jet'), ('mindrlep2jet'), ('SR_InvarMassT'), ('corrptlep1'), ('corrptlep2'), ('hadTop_BDT := max(hadTop_BDT,-1.)'), ('Hj1_BDT := max(Hj1_BDT,-1.)')]
    variable_list = [('maxeta'),('mindrlep1jet'),('mindrlep2jet'),('SR_InvarMassT'),('corrptlep1'),('corrptlep2')]
    branches = {}

    #hadTop_BDT = -999
    #Hj1_BDT = -999
    # Register names of inputs with reader. Together with the name give the address of the local variable that carries the updated input variables during event loop.
    for branchName in variable_list:
        #if 'hadTop_BDT' in branchName:
        #    branches[branchName] = array('f', [max(hadTop_BDT,-1.)])
        #elif 'Hj1_BDT' in branchName:
        #    branches[branchName] = array('f', [max(Hj1_BDT,-1.)])
        #else:
        #    branches[branchName] = array('f', [-999])
        branches[branchName] = array('f', [-999])
        print 'Add variable name %s to reader ' % branchName
        print 'Add variable address %s to reader ' % branches[branchName]
        reader.AddVariable(branchName, branches[branchName])
        #data_ttH_tree.SetBranchAddress(branchName, branches[branchName])
        #data_ttV_tree.SetBranchAddress(branchName, branches[branchName])
        #data_ttJets_tree.SetBranchAddress(branchName, branches[branchName])

    # Keep track of event numbers for cross-checks.
    event_number = array('f',[0])
    data_ttH_tree.SetBranchAddress('EVENT_event', event_number)
    reader.AddSpectator('EVENT_event', event_number)

    # Define outputs: files to store histograms/ttree with results from application of classifiers and any histos/trees themselves.
    output_file_name = 'ttHML_MultiClassBDT_application.root'
    output_file = TFile.Open(output_file_name,'RECREATE')
    histo_ttHnode_ttHsample = ROOT.TH1D('histo_ttHnode_ttHsample','BDT Response ttH sample on ttH node',100,0,1)
    histo_ttVnode_ttHsample = ROOT.TH1D('histo_ttVnode_ttHsample','BDT Response ttH sample on ttV node',100,0,1)
    histo_ttJetsnode_ttHsample = ROOT.TH1D('histo_ttJetsnode_ttHsample','BDT Response ttH sample on ttJets node',100,0,1)

    # Book methods
    # First argument is user defined name. Doesn not have to be same as training name.
    # True type of method and full configuration are read from the weights file specified in the second argument.
    reader.BookMVA('BDT', TString('MultiClass_BDTG/weights/TMVAClassification_BDTG.weights.xml'))

    # Loop over ttH ttree evaluating MVA as we go.
    response_ttH = 0.0
    # Keep track of the response and input values assigned to every event number for later checks.
    event_num_ttH_node = []
    temp_percentage_done = 0
    for i in range(data_ttH_tree.GetEntries()):
        percentage_done = int(100*float(i)/float(data_ttH_tree.GetEntries()))
        if percentage_done % 10 == 0:
            if percentage_done != temp_percentage_done:
                print percentage_done
                temp_percentage_done = percentage_done
        data_ttH_tree.GetEntry(i)
        '''print 'Jet_numLoose: ', data_ttH_tree.Jet_numLoose
        print 'maxeta: ', data_ttH_tree.maxeta
        print 'mindrlep1jet: ', data_ttH_tree.mindrlep1jet
        print 'mindrlep2jet: ', data_ttH_tree.mindrlep2jet
        print 'SR_InvarMassT: ', data_ttH_tree.SR_InvarMassT
        print 'corrptlep1: ', data_ttH_tree.corrptlep1
        print 'corrptlep2: ', data_ttH_tree.corrptlep2
        print 'hadTop_BDT: ', data_ttH_tree.hadTop_BDT
        print 'Hj1_BDT: ', data_ttH_tree.Hj1_BDT
        print '--- BDT Response ---'
        print 'Event number: ', data_ttH_tree.EVENT_event
        print 'ttH node: ', reader.EvaluateMulticlass('BDT')[0]
        print 'ttV node: ', reader.EvaluateMulticlass('BDT')[1]
        print 'ttJets node: ', reader.EvaluateMulticlass('BDT')[2]
        '''
        maxeta = data_ttH_tree.maxeta
        mindrlep1jet = data_ttH_tree.mindrlep1jet
        mindrlep2jet = data_ttH_tree.mindrlep2jet
        SR_InvarMassT = data_ttH_tree.SR_InvarMassT
        corrptlep1 = data_ttH_tree.corrptlep1
        corrptlep2 = data_ttH_tree.corrptlep2
        hadTop_BDT = data_ttH_tree.hadTop_BDT
        Hj1_BDT = data_ttH_tree.Hj1_BDT

        event_num = array('f',[0])
        event_num = data_ttH_tree.EVENT_event
        ttHnode_response = array('f',[0])
        ttHnode_response = reader.EvaluateMulticlass('BDT')[0]
        histo_ttHnode_ttHsample.Fill(reader.EvaluateMulticlass('BDT')[0])
        histo_ttVnode_ttHsample.Fill(reader.EvaluateMulticlass('BDT')[1])
        histo_ttJetsnode_ttHsample.Fill(reader.EvaluateMulticlass('BDT')[2])
        event_num_ttH_node.append((event_num,ttHnode_response, data_ttH_tree.maxeta, data_ttH_tree.mindrlep1jet, data_ttH_tree.mindrlep2jet, data_ttH_tree.SR_InvarMassT, data_ttH_tree.corrptlep1, data_ttH_tree.corrptlep2, data_ttH_tree.hadTop_BDT, data_ttH_tree.Hj1_BDT))

    # Write and close output file.
    histo_ttHnode_ttHsample.Write()
    histo_ttVnode_ttHsample.Write()
    histo_ttJetsnode_ttHsample.Write()
    output_file.Close()

    # Open training file and check that when event numbers match the response and input values are the same (otherwise application is wrong).
    test_output = TFile.Open('ttHML_MultiClassBDTG_new.root')
    test_tree = test_output.Get("MultiClass_BDTG/TestTree")
    #for i in range(train_tree.GetEntries()):
    for i in range(0,50):
        test_tree.GetEntry(i)
        for evnum , resp, max_eta, mindrl1j, mindrl2j, InvM, ptlep1, ptlep2, hadtopBDT, hj1BDT in event_num_ttH_node:
            if test_tree.EVENT_event == evnum:
                BDTG_testbranch = test_tree.GetBranch('BDTG')
                BDTG_ttH_leaf = BDTG_testbranch.GetLeaf("ttH")
                if BDTG_ttH_leaf.GetValue() != resp:
                    print '**** Response from application of weights does NOT match training response! ****'
                    print 'event number ', test_tree.EVENT_event
                    print 'ttH training value: ', BDTG_ttH_leaf.GetValue()
                    print 'Application value: ', resp
                    print 'Training maxeta: ', test_tree.maxeta
                    print 'Application max_eta: ', max_eta
                    print 'Training mindrlep1jet: ', test_tree.mindrlep1jet
                    print 'Application mindrl1j: ', mindrl1j
                    print 'Training mindrlep2jet: ', test_tree.mindrlep2jet
                    print 'Application mindrl2j: ', mindrl2j
                    print 'Training SR_InvarMassT: ', test_tree.SR_InvarMassT
                    print 'Application InvM: ', InvM
                    print 'Training corrptlep1: ', test_tree.corrptlep1
                    print 'Application ptlep1: ', ptlep1
                    print 'Training corrptlep2: ', test_tree.corrptlep2
                    print 'Application ptlep2: ', ptlep2
                    #print 'Training hadTop_BDT: ', test_tree.hadTop_BDT
                    #print 'Application hadtopBDT: ', hadtopBDT
                    #print 'Training Hj1_BDT: ', test_tree.Hj1_BDT
                    #print 'Application hj1BDT: ', hj1BDT


main()
