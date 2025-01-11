# psychosis-foraging

Description of files in the `results` folder:

- `overall_salience_values.csv`: contains the overall parameter salience values for semantic similarity, phonological similarity, and frequency for the best foraging model (`forage_phonologicaldynamiclocal` - this is the one that uses semantic + phonological + frequency for within-cluster transitions and frequency for global transitions), when combined with different switch methods (`simdrop`, `troyerextended`, and  `delta_rise=0_fall=1`)

Overall, the “best” model was `forage_phonologicaldynamiclocal` when combined with designations from the delta similarity method (rise=0, fall=1)
	
- `subject_salience_values.csv`: contains the best-fitting parameter salience values at the individual subject level for the best-fitting foraging model (`forage_phonologicaldynamiclocal`), when combined with different switch methods (`simdrop`, `troyerextended`, and  `delta_rise=0_fall=1`)

- `subject_lexical_results.csv`: contains the semantic, phonological, and frequency values for each subject’s fluency list

- `subject_individual_stats.csv`: contains some aggregate statistics about number of switches, cluster size (mean and standard deviation) for different methods (`simdrop`, `troyerextended`, and `delta_rise=0_fall=1`) for both versions

- `subject_switch_results.csv`: contains the switch designations for each transition within a fluency list for all subjects for different switch methods (`simdrop`, `troyerextended`, and  `delta_rise=0_fall=1`)
