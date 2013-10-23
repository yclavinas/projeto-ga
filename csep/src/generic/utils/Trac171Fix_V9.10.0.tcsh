#!/bin/tcsh

# Script to recompute cumulative L, R, M and S tests results for all forecasts
# groups within SCEC Testing Center

source /home/csep/.tcshrc;

pushd $CSEP/SCEC-natural-laboratory;
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=RELM-mainshock-aftershock-models --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=RELM-mainshock-aftershock-models-corrected --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=RELM-mainshock-models --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=RELM-mainshock-models-corrected --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=three-months-models --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=three-months-models-V9.4 --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=one-day-models --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=one-day-models-V9.1 --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=five-year-rate-models --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=five-year-rate-models-V9.1 --tests="L R S M";
popd;

pushd $CSEP/testing-regions/SWPacific;
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=one-day-models --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=one-year-models --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=one-year-models-V9.1 --tests="L R S M";
popd;

pushd $CSEP/testing-regions/NWPacific;
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=one-day-models --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=one-year-models --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=one-year-models-V9.1 --tests="L R S M";
popd;

pushd $CSEP/testing-regions/Global;
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=one-year-models --tests="L R S M";
python $CENTERCODE/src/generic/ResultsCumulativeSummary.py --forecasts=one-day-models-V9.7 --tests="L R S M";
popd;
