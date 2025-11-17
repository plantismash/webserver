# Advanced Options Change History

## Summary

The "Advanced options" section in the plantiSMASH webserver was introduced in the **initial import** on **May 14, 2019**.

## Details

### Initial Introduction

- **Commit**: `525e293d30b834899e97bc93d67d68c6536634f9`
- **Date**: Tuesday, May 14, 2019 at 16:39:43 +0200
- **Author**: PlantiSMASH <plantismash@bioinformatics.nl>
- **Message**: "Imported from https://bitbucket.org/antismash/runsmash"
- **File**: `websmash/templates/new.html`

### Advanced Options Included

The advanced options section included three configurable parameters from the start:

1. **CD-HIT Cutoff**
   - Field name: `cdh_cutoff`
   - Default value: 0.5
   - Description: CD-HIT Cutoff parameter

2. **Minimum unique domains**
   - Field name: `min_domain`
   - Default value: 2
   - Description: Minimum unique domains parameter

3. **MAD Cutoff (CoExpress)**
   - Field name: `coexpress_mad`
   - Default value: not set (only filter out genes with 0 MAD)
   - Description: MAD Cutoff for CoExpress analysis

### Changes Since Introduction

The advanced options section has **remained unchanged** since its introduction. The three parameters and their default values have been consistent throughout the repository's history in this webserver implementation.

### Location in Code

The advanced options can be found in:
- File: `websmash/templates/new.html`
- Lines: 106-129 (current version)
- HTML structure: Collapsible fieldset with Bootstrap classes

### Implementation Details

The advanced options are implemented as:
- A collapsible section that expands/collapses with Bootstrap's collapse functionality
- Three text input fields with default values
- Client-side JavaScript to toggle the plus/minus icon when expanding/collapsing

## Historical Context

The advanced options were part of the original codebase imported from the antiSMASH runsmash project on Bitbucket. This suggests these options were established features from the antiSMASH project that were carried over to the plantiSMASH webserver.

## Complete Timeline of Changes to new.html

Below is a complete timeline of all commits that modified the `websmash/templates/new.html` file, showing that the advanced options section has remained unchanged since the initial import:

| Date | Author | Commit | Description |
|------|--------|--------|-------------|
| 2025-10-20 | Elena Del Pup | `ce8fccd` | Change the license and add GitHub link |
| 2025-10-15 | Elena Del Pup | `e4f7955` | Change things website |
| 2025-10-15 | Elena Del Pup | `10a213b` | Edit developer notice |
| 2025-05-14 | Elena Del Pup | `7d75bff` | Adjust logo scaling and add developer notice for new version |
| 2025-04-17 | Elena Del Pup | `28c03af` | Add hyperlinks to documentation and hide developer notice |
| 2025-03-17 | Elena Del Pup | `21f49fd` | Add development notice box |
| 2024-12-19 | Elena Del Pup | `9b49705` | Add links to precalc |
| 2024-12-18 | Elena Del Pup | `c54c241` | Adjust webpages |
| 2024-12-16 | Elena Del Pup | `213c645` | Update info and helper to version 2.0 |
| 2024-11-22 | Arjan Draisma | `2cb4d41` | update precalc link again |
| 2024-11-22 | Arjan Draisma | `2a611c3` | update precalc link |
| 2020-06-22 | Satria A Kautsar | `da697f3` | Update new.html |
| 2019-12-12 | PlantiSMASH | `5cc7670` | accepts only fasta with gff3 annotation provided |
| 2019-12-12 | PlantiSMASH | `be5b8a2` | Update html |
| 2019-10-01 | PlantiSMASH | `6bca3f1` | move precalc/ url |
| **2019-05-14** | **PlantiSMASH** | **`525e293`** | **Imported from https://bitbucket.org/antismash/runsmash** ← **Advanced options introduced** |

**Note**: None of these subsequent commits modified the advanced options section. All changes were to other parts of the template (navigation, notices, links, etc.).

## Backend Implementation

The backend processing of these advanced options was also introduced in the same initial import commit. The options are processed in:

- **`websmash/views.py`**: Extracts the form parameters and passes them to the model
  - `cdh_cutoff`: Retrieved with default value 0.5 (float)
  - `min_domain_number`: Retrieved with default value 2 (int) - corresponds to `min_domain` field
  - `coexpress_mad`: Retrieved and converted to `min_mad` parameter if provided

- **`websmash/models.py`**: Stores the parameters in the job model
  - `cdh_cutoff`: Stored with default 0.5
  - `min_domain_number`: Stored with default 2

The backend implementation has also remained unchanged since the initial import (commit `525e293`).

## Conclusion

The advanced options feature has been a stable part of the plantiSMASH webserver since its inception on May 14, 2019. All three parameters (CD-HIT Cutoff, Minimum unique domains, and MAD Cutoff) have maintained their default values and implementation throughout the repository's history.
