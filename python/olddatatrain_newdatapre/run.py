# Local setup
import BiLSTMAvg_co.functions as fun
import numpy as np
import tensorflow as tf
import BiLSTMAvg_co.model as model1
import pandas as pd

dataPath="."
batch_size=64
onGPU=False
epochs=10
dataset="outFile.tsv"
dataset_1="outFile_integration.tsv"

# Reading data
exec(open('./functions.py').read())
embeddings=fun.readEmbeddings(dataPath+"/GoogleNewsUnigrams.txt")
MAX_SEQUENCE_LENGTH=120
MAX_DOCUMENT_LENGTH=50
(labels,sources,nums,wordsL,contents,documentCV,topicCV,sourceCV,lengthD)=fun.readDocuments(dataPath+"/"+dataset,MAX_SEQUENCE_LENGTH,embeddings,MAX_DOCUMENT_LENGTH)
(labels_1,sources_1,nums_1,wordsL_1,contents_1,documentCV_1,topicCV_1,sourceCV_1,lengthD_1)=fun.readDocuments(dataPath+"/"+dataset_1,MAX_SEQUENCE_LENGTH,embeddings,MAX_DOCUMENT_LENGTH)
embeddingMatrix=fun.prepareEmbeddings(embeddings,wordsL)
embeddingMatrix_1=fun.prepareEmbeddings(embeddings,wordsL_1)

# Converting to numpy
y=np.asarray(labels,dtype='float32')
y_1=np.asarray(labels_1,dtype='float32')
allY=np.concatenate((np.expand_dims(1-y,1),np.expand_dims(y,1)),axis=1)
allY_1=np.concatenate((np.expand_dims(1-y_1,1),np.expand_dims(y_1,1)),axis=1)
allX=np.array(contents)
allX_1=np.array(contents_1)

# Load models
exec(open('./model.py').read())

# Prepare CV scenarios
# documentCV=np.asarray(documentCV,dtype='int32')
# topicCV=np.asarray(topicCV,dtype='int32')
sourceCV=np.asarray(sourceCV,dtype='int32')
scenarioCV=sourceCV
sourceCV_1=np.asarray(sourceCV_1,dtype='int32')
scenarioCV_1=sourceCV_1
result=np.array([[-1,-1]]*len(scenarioCV_1),dtype='float32')
fold=4
# print("Evaluating on fold "+str(fold)+"...")
whichTest=np.isin(scenarioCV,fold)
trainY=allY[~whichTest,]
develY=allY[whichTest,]
trainX=allX[~whichTest,]
develX=allX[whichTest,]
style1=model1.Style1(embeddingMatrix,2,MAX_SEQUENCE_LENGTH,MAX_DOCUMENT_LENGTH,onGPU)
mask=style1.getMask(lengthD)
mask_1=style1.getMask(lengthD_1)
trainM=np.array(mask)[~whichTest]
develM=np.array(mask)[whichTest]
model=style1.getModel()
model.compile(optimizer=tf.train.AdamOptimizer(),loss="binary_crossentropy",metrics=["accuracy"])
fit=model.fit([trainX,trainM],trainY, epochs=epochs,validation_data=([develX,develM],develY),batch_size=batch_size)
testX=allX_1
testY=allY_1
testM=np.array(mask_1)
predictions=model.predict([testX,testM])
result=predictions




print(result)
# 创建一个字典，字典的键是列名，值是列的数据
df = pd.DataFrame()
df['num'] = nums_1
df['label'] = labels_1
df['predicton'] = result[:, 1]

df.to_csv('result_integration.csv', index=False, encoding='utf-8-sig')

fun.evaluateD(result,allY_1)
print(fun.evaluateD(result,allY_1))

