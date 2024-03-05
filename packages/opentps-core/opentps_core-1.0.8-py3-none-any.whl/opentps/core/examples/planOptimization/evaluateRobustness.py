
import os
import datetime

import numpy as np
from matplotlib import pyplot as plt
from opentps.core.data.images import CTImage
from opentps.core.data.images import ROIMask
from opentps.core.data.plan import PlanDesign
from opentps.core.data import Patient
from opentps.core.io import mcsquareIO
from opentps.core.io.scannerReader import readScanner
from opentps.core.io.serializedObjectIO import saveRTPlan, loadRTPlan
from opentps.core.processing.doseCalculation.doseCalculationConfig import DoseCalculationConfig
from opentps.core.processing.doseCalculation.mcsquareDoseCalculator import MCsquareDoseCalculator
from opentps.core.processing.planEvaluation.robustnessEvaluation import Robustness


def run():
    output_path = os.getcwd()

    # Generic example: box of water with squared target

    ctCalibration = readScanner(DoseCalculationConfig().scannerFolder)
    bdl = mcsquareIO.readBDL(DoseCalculationConfig().bdlFile)

    patient = Patient()
    patient.name = 'Patient'

    ctSize = 150

    ct = CTImage()
    ct.name = 'CT'
    ct.patient = patient


    huAir = -1024.
    huWater = ctCalibration.convertRSP2HU(1.)
    data = huAir * np.ones((ctSize, ctSize, ctSize))
    data[:, 50:, :] = huWater
    ct.imageArray = data

    roi = ROIMask()
    roi.patient = patient
    roi.name = 'TV'
    roi.color = (255, 0, 0) # red
    data = np.zeros((ctSize, ctSize, ctSize)).astype(bool)
    data[100:120, 100:120, 100:120] = True
    roi.imageArray = data

    # Create output folder
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    # Configure MCsquare
    mc2 = MCsquareDoseCalculator()
    mc2.beamModel = bdl
    mc2.nbPrimaries = 5e4
    mc2.statUncertainty = 2.
    mc2.ctCalibration = ctCalibration

    # Load / Generate new plan
    plan_file = os.path.join(output_path, "Plan_WaterPhantom_cropped_resampled.tps")

    if os.path.isfile(plan_file):
        plan = loadRTPlan(plan_file)
        print('Plan loaded')
    else:
        print("You need to design and optimize a plan first - See SimpleOptimization or robustOptimization script.")

    # Load / Generate scenarios
    scenario_folder = os.path.join(output_path,'RobustnessTest_Nov-16-2022_14-30-28_')
    if os.path.isdir(scenario_folder):
        scenarios = Robustness()
        scenarios.selectionStrategy = Robustness.Strategies.ERRORSPACE_REGULAR
        scenarios.setupSystematicError = plan.planDesign.robustness.setupSystematicError
        scenarios.setupRandomError = plan.planDesign.robustness.setupRandomError
        scenarios.rangeSystematicError = plan.planDesign.robustness.rangeSystematicError
        scenarios.load(scenario_folder)
    else:
        # MCsquare config for scenario dose computation
        mc2.nbPrimaries = 1e7
        plan.planDesign.robustness = Robustness()
        plan.planDesign.robustness.setupSystematicError = [5.0, 5.0, 5.0]  # mm
        plan.planDesign.robustness.setupRandomError = [0.0, 0.0, 0.0]  # mm (sigma)
        plan.planDesign.robustness.rangeSystematicError = 3.0  # %
        plan.planDesign.robustness.selectionStrategy = Robustness.Strategies.ERRORSPACE_REGULAR
        # run MCsquare simulation
        scenarios = mc2.computeRobustScenario(ct, plan, [roi])
        if not os.path.isdir(output_path):
          os.mkdir(output_path)
        output_folder = os.path.join(output_path, "RobustnessTest_" + datetime.datetime.today().strftime("%b-%d-%Y_%H-%M-%S"))
        scenarios.save(output_folder)

    # Robustness analysis
    scenarios.analyzeErrorSpace(ct, "D95", roi, plan.planDesign.objectives.targetPrescription)
    scenarios.printInfo()
    scenarios.recomputeDVH([roi])

    # Display DVH + DVH-bands
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    for dvh_band in scenarios.dvhBands:
        phigh = ax.plot(dvh_band._dose, dvh_band._volumeHigh, alpha=0)
        plow = ax.plot(dvh_band._dose, dvh_band._volumeLow, alpha=0)
        pNominal = ax.plot(dvh_band._nominalDVH._dose, dvh_band._nominalDVH._volume, label=dvh_band._roiName, color = 'C0')
        pfill = ax.fill_between(dvh_band._dose, dvh_band._volumeHigh, dvh_band._volumeLow, alpha=0.2, color='C0')
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Volume (%)")
    plt.grid(True)
    plt.legend()

    plt.show()
if __name__ == "__main__":
    run()
