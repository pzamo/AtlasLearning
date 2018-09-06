import ROOT as rt
from array import array
import numpy as np
import sys
sys.path.append('/pbs/home/p/pzamolod/private/DB_management')
from TreeProcessingFunctions import *



# sur jetpt: [20,30] / [30,40] / [40,50] / [50,80]
# sur jetDetectorEta: [2.5,3.2] / [3.2,4.5]
# sur mu: [0,50] / [50,inf]


def TreeProcessing(in_path, in_treeName, out_path, out_treeName, MAX_CLUSTERS = 70, masking_length = 10):
    #########################################################################################################
    ################################## DEFINING THE TREE ####################################################
    #########################################################################################################
    inputFile = rt.TFile(in_path)
    inputTree = inputFile.Get(in_treeName)

    outputFile = rt.TFile(out_path, 'recreate')
    outputTree_p20_eta_25 = rt.TTree(out_treeName+'_p20_eta_25', 'PreprocTree_p20_eta_25')
    outputTree_p30_eta_25 = rt.TTree(out_treeName+'_p30_eta_25', 'PreprocTree_p30_eta_25')
    outputTree_p40_eta_25 = rt.TTree(out_treeName+'_p40_eta_25', 'PreprocTree_p40_eta_25')
    outputTree_p50_eta_25 = rt.TTree(out_treeName+'_p50_eta_25', 'PreprocTree_p50_eta_25')
    outputTree_p20_eta_32 = rt.TTree(out_treeName+'_p20_eta_32', 'PreprocTree_p20_eta_32')
    outputTree_p30_eta_32 = rt.TTree(out_treeName+'_p30_eta_32', 'PreprocTree_p30_eta_32')
    outputTree_p40_eta_32 = rt.TTree(out_treeName+'_p40_eta_32', 'PreprocTree_p40_eta_32')
    outputTree_p50_eta_32 = rt.TTree(out_treeName+'_p50_eta_32', 'PreprocTree_p50_eta_32')
    FullOutputTree = rt.TTree(out_treeName, 'PreprocTree')
    treeList = [outputTree_p20_eta_25,
        outputTree_p30_eta_25,
        outputTree_p40_eta_25,
        outputTree_p50_eta_25,
        outputTree_p20_eta_32,
        outputTree_p30_eta_32,
        outputTree_p40_eta_32,
        outputTree_p50_eta_32,
        FullOutputTree]

    #########################################################################################################
    ################################## DEFINING THE VARIABLES ###############################################
    #########################################################################################################
    weight = array('f', [0])
    jetpt = array('f', [0])
    jetfjvt = array('f', [0])
    jettiming = array('f', [0])
    jettype = array('f', [0])
    jettruth = array('f', [0])
    jetDetectorEta = array('f', [0])
    jetDetectorPhi = array('f', [0])
    jetNegativeE = array('f', [0])
    jetN90Constituents = array('f', [0])
    o1eta_out = array('f', [0])
    o1phi_out = array('f', [0])
    o2eta_out = array('f', [0])
    o2phi_out = array('f', [0])
    o3eta_out = array('f', [0])
    o3phi_out = array('f', [0])
    o4eta_out = array('f', [0])
    o4phi_out = array('f', [0])
    eventsize_out = array('f', [0])
    masking_length_out = array('i', [0])

    nclusters = array('i', [0])
    clpt_out = array('f', MAX_CLUSTERS*[0])
    cllcpt_out = array('f', MAX_CLUSTERS*[0])
    cleta_out = array('f', MAX_CLUSTERS*[0])
    clphi_out = array('f', MAX_CLUSTERS*[0])
    cltime_out = array('f', MAX_CLUSTERS*[0])
    cle_out = array('f', MAX_CLUSTERS*[0])
    cle_samplFCAL0_out = array('f', MAX_CLUSTERS*[0])
    cle_samplFCAL1_out = array('f', MAX_CLUSTERS*[0])
    cle_samplFCAL2_out = array('f', MAX_CLUSTERS*[0])
    cle_samplEME1_out = array('f', MAX_CLUSTERS*[0])
    cle_samplEME2_out = array('f', MAX_CLUSTERS*[0])
    cle_samplEME3_out = array('f', MAX_CLUSTERS*[0])
    cle_samplHEC0_out = array('f', MAX_CLUSTERS*[0])
    cle_samplHEC1_out = array('f', MAX_CLUSTERS*[0])
    cle_samplHEC2_out = array('f', MAX_CLUSTERS*[0])
    cle_samplHEC3_out = array('f', MAX_CLUSTERS*[0])
    cle_samplEMall_out = array('f', MAX_CLUSTERS*[0])
    cle_samplHall_out = array('f', MAX_CLUSTERS*[0])
    clrawE_out = array('f', MAX_CLUSTERS*[0])
    clcalE_out = array('f', MAX_CLUSTERS*[0])
    permutation_out = array('i', MAX_CLUSTERS*[0])


    mask10deta_out = array('f', masking_length*[0])
    mask10dphi_out = array('f', masking_length*[0])
    mask10cle_out = array('f', masking_length*[0])
    mask10cltime_out = array('f', masking_length*[0])

    maskp10deta_out = array('f', masking_length*[0])
    maskp10dphi_out = array('f', masking_length*[0])
    maskp10cltime_out = array('f', masking_length*[0])


    Ndeta_out = array('f', MAX_CLUSTERS*[0])
    Ndphi_out = array('f', MAX_CLUSTERS*[0])
    Ncle_out = array('f', MAX_CLUSTERS*[0])
    Ncltime_out = array('f', MAX_CLUSTERS*[0])
    clintime_out = array('f', MAX_CLUSTERS*[0])
    pondEta_out = array('f', MAX_CLUSTERS*[0])
    pondPhi_out = array('f', MAX_CLUSTERS*[0])
    pondTime_out = array('f', MAX_CLUSTERS*[0])

    #########################################################################################################
    ################################## BRANCH DEFINITION ####################################################
    #########################################################################################################
    for outputTree in treeList:
        outputTree.Branch("weight", weight, "weight/F")
        outputTree.Branch("jetpt", jetpt, "jetpt/F")
        outputTree.Branch("jetfjvt", jetfjvt, "jetfjvt/F")
        outputTree.Branch("nclusters", nclusters, "nclusters/I")
        outputTree.Branch("jettype", jettype, "jettype/F")
        outputTree.Branch("jettruth", jettruth, "jettruth/F")
        outputTree.Branch("jetDetectorEta", jetDetectorEta, "jetDetectorEta/F")
        outputTree.Branch("jetDetectorPhi", jetDetectorPhi, "jetDetectorEta/F")
        outputTree.Branch("jetNegativeE", jetNegativeE, "jetDetectorPhi/F")
        outputTree.Branch("jetN90Constituents", jetN90Constituents, "jetN90Constituents/F")
        outputTree.Branch("o1eta", o1eta_out,"o1eta/F")
        outputTree.Branch("o1phi", o1phi_out,"o1phi/F")
        outputTree.Branch("o2eta", o2eta_out,"o2eta/F")
        outputTree.Branch("o2phi", o2phi_out,"o2phi/F")
        outputTree.Branch("o3eta", o3eta_out,"o3eta/F")
        outputTree.Branch("o3phi", o3phi_out,"o3phi/F")
        outputTree.Branch("o4eta", o4eta_out,"o4eta/F")
        outputTree.Branch("o4phi", o4phi_out,"o4phi/F")
        outputTree.Branch("eventsize", eventsize_out, "eventsize/I")
        outputTree.Branch("masking_length", masking_length_out, "masking_length/I")







        # CLUSTER VARIABLES BRANCH DEFINITION #


        outputTree.Branch("clpt", clpt_out, "clpt[nclusters]/F")
        outputTree.Branch("cllcpt", cllcpt_out, "cllcpt[nclusters]/F")
        outputTree.Branch("cleta", cleta_out,"cleta[nclusters]/F")
        outputTree.Branch("clphi", clphi_out, "clphi[nclusters]/F")
        outputTree.Branch("cltime", cltime_out, "cltime[nclusters]/F")
        outputTree.Branch("cle", cle_out, "cle[nclusters]/F")
        outputTree.Branch("cle_samplFCAL0", cle_samplFCAL0_out, "cle_samplFCAL0[nclusters]/F")
        outputTree.Branch("cle_samplFCAL1", cle_samplFCAL1_out, "cle_samplFCAL1[nclusters]/F")
        outputTree.Branch("cle_samplFCAL2", cle_samplFCAL2_out, "cle_samplFCAL2[nclusters]/F")
        outputTree.Branch("cle_samplEME1", cle_samplEME1_out, "cle_samplEME1[nclusters]/F")
        outputTree.Branch("cle_samplEME2", cle_samplEME2_out, "cle_samplEME2[nclusters]/F")
        outputTree.Branch("cle_samplEME3", cle_samplEME3_out, "cle_samplEME3[nclusters]/F")
        outputTree.Branch("cle_samplHEC0", cle_samplHEC0_out, "cle_samplHEC0[nclusters]/F")
        outputTree.Branch("cle_samplHEC1", cle_samplHEC1_out, "cle_samplHEC1[nclusters]/F")
        outputTree.Branch("cle_samplHEC2", cle_samplHEC2_out, "cle_samplHEC2[nclusters]/F")
        outputTree.Branch("cle_samplHEC3", cle_samplHEC3_out, "cle_samplHEC3[nclusters]/F")
        outputTree.Branch("cle_samplEMall", cle_samplEMall_out, "cle_samplEMall[nclusters]/F")
        outputTree.Branch("cle_samplHall", cle_samplHall_out, "cle_samplHall[nclusters]/F")
        outputTree.Branch("clrawE", clrawE_out, "clrawE[nclusters]/F")
        outputTree.Branch("clcalE", clcalE_out, "clcalE[nclusters]/F")
        outputTree.Branch("permutation", permutation_out, "permutation[nclusters]/I")


        outputTree.Branch("mask10deta", mask10deta_out, "mask10deta[masking_length]/F")
        outputTree.Branch("mask10dphi", mask10dphi_out, "mask10dphi[masking_length]/F")
        outputTree.Branch("mask10cle", mask10cle_out, "mask10cle[masking_length]/F")
        outputTree.Branch("mask10cltime", mask10cltime_out, "maskp10cltime[masking_length]/F")

        outputTree.Branch("maskp10deta", maskp10deta_out, "maskp10deta[masking_length]/F")
        outputTree.Branch("maskp10dphi", maskp10dphi_out, "maskp10dphi[masking_length]/F")
        outputTree.Branch("maskp10cltime", maskp10cltime_out, "maskp10cltime[masking_length]/F")


        outputTree.Branch("Ndeta", Ndeta_out, "Ndeta[nclusters]/F")
        outputTree.Branch("Ndphi", Ndphi_out, "Ndphi[nclusters]/F")
        outputTree.Branch("Ncle", Ncle_out, "Ncle[nclusters]/F")
        outputTree.Branch("Ncltime", Ncltime_out, "Ncltime[nclusters]/F")
        outputTree.Branch("clintime", clintime_out, "clintime[nclusters]/F")
        outputTree.Branch("pondEta", pondEta_out, "pondEta[nclusters]/F")
        outputTree.Branch("pondPhi", pondPhi_out, "pondPhi[nclusters]/F")
        outputTree.Branch("pondTime", pondTime_out, "pondTime[nclusters]/F")
    iszero = True
    isdata = True

    #########################################################################################################
    ################################## LOOP ON EVENTS #######################################################
    #########################################################################################################
    entries = inputTree.GetEntries()
    sys.stdout.write("[%s]" % (" " * 40))
    sys.stdout.flush()
    sys.stdout.write("\b" * (40+1))
    step = entries//40
    for event in xrange(entries):
        inputTree.GetEntry(event)
        if not event%step:
            sys.stdout.write("-")
            sys.stdout.flush()

        if iszero:
            sumweights = 15987000
        if isdata:
            data_lum = 44307.4
            weight = data_lum * inputTree.weight * inputTree.xweight * inputTree.muscale * inputTree.prw / sumweights
        masking_length_out[0] = masking_length
        eventsize = len(inputTree.jettype)
        eventsize_out[0] = eventsize

    #########################################################################################################
    #################################### LOOP ON JET ########################################################
    #########################################################################################################
        for jet in xrange(eventsize):
            if np.abs(inputTree.jetDetectorEta[jet])>2.5 and inputTree.jetpt[jet] > 20 and inputTree.jetpt[jet] <80:

                jetpt[0] = inputTree.jetpt[jet]
                jetfjvt[0] = inputTree.jetfjvt[jet]
                jettiming[0] = inputTree.jettiming[jet]
                jettype[0] = inputTree.jettype[jet]
                jettruth[0] = inputTree.jettruth[jet]
                jetDetectorEta[0] = inputTree.jetDetectorEta[jet]
                jetDetectorPhi[0] = inputTree.jetDetectorPhi[jet]
                jetNegativeE[0] = inputTree.jetNegativeE[jet]
                jetN90Constituents[0] = inputTree.jetN90Constituents[jet]
                nclusters[0] = len(inputTree.clpt[jet])


                cle = list(inputTree.cle[jet])
                cleta = list(inputTree.cleta[jet])
                clphi = list(inputTree.clphi[jet])
                cltime = list(inputTree.cltime[jet])
                permutation = permutation_finder(cle)
                cle = permutation_applier(cle, permutation)
                cleta = permutation_applier(cleta, permutation)
                clphi = permutation_applier(clphi, permutation)
                cltime = permutation_applier(cltime, permutation)
                clintime = intime(cltime, 30)

                Ndeta = delta_applier(cleta, jetDetectorEta[0]);
                Ndphi = delta_applier(clphi, jetDetectorPhi[0]);
                Ncltime = normalize_to_gauss(cltime, -37.0, 31.0);
                Ncle = normalize_to_max(cle);
                pondEta = ponderation_applier(Ndeta, Ncle);
                pondPhi = ponderation_applier(Ndphi, Ncle);
                pondTime = ponderation_applier(Ncltime, Ncle);
                o1eta = mean(pondEta)
                o1phi = mean(pondPhi)
                o2eta = moment(pondEta, o1eta, 2)
                o2phi = moment(pondPhi, o1phi, 2)
                o3eta = moment(pondEta, o1eta, 3)
                o3phi = moment(pondPhi, o1phi, 3)
                o4eta = moment(pondEta, o1eta, 4)
                o4phi = moment(pondPhi, o1phi, 4)
                mask10deta = mask_applier(Ndeta, masking_length, -50)
                mask10dphi = mask_applier(Ndphi, masking_length, -50)
                mask10cle = mask_applier(Ncle, masking_length, -50)
                mask10cltime = mask_applier(Ncltime, masking_length, -50)
                maskp10deta = mask_applier(pondEta, masking_length, -50)
                maskp10dphi = mask_applier(pondPhi, masking_length, -50)
                maskp10cltime = mask_applier(pondTime, masking_length, -50)


                o1eta_out[0] = o1eta
                o1phi_out[0] = o1phi
                o2eta_out[0] = o2eta
                o2phi_out[0] = o2phi
                o3eta_out[0] = o3eta
                o3phi_out[0] = o3phi
                o4eta_out[0] = o4eta
                o4phi_out[0] = o4phi



    #########################################################################################################
    ################################## FILLING CLUSTER ARRAYS ###############################################
    #########################################################################################################
                for j in range(nclusters[0]):
                    clpt_out[j] = inputTree.clpt[jet][j]
                    cllcpt_out[j] = inputTree.cllcpt[jet][j]
                    cleta_out[j] = inputTree.cleta[jet][j]
                    clphi_out[j] = inputTree.clphi[jet][j]
                    cltime_out[j] = inputTree.cltime[jet][j]
                    cle_out[j] = inputTree.cle[jet][j]
                    cle_samplFCAL0_out[j] = inputTree.cle_samplFCAL0[jet][j]
                    cle_samplFCAL1_out[j] = inputTree.cle_samplFCAL1[jet][j]
                    cle_samplFCAL2_out[j] = inputTree.cle_samplFCAL2[jet][j]
                    cle_samplEME1_out[j] = inputTree.cle_samplEME1[jet][j]
                    cle_samplEME2_out[j] = inputTree.cle_samplEME2[jet][j]
                    cle_samplEME3_out[j] = inputTree.cle_samplEME3[jet][j]
                    cle_samplHEC0_out[j] = inputTree.cle_samplHEC0[jet][j]
                    cle_samplHEC1_out[j] = inputTree.cle_samplHEC1[jet][j]
                    cle_samplHEC2_out[j] = inputTree.cle_samplHEC2[jet][j]
                    cle_samplHEC3_out[j] = inputTree.cle_samplHEC3[jet][j]
                    cle_samplEMall_out[j] = inputTree.cle_samplEMall[jet][j]
                    cle_samplHall_out[j] = inputTree.cle_samplHall[jet][j]
                    clrawE_out[j] = inputTree.clrawE[jet][j]
                    clcalE_out[j] = inputTree.clcalE[jet][j]

                    permutation_out[j] = permutation[j]
                    cle_out[j] = cle[j]
                    cleta_out[j] = cleta[j]
                    clphi_out[j] = clphi[j]
                    cltime_out[j] = cltime[j]
                    clintime_out[j] = clintime[j]
                    Ndeta_out[j] = Ndeta[j]
                    Ndphi_out[j] = Ndphi[j]
                    Ncltime_out[j] = Ncltime[j]
                    Ncle_out[j] = Ncle[j]
                    pondEta_out[j] = pondEta[j]
                    pondPhi_out[j] = pondPhi[j]
                    pondTime_out[j] = pondTime[j]
                for j in xrange(masking_length):
                    mask10deta_out[j] = mask10deta[j]
                    mask10dphi_out[j] = mask10dphi[j]
                    mask10cle_out[j] = mask10cle[j]
                    mask10cltime_out[j] = mask10cltime[j]
                    maskp10deta_out[j] = maskp10deta[j]
                    maskp10dphi_out[j] = maskp10dphi[j]
                    maskp10cltime_out[j] = maskp10cltime[j]
# sur jetpt: [20,30] / [30,40] / [40,50] / [50,80]
# sur jetDetectorEta: [2.5,3.2] / [3.2,4.5]
# sur mu: [0,50] / [50,inf]
                if inputTree.jetpt[jet]<30 and np.abs(inputTree.jetDetectorEta[jet])<3.2:
                    outputTree_p20_eta_25.Fill()
                if inputTree.jetpt[jet]>30 and inputTree.jetpt[jet]<40 and np.abs(inputTree.jetDetectorEta[jet])<3.2:
                    outputTree_p30_eta_25.Fill()
                if inputTree.jetpt[jet]>40 and inputTree.jetpt[jet]<50 and np.abs(inputTree.jetDetectorEta[jet])<3.2:
                    outputTree_p40_eta_25.Fill()
                if inputTree.jetpt[jet]>50 and np.abs(inputTree.jetDetectorEta[jet])<3.2:
                    outputTree_p50_eta_25.Fill()
                if inputTree.jetpt[jet]<30 and np.abs(inputTree.jetDetectorEta[jet])>3.2:
                    outputTree_p20_eta_32.Fill()
                if inputTree.jetpt[jet]>30 and inputTree.jetpt[jet]<40 and np.abs(inputTree.jetDetectorEta[jet])>3.2:
                    outputTree_p30_eta_32.Fill()
                if inputTree.jetpt[jet]>40 and inputTree.jetpt[jet]<50 and np.abs(inputTree.jetDetectorEta[jet])>3.2:
                    outputTree_p40_eta_32.Fill()
                if inputTree.jetpt[jet]>50 and np.abs(inputTree.jetDetectorEta[jet])>3.2:
                    outputTree_p50_eta_32.Fill()
                FullOutputTree.Fill()

    sys.stdout.write("\n")
    outputFile.Write()
    outputFile.Close()

#########################################################################################################
######################################## END OF FILE ####################################################
#########################################################################################################
