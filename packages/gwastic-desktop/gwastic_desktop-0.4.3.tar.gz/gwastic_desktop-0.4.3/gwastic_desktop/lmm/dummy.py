import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor

def prepare_data():

    s_data = np.load('snp.npy')
    s_data[np.isnan(s_data)] = -1
    labels = np.load('pheno.npy')

    # Concatenate the labels and s_data horizontally
    combined_data = np.hstack((labels, s_data))

    # Write the data to a CSV file
    with open('data_bridge.csv', 'w') as file:
        # Write the header
        file.write("ID,label,snp\n")

        for i, row in enumerate(combined_data, start=1):
            # Convert nan to 'np.nan' and other values to their string representation
            values = ["np.nan" if np.isnan(val) else str(val) for val in row]

            # Join the values with a comma and write to the file
            file.write("{},{}\n".format(i, '\t'.join(values)))
def run_tree():
    snp_data = np.load('snp.npy')
    print (snp_data)
    snp_data[np.isnan(snp_data)] = -1
    phenotype_labels = np.load('pheno.npy')

    #print (phenotype_labels)
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(snp_data, phenotype_labels, test_size=0.2, random_state=42)

    # Standardize the input features (optional but recommended)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Define and train an XGBoost model
    # xgboost1
    #xgb_model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)

    xgb_model = RandomForestRegressor(n_estimators=100, random_state=42)
    # xgboost2
    # xgb_model = xgb.XGBRegressor(n_estimators=25,
    #                                   max_depth=20,
    #                                   min_child_weight=10,
    #                                   subsample=0.8,
    #                                   eta=0.3,
    #                                   colsample_bytree=0.7)
    # Fit the model to the training data
    xgb_model.fit(X_train, y_train)

    # Evaluate the model on the test set
    test_predictions = xgb_model.predict(X_test)
    test_loss = np.mean((test_predictions - y_test)**2)  # Mean squared error
    print(f'Test Loss: {test_loss}')
    f = open('out_rf_bridge2.txt', 'w')

    #feature_list = open('C:/gwas_test_data/test/' + "WGS300_005_0020.bim", 'r')
    #feature_list = [line.rstrip() for line in feature_list.readlines()]
    df = pd.read_csv('C:/gwas_test_data/test/' + "WGS300_005_0020.bim", delimiter='\t')
    feature_list = df.iloc[:, 1].tolist()
    print (feature_list)
    for col, score in zip(feature_list, xgb_model.feature_importances_):
        f.write(str(col) + ' ' + str(score) + '\n')


def plot():
    df = pd.read_csv('out_rf_bridge2.txt', delimiter=' ', header=None)
    #df = pd.read_csv('C:/Users/lueck/PycharmProjects/genbank2/test/_out_nn_bridge100.txt', delimiter=' ', header=None)

    df.columns = ['snp', 'value']
    #print (df.dtypes)
    #print(df)
    #

    #ax1 = df.plot.scatter(x='value',
                        #  y='snp')
    #plt.savefig('out_xgboos_bridge.png')
    feature_list = df['value'].to_numpy()
    plt.plot(feature_list)
    df = df.sort_values(by=['value'], ascending=False)
    print (df)
    plt.show()
    #print (feature_list)
    #plt.axhline(y=feature_list, color='b', linestyle='--')
    # plt.ylabel('saliency value', fontdict=None, labelpad=None, fontsize=15)
    #
    # plt.xlabel('SNPs', fontdict=None, labelpad=None, fontsize=15)
    #
    #plt.savefig('sal.png')
    #

    # print (len(xgb_model.feature_importances_))
    # xgb.plot_importance(xgb_model, max_num_features=20)
    # plt.rcParams['figure.figsize'] = [50, 50]
    # plt.savefig('rf.png')

def gp_lmm():
    import pylab
    from pysnptools.snpreader import Pheno, Bed
    from fastlmm.inference import FastLMM
    import numpy as np
    from fastlmm.util import example_file  # Download and return local file name

    # define file names
    #bed_fn = example_file()
    #snp_reader = Bed('all.bed', count_A1=True)
    snp_reader = Bed("Z:/PrimedPlant_Plant2030/vcf/Concatenate_Hapmap_EC_iSelect_GBS_198GT_493846SNP.bed", count_A1=True)
    #pheno_fn = example_file()
    #pheno_fn = Pheno("pheno_10_causals.txt")
    pheno_fn = Pheno("Z:/PrimedPlant_Plant2030/Phenotypes/BPS_res_Priming_effect_SL.csv")
    #cov_fn = example_file("tests/datasets/synth/cov.txt")

    seed = None  # set to None to get a new seed each time
    rng = np.random.default_rng(seed=seed)

    test_indices = rng.choice(snp_reader.iid_count, 50, replace=False)
    #print (len(test_indices))
    train_indices = list(set(range(snp_reader.iid_count)) - set(test_indices))
    train = snp_reader[train_indices, :]
    test = snp_reader[test_indices, :]

    #print (len(train.iid))
    #train = snp_reader[:-60, :]
    #test = snp_reader[-60:, :]


    #print (pheno_fn[-10:, :])

    # In the style of scikit-learn, create a predictor and then train it.
    fastlmm = FastLMM(GB_goal=2)
    fastlmm.fit(K0_train=train, y=pheno_fn)

    # Now predict with it
    mean, covariance = fastlmm.predict(K0_whole_test=test)
    df = pd.DataFrame({'Column1': mean.val[:, 0], 'Column2': mean.iid[:, 0]})

    print(df)

    #print("Predicted means and stdevs")
    #print(mean.val[:, 0])
    #print(mean.iid[:, 0])
    #print(np.sqrt(np.diag(covariance.val)))

    # Plot actual phenotype and predicted phenotype
   # whole_pheno = Pheno("pheno_10_causals.txt")
    whole_pheno = Pheno("Z:/PrimedPlant_Plant2030/Phenotypes/BPS_res_Priming_effect_SL.csv")
    actual_pheno = whole_pheno[whole_pheno.iid_to_index(mean.iid), :].read()
    #print (actual_pheno.iid)
    pylab.plot(actual_pheno.val, "r.")
    pylab.plot(mean.val, "b.")
    pylab.errorbar(np.arange(mean.iid_count),mean.val[:,0],yerr=np.sqrt(np.diag(covariance.val)),fmt='.')
    pylab.xlabel('testing examples')
    pylab.ylabel('phenotype, actual (red) and predicted (blue with stdev)')
    pylab.show()

gp_lmm()
#un_tree()
# #plot()
#
# import pandas as pd
#
# data = np.array([['7514 7514'],
#         ['7521 7521'],
#         ['7525 7525']])
#
# # Convert the data to a DataFrame with a single column
# df = pd.DataFrame([data], columns=['Combined'])
# print (df)
# # Split the 'Combined' column into two separate columns
# df['Column1'] = df['Combined'].str.slice(0, 4)
# df['Column2'] = df['Combined'].str.slice(4, 8)
#
# # Drop the 'Combined' column
# df.drop('Combined', axis=1, inplace=True)
#
# print(df)