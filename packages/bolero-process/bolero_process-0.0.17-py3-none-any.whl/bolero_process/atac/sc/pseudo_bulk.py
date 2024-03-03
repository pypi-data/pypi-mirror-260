import pathlib
import shutil
import tempfile

import ray
import xarray as xr
from bolero import Genome

from .zarr_io import CutSitesZarr, global_coverage_to_bigwig


@ray.remote(num_cpus=4)
def _count_zarr(zarr_path, barcodes_category, output_path, chunk_size):
    cut_ds = CutSitesZarr(zarr_path)
    cut_ds.dump_barcodes_category_coverage(
        barcodes_category=barcodes_category,
        zarr_path=output_path,
        chunk_size=chunk_size,
    )


def cutsite_to_coverage_zarr(cell_meta, genome, output_path):
    """
    Convert cutsite zarr to coverage zarr.

    Parameters
    ----------
    cell_meta : pd.DataFrame
        The cell metadata table, with columns "zarr_path" and "category".
    genome : Genome
        The genome object.
    output_path : str
        The output zarr path.
    """
    temp_dir = tempfile.mkdtemp()
    fs = []
    temp_output_paths = []
    temp_zarr_chunk_size = 20_000_000
    for zarr_path, sub_df in cell_meta.groupby("zarr_path"):
        use_cells = sub_df.index
        barcodes_category = sub_df["category"]
        if use_cells.size == 0:
            continue
        name = pathlib.Path(zarr_path).name
        temp_output_path = f"{temp_dir}/{name}"
        temp_output_paths.append(temp_output_path)

        f = _count_zarr.remote(
            zarr_path=zarr_path,
            barcodes_category=barcodes_category,
            output_path=temp_output_path,
            chunk_size=temp_zarr_chunk_size,
        )
        fs.append(f)
    _ = ray.get(fs)

    chroms = genome.chrom_offsets.index
    first_chunk = True
    for chrom in chroms:
        ds_list = []
        for temp_output_path in temp_output_paths:
            ds = xr.open_zarr(f"{temp_output_path}/{chrom}/").astype("float32")
            ds_list.append(ds)
        sum_ds = xr.concat(ds_list, dim="zarr").sum(dim="zarr").astype("float32")
        sum_ds.attrs["genome"] = genome.name

        if first_chunk:
            category_chunk = max(50, sum_ds.sizes["category"])
            position_chunk = int(5000000 / category_chunk)
            load_chunks = min(int(position_chunk * 50), temp_zarr_chunk_size)

        for chunk_start in range(0, sum_ds.sizes["position"], load_chunks):
            print(f"Write {chrom}:{chunk_start}-{chunk_start+load_chunks}")
            ds_to_write = sum_ds.isel(position=slice(chunk_start, chunk_start + load_chunks)).load()
            # DO NOT USE sum_ds.chunk, which has a bug that will contain nan in the result
            # load data to memory and then modify encoding
            ds_to_write["site_count"].encoding["chunks"] = (category_chunk, position_chunk)
            if first_chunk:
                ds_to_write.to_zarr(output_path, mode="w")
                first_chunk = False
            else:
                ds_to_write.to_zarr(output_path, append_dim="position")
    shutil.rmtree(temp_dir)
    return


def coverage_zarr_to_bigwigs(zarr_path, bigwig_dir, cell_types=None):
    """
    Convert coverage zarr to bigwig files.

    Parameters
    ----------
    zarr_path : str
        The input zarr path.
    bigwig_dir : str
        The output bigwig directory.
    cell_types : list of str
        The cell types to convert. If None, convert all cell types.
    """
    coverage_ds = xr.open_zarr(zarr_path)
    genome = Genome(coverage_ds.attrs["genome"])
    chrom_offsets = genome.chrom_offsets

    bigwig_dir = pathlib.Path(bigwig_dir)
    bigwig_dir.mkdir(exist_ok=True, parents=True)

    @ray.remote
    def gen_bw(ct, conv):
        coverage_ds = xr.open_zarr("TotalCellTypeCount.zarr")
        coverage = coverage_ds["site_count"].sel(category=ct).values
        global_coverage_to_bigwig(
            coverage,
            chrom_offsets,
            bigwig_path=f"bigwig/{ct}.conv{conv}.bw",
            convolve_bp=conv,
            resolution_bp=1,
        )

    fs = []
    if cell_types is None:
        cell_types = coverage_ds.get_index("category")

    for ct in coverage_ds.get_index("category"):
        for conv in [0, 20]:
            f = gen_bw.remote(ct=ct, conv=conv)
            fs.append(f)
    _ = ray.get(fs)
    return
