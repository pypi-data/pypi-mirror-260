from .datasets import ExcelDataset, CsvDataset


class FoldswitchProteinsTableS1A(ExcelDataset):
    """(A) List of pairs (PDBIDs), lengths and the sequence of the fold-switching region.
    (For those pairs not having the second fold solved in PDB, only the first PDB is reported).

    From Paper: AlphaFold2 fails to predict protein fold switching
    https://doi.org/10.1002/pro.4353
    """

    SOURCE = "https://raw.githubusercontent.com/tomshani/aiondata/tom-branch/data/pro4353-sup-0002-tables1%20/Table_S1A_final.xlsx"
    COLLECTION = "foldswitch_proteins"


class FoldswitchProteinsTableS1B(ExcelDataset):
    """(B) RMSD, TM-scores for the whole protein and only fold-switching fragment,
    as well as sequence identities between the fold-switching pairs.
    wTM-score/wRMSD indicate TM-scores/RMSDs considering whole protein chains.
    fsTM-score/fsRMSD indicate TM-scores/RMSDs considering fold-switching regions only.

    From Paper: AlphaFold2 fails to predict protein fold switching
    https://doi.org/10.1002/pro.4353
    """

    SOURCE = "https://raw.githubusercontent.com/tomshani/aiondata/tom-branch/data/pro4353-sup-0002-tables1%20/Table_S1B_final.xlsx"
    COLLECTION = "foldswitch_proteins"


class FoldswitchProteinsTableS1C(ExcelDataset):
    """(C) List of fold-switching protein pairs (PDBID and chain) used for the analysis,
    first column corresponds to Fold1 and second to Fold2, followed by TM-scores of the predictions.
    Tables attached separately.

    From Paper: AlphaFold2 fails to predict protein fold switching
    https://doi.org/10.1002/pro.4353
    """

    SOURCE = "https://raw.githubusercontent.com/tomshani/aiondata/tom-branch/data/pro4353-sup-0002-tables1%20/Table_S1C_final.xlsx"
    COLLECTION = "foldswitch_proteins"


class CodNas91(CsvDataset):
    """
    Paper: Impact of protein conformational diversity on AlphaFold predictions
    https://doi.org/10.1093/bioinformatics/btac202
    We selected 91 proteins (Supplementary Table S1) with different degrees of conformational diversity expressed as the range of pairwise global Cα-RMSD between their conformers in the PDB (Fig. 1).
    All the pairs of conformers for each protein are apo–holo pairs selected from the CoDNaS database (Monzon et al., 2016) and bibliography. Manual curation for each protein confirmed that structural deformations were associated with a given biological process based on experimental evidence.
    This step is essential to ensure that conformational diversity is not associated with artifacts, misalignments, missing regions, or the presence of flexible ends. When more than two conformers were known, we selected the apo–holo pair showing the maximum Cα-RMSD (maxRMSD).
    Other considerations were absence of disorder, PDB resolution, absence of mutations and sequence differences. We previously observed that when conformational diversity is derived from experimentally based conformers, different ranges of RMSD are obtained between them depending on the structure determination method (Monzon et al., 2017a).
    Here we considered a continuum of protein flexibility measured as the RMSD between apo and holo forms as shown in Figure 1.
    """

    SOURCE = "https://raw.githubusercontent.com/tomshani/aiondata/tom-branch/data/Supplementary_Table_1_91_apo_holo_pairs.csv"
