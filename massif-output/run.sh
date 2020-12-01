valgrind --tool=massif --time-unit=ms --trace-children=yes --massif-out-file=./massif_%p_output --log-file=./log/massif_%p.log ~/local/sst/sstcore-10.0.0/bin/sst ~/messier-benchmarks/scan_copy.py --model-options="--memory_mb=1 --copy_mb=1024"
