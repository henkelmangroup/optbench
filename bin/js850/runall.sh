dirs="
../../website/minimization/lj38/pele-lbfgs-M1-maxstep0.1/
../../website/minimization/lj38/pele-lbfgs-M10-maxstep0.1/
../../website/minimization/lj38/pele-lbfgs-M100-maxstep0.2/
../../website/minimization/lj38/pele-lbfgs-M20-maxstep0.1/
../../website/minimization/lj38/pele-lbfgs-M4-maxstep0.05/
../../website/minimization/lj38/pele-lbfgs-M4-maxstep0.1/pele-lbfgs-M4-maxstep0.2/
../../website/minimization/lj38/scipy-lbfgs
../../website/minimization/lj38/pele-fire/
"

orig_dir=$PWD

for d in $dirs; do
  echo $d
  cd $orig_dir
  cd $d
  ./run.sh
  cd $orig_dir
done

