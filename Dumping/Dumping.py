
# coding: utf-8

# # Find Dumping Offers

# ## Observations:
# - For the same model, pvp varies (depending on configuration I guess)
# - Average difference between pvp and cash-price varies among brand and model
# - Some brands are underrepresanted, like Audi (only 2 samples)
# 
# ## Actions:
# - Taking the ratio (pvp-cashprice)/pvp = dump_value instead of only difference for normalizing. This value is between 0 and 1
# - Calculate z-score per brand and per model
# - Discarding brands that made less than 10 offers

# ## Load Packages

# In[3]:

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # Plotting
import numpy as np
import re # regular expressions --> Finding Postal Code
#from datetime import datetime


# ## Read Data

# In[2]:

data = pd.read_csv('Dumping.csv', delimiter = ',', skiprows=0, squeeze=False, skip_blank_lines=True, index_col=None)
#data


# ## Discard brands with less than 10 offers

# In[4]:

def brandNumber(brand):
    return brand, len(data[data.brand==brand])


# In[6]:

# Get all unique brands and models
brand_names = np.unique(np.asarray(data.brand[:]))
model_names = np.unique(np.asarray(data.model[:]))


# In[27]:

# discard brands with less than 10 offers
print 'Before Dropping: {} entries'.format(len(data))
brandNumbers = map(brandNumber, brand_names)
for nr in brandNumbers:
    if nr[1] <= 10:
        data = data[data.brand != nr[0]]
        print '{} dropped'.format(nr[0])
print 'After Dropping: {} entries'.format(len(data))
brand_names = np.unique(np.asarray(data.brand[:]))
model_names = np.unique(np.asarray(data.model[:]))


# ## Calculate mean and std of dump-value (pvp-cashprize/pvp) per model and brand

# In[16]:

def brandDifferences(brand):
    differences = []
    for offer in data[data.brand==brand].iterrows():
        differences.append((offer[1].pvp_build-offer[1].cash_price)/offer[1].pvp_build)
    return (brand, np.mean(differences), np.std(differences))

def modelDifferences(model):
    differences = []
    for offer in data[data.model==model].iterrows():
        differences.append((offer[1].pvp_build-offer[1].cash_price)/offer[1].pvp_build)
    brand = data[data.model==model].iloc[0].brand
    return (model, brand, np.mean(differences), np.std(differences))


# In[28]:

# For each brand/model, calculate dumping-values mean and std
brands = map(brandDifferences, brand_names)
models = map(modelDifferences, model_names)


# In[30]:

# Convert to numpy array for later operations
brands_np = np.asarray(brands)
models_np = np.asarray(models)


# In[34]:

# Sort by mean dump-value to draw conclusions
brands_sorted = sorted(brands, key = lambda x: -x[1])
models_sorted = sorted(models, key = lambda x: -x[2])


# Opel offers in average 19% under pvp and Dacia 3% over pvp ! <br>
# The model with the best relative offers is the S60 from Volvo with 33% under pvp. <br>
# The model with the worst relative offers is Mercedes-Benz Clase S with 183% over pvp ! <br>

# ## For each offer, calculate z-score (how many stds is the dumping_value away from mean)

# In[49]:

def zscore(offer, brands_np, models_np):
    # Calculate z-score for each offer, based on the mean and std from its brand and model
    # negative z-scores are below average offers and positive z-scores are above average offers
    dumpv_offer = (offer[1].pvp_build-offer[1].cash_price)/offer[1].pvp_build
    dumpv_model = models_np[models_np[:,0]==offer[1].model][0,2:]
    dumpv_brand = brands_np[brands_np[:,0]==offer[1].brand][0,1:]
    if float(dumpv_model[1])!=0:
        #zscore = (dumpv_offer - dumpv_model)/std_model
        zscore_model = (dumpv_offer-float(dumpv_model[0]))/float(dumpv_model[1])
    else: zscore_model = 0
    if dumpv_brand[1] !=0:
        zscore_brand = (dumpv_offer-float(dumpv_brand[0]))/float(dumpv_brand[1])
    else: zscore_brand = 0
    return dumpv_offer, zscore_model, zscore_brand


# In[50]:

# Calculate z-score per model and brand and add it for each offer to the data-frame
# positive z-score represent really low offers
dumping_values = []
zscores_model = []
zscores_brand = []
for offer in data.iterrows():
        dumping_values.append((offer[1].pvp_build-offer[1].cash_price)/offer[1].pvp_build)
        scores = zscore(offer, brands_np, models_np)
        dumping_values.append(scores[0])
        zscores_model.append(scores[1])
        zscores_brand.append(scores[2])
zscores_brand = np.asarray(zscores_brand)
zscores_model = np.asarray(zscores_model)

# Add Columns to data-frame
data.loc[:, 'zscore_model'] = pd.Series(zscores_model, index=data.index)
data.loc[:, 'zscore_brand'] = pd.Series(zscores_brand, index=data.index)


# ## Visualize z-score distribution with histogram

# ### Based on brand

# In[63]:

# Histogram for all offers, based on brand-z-score
plt.hist(zscores_brand, bins=20)
plt.xlabel('z-score')
plt.ylabel('# offers')
plt.show()
print '# Total Samples: {}'.format(len(zscores_brand))
print ('zscore > 2: Classify {}% as Dumping offers'
       .format(100*float(len(zscores_brand[zscores_brand>2]))/len(zscores_brand)))
print ('zscore > 3: Classify {}% as Dumping offers'
       .format(100*float(len(zscores_brand[zscores_brand>3]))/len(zscores_brand)))


# ### Based on Model

# In[61]:

# Histogramm for all offers, based on model-z-score
plt.hist(zscores_model, bins=20)
plt.xlabel('z-score')
plt.ylabel('# offers')
plt.show()
print '# Total Samples: {}'.format(len(zscores_model))
print ('zscore > 2: Classify {}% as Dumping offers'
       .format(100*float(len(zscores_model[zscores_model>2]))/len(zscores_model)))
print ('zscore > 3: Classify {}% as Dumping offers'
       .format(100*float(len(zscores_model[zscores_model>3]))/len(zscores_model)))


# ## Select the possible dumping offers, taking into account brand and model z-score

# In[59]:

# Show the offers, that have a model z-score below -6 and brand z-score below -5
DUMPINGS = data[data.zscore_model>(2)]
DUMPINGS = DUMPINGS[DUMPINGS.zscore_brand>(2)]
print '\n {}% of all offers were classified as dumpings \n'.format(100*float(len(DUMPINGS))/len(data))
DUMPINGS


# ## From Dumping offers, get the car-dealerships

# In[67]:

dumping_dealers = np.unique(np.asarray(DUMPINGS.showroom_id))
dumping_dealers

