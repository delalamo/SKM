---
title: Bispecific antibodies
created: 2026-04-10T14:02:57
modified: "2026-04-20T08:32:20"
aliases:
  - trispecific antibodies, multispecific antibodies
---

*Redirects from trispecific antibodies, polyspecific antibodies*
**Bispecific antibodies** are [[Antibodies|antibodies]] that can bind to two targets. These are designed to either be combinatorial (where the antibodies can bind to either target alone, and thus have double the breadth of equivalent mAbs) or obligate (where the antibodies are too low-affinity to bind to either target unless the other is also present). In general, each arm can function either by receptor inhibition, receptor activation, payload delivery, [[Checkpoint inhibition|checkpoint inhibition]] (for targeting cancer), [[T cell]] engagement, or T cell stimulation.

![[Pasted-image-20251201142413.png]]
*Ref [@klein2024]*

#### Mechanisms

* Dual receptor inhibition:
	* Amivantamab shows that blocking both [[EGFR]] and [[MET]] in a single molecule is more effective at inhibiting growth compared to blocking just one receptor alone
	* Other combinations include EGFR and LGR5 (Petosemtamab), [[HER2]] and [[HER3]] (Zenocutuzumab), HER3 and EGFR (Izalontamab), and [[Biparatopic]] binding of HER2 (Zanidatamab)
* Ligand receptor inhibition: prevents either ligand binding or receptor oligomerization
	* [[VEGF]] and [[DLL4]]
	* [[VEGF]] and either [[PD-1]] (Ivonescimab) or [[PD-L1]] (PM8002)
* Receptor activation, sometimes via cytokine fusion
	* Bispecificity can overcome [[Decoy receptors|decoy receptors]] that bind ligand without propagating signal
* Targeted payload delivery, either by pre-binding of payload with one arm and targeting tumor with another, or by targeting tumor with both arms and releasing bound payload upon binding
	* Examples include biparatopic HER2, biparatopic MET
* Dual checkpoint inhibitor
	* Advantages compared to single target inhibition:
 * Improved safety by avoiding autoimmune-related events, or undesired activation of immune cells. Bispecifics have greater selectivity compared to normal mAbs
 * Improved efficacy due to lower likelihood of tumors developing resistance
	* Majority of anti-solid tumor treatments involve checkpoint inhibition
	* Can be targeted by [[CTLA4]], PD1, PDL1, LAG3, TGF-beta
	* PD1 can be inhibited by phosphatase recruitement (via CD45, which is a phosphatase)
* Checkpoint inhibitor/mutein
	* Latikafusp fuses an [[IL-21]] mutein to an anti-PD1 antibody
	* Eciskafusp fuses an [[IL-2]] mutein to an anti-PD antibody.
* T cell engagers
	* Targets:
 * [[CD3]]-epsilon, albeit with lower affinity to uncouple from [[Cytokines|cytokine]] secretion
 * [[T-cell receptors|TCRs]]
 * MHC complexes (using widely recognized antigens such as those from [[Cytomegalovirus]]).
	* Avoid [[Fc-gamma-receptors|FcgR]]-binding capabilities, and sometimes longer half-life is restored by introducing a [[Human serum albumin]]-binding region
	* Similar to [[Antibody-drug conjugates|antibody-drug conjugates]] in that they have high killing potency
 * Lineage-specific antigens are preferred
	* Less "bystander killing" of antigen-lacking tumor cells than ADCs, leading to fewer feasible targets
	* Less effective in solid tumors due to tumor antigens being more common in normal tissues
 * Overcome by using two or three targets with detuning, and also to avoid escape by antigen loss
* [[Natural killer cells|Natural killer cell]] engagers
	* Use CD16, NKG2D, NKp46, NKp30
	* Fc effector functions desired
* Myeloid-derived cells and the "don't eat me signal" mediated by SIRP1-alpha/CD47
	* Can be stopped by inhibiting either CD47 (achieved in bispecifics that also target CD19 or mesothelin; these bind CD47 with low affinity to avoid off-target effects) or with SIRP-alpha fusions
* Co-stimulatory bispecifics
	* One arm binds tumor, the other binds the immune cell (via [[4-1BB]], [[CD40]], or [[CD28]])
