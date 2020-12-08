set -e
for cpucount in {1,4,16};
do
    echo "=== Starting on: $cpucount ==="
    outdir="massif-networked-noval/cpucount__$cpucount/"
    if test -f "$outdir"; then
        echo "exists: $outdir"
    else
        echo "not found: $outdir; running"
        mkdir -p $outdir
        ~/local/sst/sstcore-10.0.0/bin/sst networked.py --model-options="--cpucount=$cpucount" --print-timing-info 2>&1 | tee $outdir/stdouterr.txt
    fi
        #~/local/sst/sstcore-10.0.0/bin/sst scan_copy.py --model-options="--memory_mb=$memory_mb --copy_mb=$copy_mb" --print-timing-info 2>&1 | tee $fn
done
