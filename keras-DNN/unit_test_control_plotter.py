from plotting.control_plotter import control_plotter
from collections import OrderedDict
import os
def main():
    CPlotter = control_plotter()
    output_dir = 'control_plots_2019-05-09/'

    CPlotter.check_dir(output_dir)
    files_list = []
    files_list_SR = []
    files_list_training = []
    input_path_ttH_training = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/TrainMVA_20190315/loose/NoJetNCut/ttHnobb_NoJetNCut.root')[0]
    input_path_ttJ_training = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/TrainMVA_20190315/loose/NoJetNCut/ttJets_NoJetNCut.root')[0]
    input_path_ttW_training = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/TrainMVA_20190315/loose/NoJetNCut/ttWJets_NoJetNCut.root')[0]
    input_path_ttZ_training = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/TrainMVA_20190315/loose/NoJetNCut/ttZJets_NoJetNCut.root')[0]

    input_path_ttH_HWW_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/TTH_hww_SigRegion.root')[0]
    input_path_ttH_HZZ_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/TTH_hzz_SigRegion.root')[0]
    input_path_ttH_Htautau_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/TTH_htt_SigRegion.root')[0]
    input_path_ttH_Hmm_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/TTH_hmm_SigRegion.root')[0]
    input_path_ttH_Hother_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/TTH_hot_SigRegion.root')[0]
    input_path_Conv_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/Conv_SigRegion.root')[0]
    input_path_Fakes_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/Fakes_SigRegion.root')[0]
    input_path_Flips_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/Flips_SigRegion.root')[0]
    input_path_ttW_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/TTW_SigRegion.root')[0]
    input_path_ttZ_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/TTZ_SigRegion.root')[0]
    input_path_ttWW_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/TTWW_SigRegion.root')[0]
    input_path_EWK_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/EWK_SigRegion.root')[0]
    input_path_data_signalregion = CPlotter.getEOSlslist(directory='/b/binghuan/Rootplas/rootplas_20190227/SigRegion/SigRegion/Data_SigRegion.root')[0]

    files_list.append(input_path_Conv_signalregion)
    files_list.append(input_path_Fakes_signalregion)
    files_list.append(input_path_Flips_signalregion)
    files_list.append(input_path_ttW_signalregion)
    files_list.append(input_path_ttZ_signalregion)
    files_list.append(input_path_ttH_HWW_signalregion)
    files_list.append(input_path_ttH_HZZ_signalregion)
    files_list.append(input_path_ttH_Htautau_signalregion)
    files_list.append(input_path_ttH_Hmm_signalregion)
    files_list.append(input_path_ttH_Hother_signalregion)
    files_list.append(input_path_ttWW_signalregion)
    files_list.append(input_path_EWK_signalregion)
    files_list.append(input_path_data_signalregion)

    files_list_SR.append(input_path_Conv_signalregion)
    files_list_SR.append(input_path_Fakes_signalregion)
    files_list_SR.append(input_path_Flips_signalregion)


    #files_list_training.append(input_path_ttH_training)
    files_list_training.append(input_path_ttJ_training)
    #files_list_training.append(input_path_ttW_training)
    #files_list_training.append(input_path_ttZ_training)

    files_ = CPlotter.open_files(files_list)
    files_SR_ = CPlotter.open_files(files_list_SR)
    files_training_ = CPlotter.open_files(files_list_training)


    branch_list = [
    #'Jet_numLoose',
    #'nBJetLoose',
    #'nBJetMedium',
    #'jet1_pt',
    #'jet1_eta',
    #'jet1_phi',
    #'jet1_E',
    #'jet2_pt',
    #'jet2_eta',
    #'jet2_phi',
    #'jet2_E',
    #'jet3_pt',
    #'jet3_eta',
    #'jet3_phi',
    #'jet3_E',
    #'jet4_pt',
    #'jet4_eta',
    #'jet4_phi',
    #'jet4_E',
    #'lep1_conePt',
    #'lep1_eta',
    #'lep1_phi',
    'lep1_E',
    'lep2_conePt',
    'lep2_eta',
    'lep2_phi',
    'lep2_E',
    'resTop_BDT',
    'Hj_tagger_resTop',
    'metLD',
    'maxeta',
    'massL',
    'mindr_lep1_jet',
    'mindr_lep2_jet',
    'avg_dr_jet',
    'mT_lep1',
    'mT_lep2',
    'mbb',
    'n_presel_ele',
    'n_presel_mu',
    'Dilep_pdgId',
    'lep1_charge'
    ]

    #files_histname_dict = CPlotter.load_histos(files_,branch_list,'syncTree')

    # Start building histogram names you wish to plot (check 'load_histograms' in plotting class).
    # Can simply use the elements of previous dictionary or plottings sum hists class to create summed histogram.
    file_ttH_training_keyname = input_path_ttH_training.split('/')[-1:]
    file_ttH_training_keyname = file_ttH_training_keyname[0].split('.')[:-1]
    file_ttJ_training_keyname = input_path_ttJ_training.split('/')[-1:]
    file_ttJ_training_keyname = file_ttJ_training_keyname[0].split('.')[:-1]
    file_ttW_training_keyname = input_path_ttW_training.split('/')[-1:]
    file_ttW_training_keyname = file_ttW_training_keyname[0].split('.')[:-1]
    file_ttZ_training_keyname = input_path_ttZ_training.split('/')[-1:]
    file_ttZ_training_keyname = file_ttZ_training_keyname[0].split('.')[:-1]

    file_ttH_HWW_signalregion_keyname = input_path_ttH_HWW_signalregion.split('/')[-1:]
    file_ttH_HWW_signalregion_keyname = file_ttH_HWW_signalregion_keyname[0].split('.')[:-1]
    file_ttH_HZZ_signalregion_keyname = input_path_ttH_HZZ_signalregion.split('/')[-1:]
    file_ttH_HZZ_signalregion_keyname = file_ttH_HZZ_signalregion_keyname[0].split('.')[:-1]
    file_ttH_Htautau_signalregion_keyname = input_path_ttH_Htautau_signalregion.split('/')[-1:]
    file_ttH_Htautau_signalregion_keyname = file_ttH_Htautau_signalregion_keyname[0].split('.')[:-1]
    file_ttH_Hmm_signalregion_keyname = input_path_ttH_Hmm_signalregion.split('/')[-1:]
    file_ttH_Hmm_signalregion_keyname = file_ttH_Hmm_signalregion_keyname[0].split('.')[:-1]
    file_ttH_Hoth_signalregion_keyname = input_path_ttH_Hother_signalregion.split('/')[-1:]
    file_ttH_Hoth_signalregion_keyname = file_ttH_Hoth_signalregion_keyname[0].split('.')[:-1]
    file_Conv_signalregion_keyname = input_path_Conv_signalregion.split('/')[-1:]
    file_Conv_signalregion_keyname = file_Conv_signalregion_keyname[0].split('.')[:-1]
    file_Fakes_signalregion_keyname = input_path_Fakes_signalregion.split('/')[-1:]
    file_Fakes_signalregion_keyname = file_Fakes_signalregion_keyname[0].split('.')[:-1]
    file_Flips_signalregion_keyname = input_path_Flips_signalregion.split('/')[-1:]
    file_Flips_signalregion_keyname = file_Flips_signalregion_keyname[0].split('.')[:-1]
    file_ttW_signalregion_keyname = input_path_ttW_signalregion.split('/')[-1:]
    file_ttW_signalregion_keyname = file_ttW_signalregion_keyname[0].split('.')[:-1]
    file_ttZ_signalregion_keyname = input_path_ttZ_signalregion.split('/')[-1:]
    file_ttZ_signalregion_keyname = file_ttZ_signalregion_keyname[0].split('.')[:-1]
    file_ttWW_signalregion_keyname = input_path_ttWW_signalregion.split('/')[-1:]
    file_ttWW_signalregion_keyname = file_ttWW_signalregion_keyname[0].split('.')[:-1]
    file_EWK_signalregion_keyname = input_path_EWK_signalregion.split('/')[-1:]
    file_EWK_signalregion_keyname = file_EWK_signalregion_keyname[0].split('.')[:-1]
    file_data_signalregion_keyname = input_path_data_signalregion.split('/')[-1:]
    file_data_signalregion_keyname = file_data_signalregion_keyname[0].split('.')[:-1]

    for branch_index in xrange(len(branch_list)):
        branch_to_draw = []
        branch_to_draw.append(branch_list[branch_index])
        files_histname_dict = CPlotter.load_histos(files_, branch_to_draw,'syncTree','geq3j')

        files_histname_dict_SR = CPlotter.load_histos(files_SR_, branch_to_draw,'syncTree','geq3j')
        files_histname_dict_training = CPlotter.load_histos(files_training_, branch_to_draw,'syncTree','geq3j')

        # Finish building histogram names (check 'load_histograms' in plotting class).
        file_ttH_training_Jet_numLoose_key = file_ttH_training_keyname[0] + '_' + branch_list[branch_index] + '_loose_TrainingRegion'
        file_ttJ_training_Jet_numLoose_key = file_ttJ_training_keyname[0] + '_' + branch_list[branch_index] + '_loose_TrainingRegion'
        file_ttW_training_Jet_numLoose_key = file_ttW_training_keyname[0] + '_' + branch_list[branch_index] + '_loose_TrainingRegion'
        file_ttZ_training_Jet_numLoose_key = file_ttZ_training_keyname[0] + '_' + branch_list[branch_index] + '_loose_TrainingRegion'

        file_ttH_HWW_Jet_numLoose_key = file_ttH_HWW_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"
        file_ttH_HZZ_Jet_numLoose_key = file_ttH_HZZ_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"
        file_ttH_Htautau_Jet_numLoose_key = file_ttH_Htautau_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"
        file_ttH_Hmm_Jet_numLoose_key = file_ttH_Hmm_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"
        file_ttH_Hoth_Jet_numLoose_key = file_ttH_Hoth_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"
        file_Conv_Jet_numLoose_key = file_Conv_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"
        file_Fakes_Jet_numLoose_key = file_Fakes_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"
        file_Flips_Jet_numLoose_key = file_Flips_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"
        file_ttW_signalregion_Jet_numLoose_key = file_ttW_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"
        file_ttWW_signalregion_Jet_numLoose_key = file_ttWW_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"
        file_EWK_signalregion_Jet_numLoose_key = file_EWK_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"
        file_ttZ_signalregion_Jet_numLoose_key = file_ttZ_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"
        file_data_signalregion_Jet_numLoose_key = file_data_signalregion_keyname[0] + '_' + branch_list[branch_index] + "_SignalRegion"

        # Get loose training region hisograms
        ttH_training_region_hist = files_histname_dict.get(file_ttH_training_Jet_numLoose_key)
        ttJ_training_region_hist = files_histname_dict.get(file_ttJ_training_Jet_numLoose_key)
        ttW_training_region_hist = files_histname_dict.get(file_ttW_training_Jet_numLoose_key)
        ttZ_training_region_hist = files_histname_dict.get(file_ttZ_training_Jet_numLoose_key)
        #Get all signal region histograms that are associated with trainign region processes
        hist_ttH_HWW = files_histname_dict.get(file_ttH_HWW_Jet_numLoose_key)
        hist_ttH_HZZ = files_histname_dict.get(file_ttH_HZZ_Jet_numLoose_key)
        hist_ttH_Htautau = files_histname_dict.get(file_ttH_Htautau_Jet_numLoose_key)
        hist_ttH_Hmm = files_histname_dict.get(file_ttH_Hmm_Jet_numLoose_key)
        hist_ttH_Hoth = files_histname_dict.get(file_ttH_Hoth_Jet_numLoose_key)
        hist_fakes = files_histname_dict.get(file_Fakes_Jet_numLoose_key)
        hist_flips = files_histname_dict.get(file_Flips_Jet_numLoose_key)
        hist_convs = files_histname_dict.get(file_Conv_Jet_numLoose_key)
        hist_ttW_SR = files_histname_dict.get(file_ttW_signalregion_Jet_numLoose_key)
        hist_ttWW_SR = files_histname_dict.get(file_ttWW_signalregion_Jet_numLoose_key)
        hist_EWK_SR = files_histname_dict.get(file_EWK_signalregion_Jet_numLoose_key)
        hist_ttZ_SR = files_histname_dict.get(file_ttZ_signalregion_Jet_numLoose_key)
        hist_data_SR = files_histname_dict.get(file_data_signalregion_Jet_numLoose_key)

        combined_hist_MC_SR_title = branch_list[branch_index]+'_combined_MC'

        output_file_name = branch_list[branch_index] + '_DataMC.png'
        output_fullpath = os.path.join(output_dir, output_file_name)
        data_hist_name = 'Data_SigRegion_%s_SignalRegion' % (branch_list[branch_index])
        input_hist_data = files_histname_dict.get(data_hist_name)

        #stacked_hist_MC_SR = CPlotter.stack_hists(files_histname_dict, combined_hist_MC_SR_title, branch_list[branch_index], input_hist_data)

        SR_hists = []
        for name, hist in files_histname_dict_SR.iteritems():
            SR_hists.append(hist)
        summed_hist_MC_SR = CPlotter.sum_hists(SR_hists,'SRCombined')
        print 'summed_hist_MC_SR = ', summed_hist_MC_SR

        TR_hists = []
        for name, hist in files_histname_dict_training.iteritems():
            TR_hists.append(hist)
        summed_hist_MC_TR = CPlotter.sum_hists(TR_hists,'TRCombined')
        print 'summed_hist_MC_TR = ', summed_hist_MC_TR

        CPlotter.make_comparison(summed_hist_MC_TR, 'MCTR', summed_hist_MC_SR, 'MCSR', branch_list[branch_index], output_fullpath)

        print 'output in ', output_fullpath

    exit(0)

main()
