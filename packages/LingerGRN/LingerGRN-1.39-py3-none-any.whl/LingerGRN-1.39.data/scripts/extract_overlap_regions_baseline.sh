Input_dir=$1
GRNdir=$2
genome=$3
outdir=$4
mkdir $outdir
cd $Input_dir
ml bedtools2/2.26.0-gcc/9.5.0
cat ATAC.txt|cut -f 1 |sed '1d' |sed 's/:/\t/g'| sed 's/-/\t/g' > $outdir/Region.bed
for i in $(seq 1 22); do
bedtools intersect -a "$GRNdir/${genome}_Peaks_chr$i.bed" -b $outdir/Region.bed -wa -wb > $outdir/"Region_overlap_chr$i.bed"
done
i=X
bedtools intersect -a "$GRNdir/${genome}_Peaks_chr$i.bed" -b $outdir/Region.bed -wa -wb > $outdir/"Region_overlap_chr$i.bed"

