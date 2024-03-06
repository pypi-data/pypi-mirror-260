@click.command()
@click.argument('fastq_file_path', type=click.Path(exists=True))
@click.option('--engine', default='biopython', help='Engine to use for reading FASTQ file')
@click.option('--slice-seq', nargs=2, type=int, help='Slice sequence range')
def main(fastq_file_path, engine, slice_seq):
    """
    Command line interface for working with NGS data.
    """
    fastq_to_count_unique_seq(fastq_file_path, engine=engine, slice_seq=slice_seq)


if __name__ == '__main__':
    main()
