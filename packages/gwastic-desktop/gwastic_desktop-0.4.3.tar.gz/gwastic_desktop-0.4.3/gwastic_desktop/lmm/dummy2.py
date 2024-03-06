from pysnptools.snpreader import Pheno, Bed
from fastlmm.inference import FastLMM
import numpy as np
from fastlmm.util import example_file
from sklearn.model_selection import KFold  # install scikit-learn
import pylab
import pandas as pd

# Load data
snp_reader = Bed("Z:/PrimedPlant_Plant2030/vcf/Concatenate_Hapmap_EC_iSelect_GBS_198GT_493846SNP.bed", count_A1=True)
pheno= Pheno("Z:/PrimedPlant_Plant2030/Phenotypes/BPS_res_Priming_effect_SL.csv")

#snp_reader = Bed('all.bed', count_A1=True)
#pheno = Pheno("pheno_10_causals.txt")



#snp_reader = Bed('C:/gwas_test_data/test/vcf2gwas/example.bed', count_A1=True)
#pheno = Pheno("C:/gwas_test_data/test/vcf2gwas/pheno_gp.csv")

#snp_reader = Bed('C:/gwas_test_data/test/WGS300_005_0020.bed', count_A1=True)
#pheno = Pheno("C:/gwas_test_data/test/bridge_random.csv")
#pheno = Pheno("C:/gwas_test_data/test/bridge_row_type.txt")



# KFold setup
n_splits = 5
kf = KFold(n_splits=n_splits)

# Prepare to collect results
results = []
counter = 1
# Start cross-validation
for train_indices, test_indices in kf.split(range(snp_reader.iid_count)):
    # Split data into training and testing

    train = snp_reader[train_indices, :]
    test = snp_reader[test_indices, :]

    # Train the model
    fastlmm = FastLMM(GB_goal=2)
    fastlmm.fit(K0_train=train, y=pheno)

    # Test the model
    mean, covariance = fastlmm.predict(K0_whole_test=snp_reader)
    df = pd.DataFrame({'Column1': mean.val[:, 0], 'Column2': mean.iid[:, 0]})
    df.to_csv(str(counter) + '_lmm_gp_priming2.csv', index=False)
    counter += 1
    print(df)

    # Evaluate the model (e.g., calculating some metrics)
    # actual_pheno = pheno[pheno.iid_to_index(mean.iid), :].read()
    #
    # # Here you might want to calculate some metric between actual_pheno.val and mean.val
    # # and append it to results list
    # # For example: results.append(some_metric_function(actual_pheno.val, mean.val))
    #
    # # Optionally, plot results for each fold
    # pylab.plot(actual_pheno.val, "r.")
    # pylab.plot(mean.val, "b.")
    # pylab.errorbar(np.arange(mean.iid_count), mean.val[:, 0], yerr=np.sqrt(np.diag(covariance.val)), fmt='.')
    # pylab.xlabel('Testing examples')
    # pylab.ylabel('Phenotype, actual (red) and predicted (blue with stdev)')
    # pylab.show()

# After the loop, aggregate your results for overall performance metrics
# For example, mean_result = np.mean(results)