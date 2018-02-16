############################################
#              train_DNN.py
#         Joshuha Thomas-Wilsker
#           IHEP Beijing, CERN
############################################
# Python script using Keras with TensorFlow
# backend to train deep neural network for
# ttH multilepton dilepton analysis region.
############################################

USAGE:
$> python train_DNN.py

########################
# Introduction
########################
- Using pyMVA Keras interface with Tensorflow backend to design DNN model for ttH multilpeton dilepton analysis region.
- In this setup we can easily change the backend in case wewant to use e.g. Theano instead of TensorFlow.
- Import all Keras libraries along with TensorFlow backend into pyMVA so that we can easily produce .root files.
- Using objects from TMVA library to manage the data / book methods etc.
- .root files output with training histograms/ttrees.
- '.h5' file (stores multidimensional arrays of scientific data) stores model.
- pyKeras much faster and better performing (integral of ROC) than TMVA DNN especially when going to higher number of hidden layers.


########################
# Initial setup
########################
The fermilab keras workshop has a nice set of scripts
one can use to setup the keras environment. Check
out the package:
$> git clone https://github.com/stwunsch/fermilab_keras_workshop

and follow the commands here:
https://github.com/stwunsch/fermilab_keras_workshop

On lxplus we needed python 2.7 for initial setup.
Check which python versions are available:
$> scl -l | grep python

Enable the one you want:
$> scl enable python27 bash

Run the following command to install necessary packages with pip:
$> bash init_virtualenv.sh

########################
# New shell
########################
Every time you open a new shell you need to rerun the
commands beneath in the keras work area:

$> scl enable python27 bash
$> source /afs/cern.ch/work/j/jthomasw/private/IHEP/ttH_multilepton/DNN/fermilab_keras_workshop/py2_virtualenv/bin/activate

Because this script uses ROOT with pyRoot enabled we need an additional step to
so that the libraries are accessible in this environment:
$> source /cvmfs/sft.cern.ch/lcg/views/LCG_91/x86_64-slc6-gcc62-opt/setup.sh


########################
# TMVA GUI
########################
Can setup TMVA GUI to create plots from output files.
Need to setup the shell as described above. Then inside
a python environment run the following commands:

$> import ROOT
$> ROOT.TMVA.TMVAMultiClassGui('TMVAoutput.root')


#######################################
# DNN Model and Hyperparameter Tuning
#######################################
- The analysis performed is a 'multiclass' analysis.
- Three output nodes are used here.
- 'softmax' activation function used in final layer so that the outputs represent probabilities (output is normalised to 1).
- A consequence of the softmax function is that the probability of a class is not independent of the other class probabilities.
- Fine if we want to select a single label per sampling.
- In this case, for a given event, you get three probabilities, one for each output node.
- We assign the event to the label associated with the output node with the highest probability.


#Normalisation#
- One very important parameter here is 'NormMode'.
        - 'NormMode=EqualNumEvents' : Sets the average weight of signal events to 1 and the sum of the background weights is set equal to signal.
        - 'NormMode=NumEvents' : Average weight of 1 per event, signal and background renormalised independently.
- In the case of ttH multilepton, if one *doesn't* normalise background to the same as signal, the DNN will seperate out ttV seeing as the MC has many more events (DNN tunes to this).

#Number of Hidden layers#
- Increasing the number of hidden layers seems to make ttJets more background like, ttW more signal like and ttH remains in the middle (if perhaps more background like).
-

#Output Layers#
- Number of neurons in the output layer should be the same as the number of samples[processes] you want to run.
- When running in TMVA using Keras interface you should see something like:

*PrepareTrainingAndTestTree
                       : Dataset[MultiClass_DNN] : Class index : 0  name : sample=ttH
                       : Dataset[MultiClass_DNN] : Class index : 1  name : sample=ttV
                       : Dataset[MultiClass_DNN] : Class index : 2  name : sample=ttJets*

- As you can see here, the three classes (neurons) in the output layer are associated with one of the inputs.
-

########################
# DNN Training
########################

-
-

########################
# Possible Methods
########################
1. For each event we can calculate a probability it is of a certain hypothesis (comes from a certain process). This probability is its output score on a given node, where the node represents the process. The event is assigned to a given process according to the node with the highest probability.
2. Separate signal from background (only two classes) with a multiclass DNN method. Find the best working point on all nodes which maximises the signal efficiency and background rejection. Not sure we have the stats for this and/or can find a reasonable WP.