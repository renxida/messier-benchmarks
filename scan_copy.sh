for memory_mb in {32..256..32};
do
    echo "=== Starting on: $memory_mb ==="
    for copy_mb in {32..256..32};
    do
        echo "    --- starting on: $copy_mb ---"
        fn="scan_copy_output/memory_mb${memory_mb}copy_mb${copy_mb}.out"
        if test -f "$fn"; then
            echo "exists: $fn"
        else
            echo "not found: $fn"
            ~/local/sst/sstcore-10.0.0/bin/sst scan_copy.py --model-options="--memory_mb=$memory_mb --copy_mb=$copy_mb" --print-timing-info 2>&1 | tee $fn
        fi
        #~/local/sst/sstcore-10.0.0/bin/sst scan_copy.py --model-options="--memory_mb=$memory_mb --copy_mb=$copy_mb" --print-timing-info 2>&1 | tee $fn
    done
done