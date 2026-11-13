# GitHub and Zenodo publication checklist

1. Review every file and confirm that the 335-row dataset can be made public.
2. Confirm authorization from all relevant rights holders for MIT-licensed code and CC BY 4.0 data. These licenses are included in the package.
3. Create an empty public GitHub repository (do not initialize it with a README or license) (suggested name: `dra-self-sensing`) and upload the files in this package. Do not upload HFSS projects or personal/local files.
4. Check that the README renders correctly. Verify that `python src/train_evaluate.py --check` succeeds in a clean environment.
5. Log in to Zenodo at https://zenodo.org and connect GitHub in Zenodo's GitHub settings, authorizing the selected repository. Check current interface instructions; the integration and release workflow may change.
6. Enable archiving for the repository. On GitHub, create a release with tag `v1.0.0` and a short release note describing the archived code and accepted dataset.
7. Wait for Zenodo to ingest the release, then review the Zenodo record: title, all contributors, affiliations, description, keywords, license, and related identifiers. Link the associated article DOI once available.
8. Copy the DOI of the specific archived version into the paper's Data Availability Statement. Prefer the version DOI for an exact reproducibility snapshot; Zenodo may also issue a concept DOI covering all versions.
9. Before submission, verify the DOI resolves and the Zenodo record contains the expected files. Keep the archived release unchanged; subsequent corrections require a new release/version.

## Suggested Zenodo title

`Numerical dataset and regression code for a self-sensing dielectric resonator antenna`

## Suggested description

`Accepted full-wave simulation responses (n = 335) and Python code for cross-validated regression of relative permittivity and dielectric loss tangent from single-port reflection features of a fixed-geometry rectangular dielectric resonator antenna. The deposit reproduces the principal regression evaluation; it excludes HFSS project files, raw electromagnetic sweeps, and auxiliary simulation studies.`

## Suggested Data Availability Statement for the paper

`The accepted full-wave simulation dataset and Python code used for the main regression analysis are publicly available in Zenodo at [DOI]. The deposit contains the extracted reflection-response features and material parameters. The HFSS project files, raw frequency sweeps, and auxiliary simulation datasets are not included in this deposit.`

Replace `[DOI]` only after the Zenodo record is public. Confirm the journal's current data-sharing policy and respond to any editor request for further supporting data.