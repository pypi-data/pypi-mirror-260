import pyBigWig
import numpy as np
import pandas as pd
import pysam
from tqdm import tqdm


class GCoverages:
    """
    GCoverages module

    This module contains functions and classes for working with a collection of
    genomic coverages. It provides utilities for handling and analyzing the
    interactions of many genomic coverages.
    """
    def __init__(self, bin_size: int = 1):
        """Initialize GCoverages object.

        :param bin_size: Size of the bin for coverage calculation.
                         Defaults to 1 (single nucleotide resolution).
        :type bin_size: str
        """
        self.coverage = {}
        self.bin_size = bin_size

    def load_coverage_from_bigwig(self, filename: str):
        """Load coverage data from a bigwig file.

        :param filename: Path to the bigwig file.
        :type filename: str
        """
        bw = pyBigWig.open(filename)
        chromosomes = bw.chroms()
        for chrom, chrom_length in chromosomes.items():
            coverage = bw.values(chrom, 0, chrom_length, numpy=True)
            if self.bin_size > 1:
                coverage = [np.mean(coverage[i:i+self.bin_size])
                            for i in range(0, len(coverage), self.bin_size)]
            self.coverage[chrom] = coverage
        bw.close()

    def calculate_coverage_from_bam(self, filename: str):
        """Calculate coverage from a BAM file.

        :param filename: Path to the BAM file.
        :type filename: str
        """
        bam = pysam.AlignmentFile(filename, "rb")
        for pileupcolumn in bam.pileup():
            chrom = bam.get_reference_name(pileupcolumn.reference_id)
            if chrom not in self.coverage:
                self.coverage[chrom] = [0] * bam.get_reference_length(chrom)
            self.coverage[chrom][pileupcolumn.reference_pos] += 1
        bam.close()
        # Adjust for bin size
        for chrom in self.coverage:
            if self.bin_size > 1:
                self.coverage[chrom] = [sum(self.coverage[chrom]
                                            [i:i+self.bin_size])
                                        / self.bin_size
                                        for i in range(0,
                                        len(self.coverage[chrom]),
                                        self.bin_size)]

    def calculate_coverage_GRegions(self, regions, scores,
                                    strandness: bool = False):
        """Calculate the coverage from two GRegions. `regions` defines the loci for the coverage
        `scores` contains the scores loaded into the coverage.

        :param regions: Define the loci and the length of the coverage
        :type regions: GRegions
        :param scores: Provide the scores for calculating the coverage
        :type scores: GRegions
        :param strandness: Make this operation strandness specific, defaults
                           to False
        :type strandness: bool, optional
        """
        from genomkit import GRegions
        assert isinstance(regions, GRegions)
        assert isinstance(scores, GRegions)
        filtered_scores = scores.intersect(target=regions,
                                           mode="ORIGINAL")
        for region in tqdm(regions, desc="Calculating coverage",
                           total=len(regions)):
            self.coverage[region] = np.zeros(shape=len(region) //
                                             self.bin_size)
            for target in filtered_scores:
                if region.overlap(target, strandness=strandness):
                    start_ind = (max(0, target.start - region.start))
                    start_ind = start_ind // self.bin_size
                    end_ind = (min(len(region), target.end - region.start))
                    end_ind = end_ind // self.bin_size
                    for i in range(start_ind, end_ind):
                        self.coverage[region][i] += target.score

    def get_coverage(self, seq_name: str):
        """Get coverage data for a specific sequence by name. This sequence
        can be a chromosome or a genomic region.

        :param seq_name: sequence name.
        :type seq_name: str
        :return: Coverage data for the specified sequence.
        :rtype: numpy array
        """
        return self.coverage.get(seq_name, [])

    def filter_regions_coverage(self, regions):
        """Filter regions for their coverages.

        :param regions: GRegions object containing regions.
        :type regions: GRegions
        :return: Dictionary where keys are region objects and values are
                 coverage lists.
        :rtype: dict
        """
        filtered_coverages = {}
        for region in regions:
            if region.sequence in self.coverage:
                start = region.start - 1  # 0-based indexing
                end = region.end
                coverage = self.coverage[region.sequence][start:end]
                filtered_coverages[region] = coverage
        return filtered_coverages

    def total_sequencing_depth(self):
        """Calculate the total sequencing depth.

        :return: Total sequencing depth.
        :rtype: float
        """
        total_depth = 0
        for chrom, cov in self.coverage.items():
            total_depth += np.nansum(cov)
        return total_depth

    def scale_coverage(self, coefficient):
        """Scale the coverages by a coefficient.

        :param coefficient: Coefficient to scale the coverages.
        :type coefficient: float
        """
        for chrom in self.coverage:
            # Replace NaN values with 0 before scaling
            self.coverage[chrom][np.isnan(self.coverage[chrom])] = 0
            # Scale the non-NaN values
            self.coverage[chrom] = self.coverage[chrom] * coefficient

    def flip_negative_regions(self):
        """Flip the coverage arrays which are on the negative strands. If the
        coverage arrays are calculated by the whole chromosomes, it won't
        work.
        """
        for region, cov in self.coverage.items():
            if region.orientation == "-":
                self.coverage[region] = cov[::-1]

    def get_dataframe(self):
        """Return a pandas dataframe concatenating all coverage arrays."""
        df = pd.DataFrame(self.coverage)
        df = df.transpose()
        df.index.name = None
        return df
