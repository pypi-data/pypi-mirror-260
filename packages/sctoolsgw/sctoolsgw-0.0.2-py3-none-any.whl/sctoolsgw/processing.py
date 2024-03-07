import scanpy as sc


def process(adata) -> sc.AnnData:
    """Performs a quick processing workflow on :class:`adata <sc.AnnData>`.

    :param adata: :class:`sc.AnnData` object to be processed.
    """
    adata_cp = adata.copy()

    if not adata_cp.layers["counts"]:
        adata_cp.layers["counts"] = adata_cp.X.copy()

    sc.pp.normalize_total(adata_cp, target_sum=1e6)
    sc.pp.log1p(adata_cp)

    sc.pp.pca(adata_cp)
    sc.pp.neighbors(adata_cp)

    sc.tl.leiden(adata_cp)
    sc.tl.umap(adata_cp)

    return adata_cp
