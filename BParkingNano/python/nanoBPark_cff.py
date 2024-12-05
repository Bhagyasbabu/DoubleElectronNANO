from __future__ import print_function
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.globals_cff import *
from PhysicsTools.NanoAOD.nano_cff import *
from PhysicsTools.NanoAOD.vertices_cff import *
from PhysicsTools.NanoAOD.NanoAODEDMEventContent_cff import *
from PhysicsTools.BParkingNano.trgbits_cff import *

##for gen and trigger muon
from PhysicsTools.BParkingNano.genparticlesBPark_cff import *
from PhysicsTools.BParkingNano.particlelevelBPark_cff import *
from PhysicsTools.BParkingNano.triggerObjectsBPark_cff import *
# from PhysicsTools.BParkingNano.muonsBPark_cff import * 

## filtered input collections
from PhysicsTools.BParkingNano.electronsBPark_cff import * 
from PhysicsTools.BParkingNano.tracksBPark_cff import *

## Dielectron collection
from PhysicsTools.BParkingNano.dielectron_cff import *

# nanoSequenceOnlyFullSim = cms.Sequence(triggerObjectBParkTables + l1bits)
nanoSequenceOnlyFullSim = cms.Sequence(electronTriggerObjectBParkTables + l1bits)

nanoSequence = cms.Sequence(nanoMetadata + 
                            cms.Sequence(vertexTask) +
                            cms.Sequence(globalTablesTask) + cms.Sequence(vertexTablesTask) +
                            # triggerObjectBParkTables + l1bits)
                            electronTriggerObjectBParkTables + l1bits)

nanoSequenceMC = cms.Sequence(particleLevelBParkSequence + genParticleBParkSequence + 
                              cms.Sequence(globalTablesMCTask) + cms.Sequence(genWeightsTableTask) + genParticleBParkTables + lheInfoTable)

from PhysicsTools.BParkingNano.electronsTrigger_cff import *

def nanoAOD_customizeEle(process):
    process.nanoEleSequence = cms.Sequence(
        myUnpackedPatTrigger
        +myPFTriggerMatches
        +myLPTriggerMatches
        +mySlimmedPFElectronsWithEmbeddedTrigger
        +mySlimmedLPElectronsWithEmbeddedTrigger
        +electronTrgSelector
        +hltHighLevel)
    return process

# def nanoAOD_customizeMuonTriggerBPark(process):
#     process.nanoSequence = cms.Sequence( process.nanoSequence + muonBParkSequence + muonBParkTables)#+ muonTriggerMatchedTables)   ###comment in this extra table in case you want to create the TriggerMuon collection again.
#     return process

# def nanoAOD_customizeTrackFilteredBPark(process):
#     process.nanoTracksSequence = cms.Sequence( tracksBParkSequence + tracksBParkTables)
#     return process

def nanoAOD_customizeElectronFilteredBPark(process):
    process.nanoDiEleSequence     = cms.Sequence(electronsBParkSequence + electronBParkTables)
    return process

def nanoAOD_customizeElectronTriggerSelectionBPark(process):
    process.nanoDiEleSequence = cms.Sequence( process.nanoDiEleSequence + electronBParkTriggerSelection)
    return process

def nanoAOD_customizeTriggerBitsBPark(process):
    process.nanoSequence = cms.Sequence( process.nanoSequence + trgTables)
    return process

def nanoAOD_customizeDiElectron(process):
    process.nanoDiEleSequence = cms.Sequence( process.nanoDiEleSequence + DiElectronSequence)
    return process

from FWCore.ParameterSet.MassReplace import massSearchReplaceAnyInputTag
def nanoAOD_customizeMC(process):
    for name, path in process.paths.iteritems():
        # replace all the non-match embedded inputs with the matched ones
        massSearchReplaceAnyInputTag(path, 'muonTrgSelector:SelectedMuons', 'selectedMuonsMCMatchEmbedded')
        #massSearchReplaceAnyInputTag(path, 'electronTrgSelector:SelectedElectrons', 'selectedElectronsMCMatchEmbedded') # Is this needed if the trigger is emulated ???
        massSearchReplaceAnyInputTag(path, 'electronsForAnalysis:SelectedElectrons', 'selectedElectronsMCMatchEmbedded')
        massSearchReplaceAnyInputTag(path, 'tracksBPark:SelectedTracks', 'tracksBParkMCMatchEmbedded')

        # modify the path to include mc-specific info
        path.insert(0, nanoSequenceMC)
        # path.replace(process.muonBParkSequence, process.muonBParkMC)
        path.replace(process.electronsBParkSequence, process.electronBParkMC)
        path.replace(process.tracksBParkSequence, process.tracksBParkMC)
