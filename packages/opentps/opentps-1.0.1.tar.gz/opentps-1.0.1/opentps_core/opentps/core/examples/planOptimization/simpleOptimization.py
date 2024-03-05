import os
import logging
import numpy as np
from matplotlib import pyplot as plt
import sys
import datetime
import pydicom
sys.path.append('..')

from opentps.core.io.dicomIO import writeRTPlan, writeDicomCT, writeRTDose, writeRTStruct
from opentps.core.processing.planOptimization.tools import evaluateClinical
from opentps.core.data.images import CTImage, DoseImage
from opentps.core.data.images import ROIMask
from opentps.core.data.plan import ObjectivesList
from opentps.core.data.plan import PlanDesign
from opentps.core.data import DVH
from opentps.core.data import Patient
from opentps.core.data import RTStruct
from opentps.core.data.plan import FidObjective
from opentps.core.io import mcsquareIO
from opentps.core.io.scannerReader import readScanner
from opentps.core.io.serializedObjectIO import saveRTPlan, loadRTPlan
from opentps.core.processing.doseCalculation.doseCalculationConfig import DoseCalculationConfig
from opentps.core.processing.doseCalculation.mcsquareDoseCalculator import MCsquareDoseCalculator
from opentps.core.processing.imageProcessing.resampler3D import resampleImage3DOnImage3D, resampleImage3D
from opentps.core.processing.planOptimization.planOptimization import IMPTPlanOptimizer

logger = logging.getLogger(__name__)

# Generic example: box of water with squared target
def run(output_path=""):
    if(output_path != ""):
        output_path = output_path
    else:
        output_path = os.getcwd()
        
    logger.info('Files will be stored in {}'.format(output_path))

    ctCalibration = readScanner(DoseCalculationConfig().scannerFolder)
    bdl = mcsquareIO.readBDL(DoseCalculationConfig().bdlFile)

    # CT
    patient = Patient()
    patient.name = 'Simple_Patient'
    
    ctSize = 150
    ct = CTImage()
    ct.name = 'CT'
    ct.patient = patient

    huAir = -1024.
    huWater = ctCalibration.convertRSP2HU(1.)
    data = huAir * np.ones((ctSize, ctSize, ctSize))
    data[:, 50:, :] = huWater
    ct.imageArray = data
    dcm_CT_file = os.path.join(output_path, "CTImage_WaterPhantom_cropped_resampled_optimized")
    writeDicomCT(ct, dcm_CT_file)

    # Struct
    roi = ROIMask()
    roi.patient = patient
    roi.name = 'TV'
    roi.color = (255, 0, 0)  # red
    data = np.zeros((ctSize, ctSize, ctSize)).astype(bool)
    data[100:120, 100:120, 100:120] = True
    roi.imageArray = data

    # contour = roi.getROIContour()
    # struct = RTStruct()
    # struct.appendContour(contour)
    # writeRTStruct(struct, os.path.join(output_path, "struct.dcm"))

    # Design plan
    beamNames = ["Beam1"]
    gantryAngles = [0.]
    couchAngles = [0.]

    # method 1 : create or load existing plan (no workflow)

    # Configure MCsquare
    mc2 = MCsquareDoseCalculator()
    mc2.beamModel = bdl
    mc2.nbPrimaries = 5e4
    mc2.ctCalibration = ctCalibration

    # Load / Generate new plan
    plan_file = os.path.join(output_path, "Plan_WaterPhantom_cropped_resampled.tps")

    if os.path.isfile(plan_file):
        plan = loadRTPlan(plan_file)
        logger.info('Plan loaded')
    else:
        planDesign = PlanDesign()
        planDesign.ct = ct
        planDesign.targetMask = roi
        planDesign.gantryAngles = gantryAngles
        planDesign.beamNames = beamNames
        planDesign.couchAngles = couchAngles
        planDesign.calibration = ctCalibration
        planDesign.spotSpacing = 5.0
        planDesign.layerSpacing = 5.0
        planDesign.targetMargin = 5.0
        planDesign.setScoringParameters(scoringSpacing=[2, 2, 2], adapt_gridSize_to_new_spacing=True)

        plan = planDesign.buildPlan()  # Spot placement
        plan.rtPlanName = "Simple_Patient"

        beamlets = mc2.computeBeamlets(ct, plan, roi=[roi])
        plan.planDesign.beamlets = beamlets
        beamlets.storeOnFS(os.path.join(output_path, "BeamletMatrix_" + plan.seriesInstanceUID + ".blm"))
        # Save plan with initial spot weights in serialized format (OpenTPS format)
        saveRTPlan(plan, plan_file)

    plan.planDesign.objectives = ObjectivesList()
    plan.planDesign.objectives.setTarget(roi.name, 20.0)
    plan.planDesign.objectives.fidObjList = []
    plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMAX, 20.0, 1.0)
    plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMIN, 20.5, 1.0)
    
    solver = IMPTPlanOptimizer(method='Scipy-LBFGS', plan=plan, maxit=1000)
    # Optimize treatment plan
    w, doseImage, ps = solver.optimize()

    # Save plan with updated spot weights in serialized format (OpenTPS format)
    plan_file_optimized = os.path.join(output_path, "Plan_WaterPhantom_cropped_resampled_optimized.tps")
    saveRTPlan(plan, plan_file_optimized)
    # Save plan with updated spot weights in dicom format
    plan.patient = patient
    dcm_Plan_file = os.path.join(output_path, "Plan_WaterPhantom_cropped_resampled_optimized.dcm")
    writeRTPlan(plan, dcm_Plan_file)

    # Compute DVH on resampled contour
    target_DVH = DVH(roi, doseImage)
    print('D5 - D95 =  {} Gy'.format(target_DVH.D5 - target_DVH.D95))
    clinROI = [roi.name, roi.name]
    clinMetric = ["Dmin", "Dmax"]
    clinLimit = [19., 21.]
    clinObj = {'ROI': clinROI, 'Metric': clinMetric, 'Limit': clinLimit}
    print('Clinical evaluation')
    evaluateClinical(doseImage, [roi], clinObj)

    # center of mass
    roi = resampleImage3DOnImage3D(roi, ct)
    COM_coord = roi.centerOfMass
    COM_index = roi.getVoxelIndexFromPosition(COM_coord)
    Z_coord = COM_index[2]

    img_ct = ct.imageArray[:, :, Z_coord].transpose(1, 0)
    contourTargetMask = roi.getBinaryContourMask()
    img_mask = contourTargetMask.imageArray[:, :, Z_coord].transpose(1, 0)
    img_dose = resampleImage3DOnImage3D(doseImage, ct)
    img_dose = img_dose.imageArray[:, :, Z_coord].transpose(1, 0)
    di = DoseImage(imageArray=img_dose, referencePlan=plan, referenceCT=ct, patient=patient)
    
    dcm_dose_file = os.path.join(output_path, "Dose_WaterPhantom_cropped_resampled_optimized.dcm")
    writeRTDose(di, dcm_dose_file)

    # Display dose
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].axes.get_xaxis().set_visible(False)
    ax[0].axes.get_yaxis().set_visible(False)
    ax[0].imshow(img_ct, cmap='gray')
    ax[0].imshow(img_mask, alpha=.2, cmap='binary')  # PTV
    dose = ax[0].imshow(img_dose, cmap='jet', alpha=.2)
    plt.colorbar(dose, ax=ax[0])
    ax[1].plot(target_DVH.histogram[0], target_DVH.histogram[1], label=target_DVH.name)
    ax[1].set_xlabel("Dose (Gy)")
    ax[1].set_ylabel("Volume (%)")
    ax[1].grid(True)
    ax[1].legend()

    convData = solver.getConvergenceData()
    ax[2].plot(np.arange(0, convData['time'], convData['time'] / convData['nIter']), convData['func_0'], 'bo-', lw=2,
               label='Fidelity')
    ax[2].set_xlabel('Time (s)')
    ax[2].set_ylabel('Cost')
    ax[2].set_yscale('symlog')
    ax2 = ax[2].twiny()
    ax2.set_xlabel('Iterations')
    ax2.set_xlim(0, convData['nIter'])
    ax[2].grid(True)

    plt.show()


if __name__ == "__main__":
    run()
