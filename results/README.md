# File Descriptions
Description of files in the `results` folder:

- `individual_best_models.csv`: contains the best performing model for a given participant based on lowest BIC.

- `overall_salience_values.csv`: contains the overall parameter salience values for semantic similarity, phonological similarity, and frequency for the best foraging model (`forage_phonologicaldynamiclocal` - this is the one that uses semantic + phonological + frequency for within-cluster transitions and frequency for global transitions), when combined with different switch methods (`simdrop`, and `troyerextended`). Overall, the “best” model was `forage_phonologicaldynamiclocal` when combined with designations from simdrop method. Model fit was assessed based on largest improvement from the random baseline model based on BIC.

- `subject_salience_values.csv`: contains the best-fitting parameter salience values at the individual subject level for the best-fitting foraging model (`forage_phonologicaldynamiclocal`), when combined with different switch methods (`simdrop`, and `troyerextended`)
	
- `subject_lexical_results.csv`: contains the semantic, phonological, and frequency values for each subject’s fluency list

- `subject_individual_stats.csv`: contains some aggregate statistics about number of switches, cluster size (mean and standard deviation) for different methods (`simdrop`, `troyerextended`, and `delta_rise=0_fall=1`) for both versions

- `subject_switch_results.csv`: contains the switch designations for each transition within a fluency list for all subjects for different switch methods (`simdrop`, `troyerextended`, and  `delta_rise=0_fall=1`)

