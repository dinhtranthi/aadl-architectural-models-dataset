# AADL Architectural Models Dataset

This repository provides a curated dataset of AADL architectural models mined from public GitHub repositories, enriched with multi-level annotations and reference architecture (RA) alignment artifacts.

The dataset is introduced in:

> *Mining Architectural Models in the Wild: A Curated Dataset of AADL Models* 

---

## Overview

This dataset provides the **curated and validated collection of AADL architectural models** collected from real-world projects, supporting reproducible research on software architecture analysis, reuse, and AI-driven techniques.

It includes:

- validated AADL models mined from GitHub  
- generic domain and specific problem level annotations for clustering  
- component-level mappings to reference architectures  
- full provenance metadata and reproducible pipeline  

---

## Repository Structure

```text
.
├── dataset/
│   ├── models/
│   │   ├── xmi/
│   │   └── json/
│   ├── metadata.csv
│   ├── annotations/
│   │   ├── generic_domain_clusters.csv
│   │   ├── specific_domain_clusters.csv
│   │   └── ra_alignment.csv
│   └── reference_architectures/
│       ├── SMART_HOME/
│       ├── SMART_PARKING/
│       ├── SELF_DRIVING_CAR/
│       ├── DRONE_CONTROL/
│       ├── FLIGHT_MANAGEMENT_SYSTEM/
│       └── CRUISE_CONTROL/
│
├── schema/
│   ├── model_metadata_schema.json
│   └── ra_mapping_schema.json
│
├── scripts/
│
├── experiment_protocol/
│   ├── ra_validation_protocol.md
│   └── ANNOTATION_GUIDELINES.md
│
├── figures/
├── CITATION.cff
└── README.md
```
---

## Dataset Content

* **Models** (`dataset/models/`): AADL models in `.aaxl2` and JSON formats
* **Metadata** (`dataset/metadata.csv`): provenance and structural information
* **Annotations** (`dataset/annotations/`):

  * 13 generic domains
  * 49 specific problem clusters
  * RA component mappings
* **Reference Architectures**: multiple domains (e.g., SMART_HOME, SELF_DRIVING_CAR, DRONE_CONTROL)
* **Schema**: JSON schemas for structured data access

---

## Usage

The dataset supports research on:

* architectural clustering and similarity
* machine learning and LLM-based analysis of architectures
* reference architecture conformance and alignment
* architectural reuse and variability

---

## Reproducibility

The repository includes:

* scripts for mining, validation, and preprocessing
* full provenance metadata
* schema definitions for structured processing
* a documented protocol for RA mapping validation

---

## License

See `LICENSE` for usage terms.
Original models retain references to their source repositories.

---

## Citation

If you use this dataset, please cite the dataset and the associated paper.
See `CITATION.cff`.
