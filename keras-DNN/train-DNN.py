import matplotlib.pyplot as plt
import numpy as np
import pandas
import pandas as pd
import optparse, json, argparse, math
import ROOT
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import class_weight
from sklearn.metrics import log_loss
import os
from os import environ
os.environ['KERAS_BACKEND'] = 'tensorflow'
import keras
from keras import backend as K
from keras.utils import np_utils
from keras.utils import plot_model
from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.optimizers import Adam
from keras.optimizers import Adadelta
from keras.optimizers import Adagrad
from keras.layers import Dropout
from keras.models import load_model
from keras.wrappers.scikit_learn import KerasClassifier
from keras.callbacks import EarlyStopping
from plotting.plotter import plotter
from root_numpy import root2array, tree2array
seed = 7
np.random.seed(7)
rng = np.random.RandomState(31337)

def load_data(inputPath,variables,criteria):
    print variables
    my_cols_list=variables+['process', 'key', 'target', 'totalWeight']
    data = pd.DataFrame(columns=my_cols_list)
    keys=['ttH','ttJ','ttW','ttZ']

    for key in keys :
        print key
        if 'ttH' in key or 'TTH' in key:
            sampleName='ttH'
            #fileName = 'ttHnobb_NoJetNCut'
            fileName = 'ttHnobb_DiLepRegion'
        if 'ttJ' in key or 'TTJ' in key:
            sampleName='ttJ'
            #fileName='ttJets_NoJetNCut'
            fileName='ttJets_DiLepRegion'
        if 'ttW' in key or 'TTW' in key:
            sampleName='ttW'
            #fileName='ttWJets_NoJetNCut'
            fileName='ttWJets_DiLepRegion'
        if 'ttZ' in key or 'TTZ' in key:
            sampleName='ttZ'
            #fileName='ttZJets_NoJetNCut'
            fileName='ttZJets_DiLepRegion'
        if 'ttH' in key:
                target=0
        if 'ttJ' in key:
                target=1
        if 'ttW' in key:
                target=2
        if 'ttZ' in key:
                target=3

        inputTree = 'syncTree'
        try: tfile = ROOT.TFile(inputPath+"/"+fileName+".root")
        except :
            print " file "+ inputPath+"/"+fileName+".root deosn't exits "
            continue
        try: tree = tfile.Get(inputTree)
        except :
            print inputTree + " deosn't exists in " + inputPath+"/"+fileName+".root"
            continue
        if tree is not None :
            try: chunk_arr = tree2array(tree=tree, selection=criteria) #,  start=start, stop = stop)
            except : continue
            else :
                chunk_df = pd.DataFrame(chunk_arr, columns=variables)
                chunk_df['process']=sampleName
                chunk_df['key']=key
                chunk_df['target']=target
                chunk_df['totalWeight']=chunk_df["EventWeight"]
                data=data.append(chunk_df, ignore_index=True)
        tfile.Close()
        if len(data) == 0 : continue
        nttH = len(data.ix[(data.target.values == 0) & (data.key.values==key) ])
        nttJ = len(data.ix[(data.target.values == 1) & (data.key.values==key) ])
        nttW = len(data.ix[(data.target.values == 2) & (data.key.values==key) ])
        nttZ = len(data.ix[(data.target.values == 3) & (data.key.values==key) ])
        print 'key = ', key
        print "length of nttH = %i, nttJ = %i, nttW = %i, nttZ = %i, TotalWeights = %f" % (nttH, nttJ , nttW, nttZ, data.ix[(data.key.values==key)]["totalWeight"].sum())
        nNW = len(data.ix[(data["totalWeight"].values < 0) & (data.key.values==key) ])
        #print key, "events with -ve weights", nNW
    print (data.columns.values.tolist())
    n = len(data)
    nttH = len(data.ix[data.target.values == 0])
    nttJ = len(data.ix[data.target.values == 1])
    nttW = len(data.ix[data.target.values == 2])
    nttZ = len(data.ix[data.target.values == 3])
    print "Total length of nttH = %i, nttJ = %i, nttW = %i, nttZ = %i" % (nttH, nttJ , nttW, nttZ)
    return data

def load_trained_model(weights_path, num_variables, optimizer):
    model = baseline_model(num_variables, optimizer)
    model.load_weights(weights_path)
    return model

def normalise(x_train, x_test):
    mu = np.mean(x_train, axis=0)
    std = np.std(x_train, axis=0)
    x_train_normalised = (x_train - mu) / std
    x_test_normalised = (x_test - mu) / std
    return x_train_normalised, x_test_normalised

def create_model(num_variables=26, optimizer='Adam', init='glorot_normal'):
    model = Sequential()
    # input_dim = number of variables
    num_variables = 18
    model.add(Dense(32,input_dim=num_variables,kernel_initializer=init,activation='relu'))
    for index in xrange(5):
        model.add(Dense(16,activation='relu'))
    for index in xrange(5):
        model.add(Dense(16,activation='relu'))
    for index in xrange(5):
        model.add(Dense(8,activation='relu'))
    model.add(Dense(4, activation='softmax'))
    model.compile(loss='categorical_crossentropy',optimizer=optimizer,metrics=['acc'])
    return model

def baseline_model(num_variables,optimizer):
    model = Sequential()
    # input_dim = number of variables
    model.add(Dense(32,input_dim=num_variables,kernel_initializer='glorot_normal',activation='relu'))
    #model.add(Dense(64,input_dim=num_variables,kernel_initializer='glorot_normal',activation='relu'))
    for index in xrange(5):
        model.add(Dense(16,activation='relu'))
        #model.add(Dense(32,activation='relu'))
    for index in xrange(5):
        model.add(Dense(16,activation='relu'))
        #model.add(Dense(32,activation='relu'))
    for index in xrange(5):
        model.add(Dense(8,activation='relu'))
        #model.add(Dense(32,activation='relu'))
    model.add(Dense(4, activation='softmax'))
    model.compile(loss='categorical_crossentropy',optimizer=optimizer,metrics=['acc'])

    return model

def check_dir(dir):
    if not os.path.exists(dir):
        print 'mkdir: ', dir
        os.makedirs(dir)

# Ratio always > 1. mu use in natural log multiplied into ratio. Keep mu above 1 to avoid class weights going negative.
def create_class_weight(labels_dict,mu=0.9):
    total = np.sum(labels_dict.values()) # total number of examples in all datasets
    keys = labels_dict.keys() # labels
    class_weight = dict()
    print 'total: ', total

    for key in keys:
        # logarithm smooths the weights for very imbalanced classes.
        score = math.log(mu*total/float(labels_dict[key])) # natlog(parameter * total number of examples / number of examples for given label)
        #score = float(total/labels_dict[key])
        print 'score = ', score
        if score > 0.:
            class_weight[key] = score
        else :
            class_weight[key] = 1.
    return class_weight

def main():
    print 'Using Keras version: ', keras.__version__

    usage = 'usage: %prog [options]'
    parser = argparse.ArgumentParser(usage)
    parser.add_argument('-t', '--train_model', dest='train_model', help='Option to train model or simply make diagnostic plots (0=False, 1=True)', default=0, type=int)
    parser.add_argument('-r', '--region', dest='region', help='Option to choose SigRegion or CtrlRegion', default='SigRegion', type=str)
    parser.add_argument('-w', '--classweights', dest='classweights', help='Option to choose class weights (InverseNEventsTR, InverseSRYields or BalancedWeights)', default='InverseNEventsTR', type=str)
    parser.add_argument('-s', '--sel', dest='selection', help='Option to choose selection', default='geq4j', type=str)
    args = parser.parse_args()
    do_model_fit = args.train_model
    region = args.region
    classweights_name = args.classweights
    selection = args.selection
    number_of_classes = 4

    # Create instance of output directory where all results are saved.

    output_directory = '2019-07-03_DNN_newfiles_%s_%s_%s/' % (selection,classweights_name,region)

    check_dir(output_directory)

    # Create plots subdirectory
    plots_dir = os.path.join(output_directory,'plots/')

    input_var_jsonFile = open('input_vars_SigRegion.json','r')
    #input_var_jsonFile = open('LOWLEVEL_invars_conv1DNN.json','r')
    #input_var_jsonFile = open('HIGHLEVEL_invars_conv1DNN.json','r')

    if selection == 'geq4j':
        selection_criteria = 'n_presel_jet>=4'
    if selection == 'geq3j':
        selection_criteria = 'n_presel_jet>=3'
    if selection == 'eeq3j':
        selection_criteria = 'n_presel_jet==3'
    if selection == 'fullSRsel':
        selection_criteria = 'n_presel_jet>=4 && passTrigCut==1 && passMassllCut==1 && passTauNCut==1 && passZvetoCut==1 && passMetLDCut==1 && passTightChargeCut==1 && passLepTightNCut==1 && passGenMatchCut==1'

    variable_list = json.load(input_var_jsonFile,encoding="utf-8").items()
    column_headers = []
    for key,var in variable_list:
        if 'hadTop_BDT' in key:
            key = 'hadTop_BDT'
        if 'Hj1_BDT' in key:
            key = 'Hj1_BDT'
        if 'Hj_tagger_hadTop' in key:
            key = 'Hj_tagger_hadTop'
        column_headers.append(key)
    column_headers.append('EventWeight')
    column_headers.append('xsec_rwgt')

    # Create instance of the input files directory
    inputs_file_path = '/afs/cern.ch/work/j/jthomasw/private/IHEP/ttHML/github/ttH_multilepton/keras-DNN/samples/TrainMVA_looseWithTH_20190628/'

    print 'Getting files from:', inputs_file_path
    outputdataframe_name = '%s/output_dataframe_%s_%s.csv' %(output_directory,region,selection) #"output_dataframe_NJetgeq4.csv"

    if os.path.isfile(outputdataframe_name):
        data = pandas.read_csv(outputdataframe_name)
        print 'Loading %s . . . . ' % (outputdataframe_name)
    else:
        print 'Creating and loading new data file in %s . . . . ' % (inputs_file_path)
        data = load_data(inputs_file_path,column_headers,selection_criteria)
        data.to_csv(outputdataframe_name, index=False)
        data = pandas.read_csv(outputdataframe_name)

    Plotter = plotter()

    #iloc 'totalWeight' column for rows with key value 'ttH' and sum
    ttH_sumweights = data.iloc[(data.key.values=='ttH')]["totalWeight"].sum()
    ttJ_sumweights = data.iloc[(data.key.values=='ttJ')]["totalWeight"].sum()
    ttW_sumweights = data.iloc[(data.key.values=='ttW')]["totalWeight"].sum()
    ttZ_sumweights = data.iloc[(data.key.values=='ttZ')]["totalWeight"].sum()
    print 'ttH_sumweights: %s , ttJ_sumweights: %s , ttW_sumweights: %s, ttZ_sumweights: %s ' % (ttH_sumweights,ttJ_sumweights,ttW_sumweights,ttZ_sumweights)

    traindataset, valdataset = train_test_split(data, test_size=0.2)

    print 'train dataset shape: ', traindataset.shape
    print 'validation dataset shape: ', valdataset.shape
    train_df = data.iloc[:traindataset.shape[0]]
    train_df.drop(['EventWeight'], axis=1, inplace=True)
    train_df.drop(['xsec_rwgt'], axis=1, inplace=True)

    train_weights = traindataset['EventWeight'].values * traindataset['xsec_rwgt'].values
    test_weights = valdataset['EventWeight'].values * valdataset['xsec_rwgt'].values
    if region == 'CtrlRegion':
        training_columns = column_headers[:-3]
    else:
        training_columns = column_headers[:-2]
    print 'Use columns = ', training_columns
    X_train = traindataset[training_columns].values
    Y_train = traindataset.target.astype(int)
    X_test = valdataset[training_columns].values
    Y_test = valdataset.target.astype(int)

    num_variables = len(training_columns)

    ## Input Variable Correlations
    correlation_plot_file_name = 'correlation_plot.png'
    Plotter.correlation_matrix(train_df)
    Plotter.save_plots(dir=plots_dir, filename=correlation_plot_file_name)

    # =============== Weights ==================
    # WARNING! 'sample_weight' will overide 'class_weight'
    # ==========================================
    # Sample                    |       ttH       |      tt+jets       |       ttW        |       ttZ        |
    ############################
    #  ======= geq 4 Jets ======
    ############################
    # Loose lepton TR selection
    ############################
    # XS                              0.2118              831.                0.2043            0.2529
    # # events in TR            |     221554      |      1168897       |      321674      |      204998      |
    # Sum of weights:           |    94.379784    |   7372.112793      |    206.978439    |    122.834419    |
    # Yields 2LSS SR HIG 18-019 |      60.08      | 140.25+22.79+17.25 |      151.03      |      87.05       |
    #                                                    =180.29
    ############################
    #= Control Region (== 3 Jets)
    ############################
    # Loose lepton TR selection
    ############################
    # # events in TR            |    39418        |      568724        |      111809      |      58507       |
    # Sum of weights            |   24.269867     |    3807.655762     |    102.885391    |     58.825554    |
    # Yields 2LSS ttWctrl       |    14.36        |    120.54 + 9.55   |       75.97      |      38.64       |
    #   AN2018-098-v18

    # Yields 2LSS SR HIG 18-019 |       60.08        | 140.25+22.79+17.25 |       151.03       |      87.05       |
    # Yields 2LSS ttWctrl       |       14.36        |    120.54 + 9.55   |        75.97       |      38.64       |
    # Yields 2LSS >= 3 jets     |       74.44        |        310.38      |       227.00       |     125.69       |
    #balancedweights = class_weight.compute_class_weight('balanced', np.unique([0,1,2,3]), Y_train)

    if region == 'SigRegion':
        if classweights_name == 'InverseSRYields':
            if selection == 'geq4j':
                tuned_weighted = {0 : 0.0166445, 1 : 0.00554662, 2 : 0.00662120, 3 : 0.0114877}
            if selection == 'geq3j':
                tuned_weighted = {0 : 0.01343363782, 1 : 0.00322185707, 2 : 0.00440528634, 3 : 0.00795608242}
        elif classweights_name == 'InverseNEventsTR':
            tuned_weighted = {0 : 0.00000451357, 1 : 0.000000855507, 2 : 0.00000310874, 3 : 0.00000487810}
        elif classweights_name == 'BalancedWeights':
            tuned_weighted = balancedweights
        elif classweights_name == 'InverseSumWeightsTR':
            tuned_weighted = {0 : 0.01059548939, 1 : 0.00013564632, 2 : 0.00483142111, 3 : 0.00814104066}
        elif classweights_name == 'noWeights':
            tuned_weighted = {0 : 1.0, 1 : 1.0, 2 : 1.0, 3 : 1.0}
    elif region == 'CtrlRegion':
        if classweights_name == 'InverseSRYields':
            tuned_weighted = { 0 : 0.069637883, 1 : 0.00768698593, 2 : 0.01316309069, 3 : 0.02587991718}
        elif classweights_name == 'InverseNEventsTR':
            tuned_weighted = {0 : 0.00002536912, 1 : 0.00000175832, 2 : 0.00000894382, 3 : 0.00001709197}
        elif classweights_name == 'BalancedWeights':
            tuned_weighted = balancedweights
        elif classweights_name == 'InverseSumWeightsTR':
            tuned_weighted = {0 : 0.04120335723, 1 : 0.00026262878, 2 : 0.00971955289, 3 : 0.01699941491}
        elif classweights_name == 'noWeights':
            tuned_weighted = {0 : 1.0, 1 : 1.0, 2 : 1.0, 3 : 1.0}


    print 'class weights : ', classweights_name
    print 'weights = ', tuned_weighted

    # Fit label encoder to Y_train
    newencoder = LabelEncoder()
    newencoder.fit(Y_train)
    # Transform to encoded array
    encoded_Y = newencoder.transform(Y_train)
    encoded_Y_test = newencoder.transform(Y_test)
    # Transform to one hot encoded arrays
    Y_train = np_utils.to_categorical(encoded_Y)
    Y_test = np_utils.to_categorical(encoded_Y_test)

    print 'num_variables = ',num_variables
    optimizer = 'Adam'
    if do_model_fit == 1:
        print 'Training new model. . . . '
        histories = []
        labels = []
        early_stopping_monitor = EarlyStopping(patience=50,monitor='val_loss',verbose=1)

        optimizers = ['Adamax','Adam','Nadam']
        #epochs = np.array([10,20,30])
        batchessize = np.array([100,200,500,1000])
        #init = ['glorot_normal','uniform','normal','glorot_uniform']
        #learning_rates = [0.0001,0.001,0.01,0.1]

        #param_grid = dict(optimizer=optimizers, nb_epoch=epochs, batch_size=batchessize)
        '''param_grid = dict(batch_size=batchessize)
        model = KerasClassifier(build_fn=create_model,epochs=10,batch_size=50)
        grid = GridSearchCV(estimator=model,param_grid=param_grid,n_jobs=-1)
        grid_result = grid.fit(X_train,Y_train)
        print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
        means = grid_result.cv_results_['mean_test_score']
        stds = grid_result.cv_results_['std_test_score']
        params = grid_result.cv_results_['params']
        for mean, stdev, param in zip(means, stds, params):
            print("%f (%f) with: %r" % (mean, stdev, param))'''

        '''model1 = baseline_model(num_variables)
        model1.compile(loss='categorical_crossentropy',
                       optimizer=Adam(lr=0.01),
                       metrics=['accuracy'])
        history1 = model1.fit(X_train,Y_train,validation_split=0.010,epochs=10,batch_size=5,verbose=1)
        histories.append(history1)
        labels.append('Adam')'''


        '''model2 = baseline_model(num_variables)
        model2.compile(loss='categorical_crossentropy',
                       optimizer=Adagrad(lr=0.01),
                       metrics=['accuracy'])
        history2 = model2.fit(X_train,Y_train,validation_split=0.010,epochs=10,batch_size=5,verbose=1)
        histories.append(history2)
        labels.append('Adagrad')'''

        model3 = baseline_model(num_variables,optimizer)

        #Batch size = number of examples before updating weights (larger = faster training)
        history3 = model3.fit(X_train,Y_train,validation_split=0.2,epochs=200,batch_size=1000,verbose=1,shuffle=True,class_weight=tuned_weighted,callbacks=[early_stopping_monitor])
        histories.append(history3)
        labels.append(optimizer)
        Plotter.plot_training_progress_acc(histories, labels)
        acc_progress_filename = 'DNN_acc_wrt_epoch.png'

        Plotter.save_plots(dir=plots_dir, filename=acc_progress_filename)

        # Which model do you want the rest of the plots for?
        model = model3
    else:
        # Which model do you want to load?
        model_name = os.path.join(output_directory,'model.h5')
        print 'Loading  %s' % (model_name)
        model = load_trained_model(model_name, num_variables, optimizer)

    # Node probabilities for training sample events

    result_probs = model.predict(np.array(X_train))
    result_classes = model.predict_classes(np.array(X_train))

    result_probs_test = model.predict(np.array(X_test))
    result_classes_test = model.predict_classes(np.array(X_test))

    # Store model in file
    model_output_name = os.path.join(output_directory,'model.h5')
    model.save(model_output_name)
    weights_output_name = os.path.join(output_directory,'model_weights.h5')
    model.save_weights(weights_output_name)

    model_json = model.to_json()
    model_json_name = os.path.join(output_directory,'model_serialised.json')
    with open(model_json_name,'w') as json_file:
        json_file.write(model_json)

    model.summary()
    model_schematic_name = os.path.join(output_directory,'model_schematic.png')
    #plot_model(model, to_file=model_schematic_name, show_shapes=True, show_layer_names=True)

    # Initialise output directory where plotter results will be saved.
    Plotter.output_directory = output_directory

    #Plotter.overfitting(model, Y_train, Y_test, result_probs, result_probs_test, plots_dir, train_weights, test_weights)

    original_encoded_test_Y = []
    for i in xrange(len(result_probs_test)):
        if Y_test[i][0] == 1:
            original_encoded_test_Y.append(0)
        if Y_test[i][1] == 1:
            original_encoded_test_Y.append(1)
        if Y_test[i][2] == 1:
            original_encoded_test_Y.append(2)
        if Y_test[i][3] == 1:
            original_encoded_test_Y.append(3)

    original_encoded_train_Y = []
    for i in xrange(len(result_probs)):
        if Y_train[i][0] == 1:
            original_encoded_train_Y.append(0)
        if Y_train[i][1] == 1:
            original_encoded_train_Y.append(1)
        if Y_train[i][2] == 1:
            original_encoded_train_Y.append(2)
        if Y_train[i][3] == 1:
            original_encoded_train_Y.append(3)

    result_classes_test = newencoder.inverse_transform(result_classes_test)
    result_classes_train = newencoder.inverse_transform(result_classes)

    Plotter.plots_directory = plots_dir

    # Create confusion matrices for training and testing performance
    #Plotter.conf_matrix(original_encoded_train_Y,result_classes_train,train_weights,'index')
    #Plotter.save_plots(dir=plots_dir, filename='yields_norm_confusion_matrix_TRAIN.png')
    #Plotter.conf_matrix(original_encoded_test_Y,result_classes_test,test_weights,'index')
    #Plotter.save_plots(dir=plots_dir, filename='yields_norm_confusion_matrix_TEST.png')

    #Plotter.ROC_sklearn(original_encoded_train_Y, result_probs, original_encoded_test_Y, result_probs_test, 0 , 'ttHnode')
    #Plotter.ROC_sklearn(original_encoded_train_Y, result_probs, original_encoded_test_Y, result_probs_test, 1 , 'ttJnode')
    #Plotter.ROC_sklearn(original_encoded_train_Y, result_probs, original_encoded_test_Y, result_probs_test, 2 , 'ttWnode')
    #Plotter.ROC_sklearn(original_encoded_train_Y, result_probs, original_encoded_test_Y, result_probs_test, 3 , 'ttZnode')

    #Plotter.separation_table(Plotter.output_directory)

main()
