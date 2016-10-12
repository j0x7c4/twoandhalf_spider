ROOT=/data/crawlers/$1
mkdir -p $ROOT
scrapy crawl $1 --logfile $ROOT/$1.log -L INFO -o $ROOT/$1.jl -s JOBDIR=$ROOT/tmp/$1
