📊 AionData
===========

AionData is a common data access layer designed for AI-driven drug discovery software. It provides a unified interface to access diverse biochemical databases.

Installation
------------

To install AionData, ensure you have Python 3.10 or newer installed on your system. You can install AionData via pip:

```bash
pip install aiondata
```

Datasets
--------

AionData provides access to the following datasets:

- **BindingDB**: A public, web-accessible database of measured binding affinities, focusing chiefly on the interactions of proteins considered to be drug-targets with small, drug-like molecules.

- **MoleculeNet**: An extensive collection of datasets curated to support and benchmark the development of machine learning models in the realm of drug discovery and chemical informatics. Covers a broad spectrum of molecular data including quantum mechanical properties, physical chemistry, biophysics, and physiological effects.
 
    - **Tox21**: Features qualitative toxicity measurements for 12,000 compounds across 12 targets, used for toxicity prediction.
    - **ToxCast**: ToxCast is a large-scale dataset for toxicity prediction, which includes over 600 experiments across 185 assays.
    - **ESOL**: Contains water solubility data for 1,128 compounds, aiding in solubility prediction models.
    - **FreeSolv**: Provides experimental and calculated hydration free energy for small molecules, crucial for understanding solvation.
    - **Lipophilicity**: Includes experimental measurements of octanol/water distribution coefficients (logD) for 4,200 compounds.
    - **QM7**: A dataset of 7,165 molecules with quantum mechanical properties computed using density functional theory (DFT).
    - **QM8**: Features electronic spectra and excited state energies of over 20,000 small molecules computed with TD-DFT.
    - **QM9**: Offers geometric, energetic, electronic, and thermodynamic properties of ~134k molecules computed with DFT.
    - **MUV**: Datasets designed for the validation of virtual screening techniques, with about 93,000 compounds.
    - **HIV**: Contains data on the ability of compounds to inhibit HIV replication, for binary classification tasks.
    - **BACE**: Includes quantitative binding results for inhibitors of human beta-secretase 1, with both classification and regression tasks.
    - **BBBP**: Features compounds with information on permeability properties across the Blood-Brain Barrier.
    - **SIDER**: Contains information on marketed medicines and their recorded adverse drug reactions, for side effects prediction.
    - **ClinTox**: Compares drugs approved by the FDA and those that failed clinical trials for toxicity reasons, for binary classification and toxicity prediction.

- **Foldswitch Proteins**: Datasets from the paper [AlphaFold2 fails to predict protein fold switching](https://pubmed.ncbi.nlm.nih.gov/35634782/) featuring information on fold-switching proteins. These datasets provide insights into the structural dynamics and functional versatility of proteins, highlighting cases where AlphaFold2's predictive capabilities are challenged.

    - **Table S1A**: Lists pairs of proteins (PDBIDs), their lengths, and the sequence of the fold-switching region. For some pairs, only the first fold's PDBID is available if the second fold has not been solved.
    - **Table S1B**: Offers RMSD and TM-scores for the whole protein and the fold-switching fragment specifically, along with sequence identities between the fold-switching pairs.
    - **Table S1C**: Provides a list of fold-switching protein pairs (PDBID and chain) used for analysis, including TM-scores of the predictions.

- **CodNas91**: A dataset curated from the paper [Impact of protein conformational diversity on AlphaFold predictions](https://pubmed.ncbi.nlm.nih.gov/35561203/), featuring 91 proteins with varying degrees of conformational diversity. This dataset focuses on apo–holo pairs selected for their significant structural changes associated with biological processes.


License
-------

AionData is licensed under the Apache License. See the LICENSE file for more details.