# Local setup
import BiLSTMAvg_old.functions as fun
import numpy as np
import tensorflow as tf
import BiLSTMAvg_old.model as model1

dataPath="."
batch_size=64
onGPU=False
epochs=10
dataset="outFile_pre.tsv"

# Reading data
exec(open('./functions.py').read())
embeddings=fun.readEmbeddings(dataPath+"/GoogleNewsUnigrams.txt")
MAX_SEQUENCE_LENGTH=120
MAX_DOCUMENT_LENGTH=50
(labels,sources,nums,wordsL,contents,documentCV,topicCV,sourceCV,lengthD)=fun.readDocuments(dataPath+"/"+dataset,MAX_SEQUENCE_LENGTH,embeddings,MAX_DOCUMENT_LENGTH)
embeddingMatrix=fun.prepareEmbeddings(embeddings,wordsL)

# Converting to numpy
y=np.asarray(labels,dtype='float32')
allY=np.concatenate((np.expand_dims(1-y,1),np.expand_dims(y,1)),axis=1)
allX=np.array(contents)

# Load models
exec(open('./model.py').read())

# Prepare CV scenarios
documentCV=np.asarray(documentCV,dtype='int32')
topicCV=np.asarray(topicCV,dtype='int32')
sourceCV=np.asarray(sourceCV,dtype='int32')
scenarioCV=sourceCV

result=np.array([[-1,-1]]*len(scenarioCV),dtype='float32')
for folda in range(max(scenarioCV)):
	fold=folda+1
	print("Evaluating on fold "+str(fold)+"...")
	whichTest=np.isin(scenarioCV,fold)
	trainY=allY[~whichTest,]
	develY=allY[whichTest,]
	trainX=allX[~whichTest,]
	develX=allX[whichTest,]
	style1=model1.Style1(embeddingMatrix,2,MAX_SEQUENCE_LENGTH,MAX_DOCUMENT_LENGTH,onGPU)
	mask=style1.getMask(lengthD)
	trainM=np.array(mask)[~whichTest]
	develM=np.array(mask)[whichTest]
	model=style1.getModel()
	model.compile(optimizer=tf.train.AdamOptimizer(),loss="binary_crossentropy",metrics=["accuracy"])
	fit=model.fit([trainX,trainM],trainY, epochs=epochs,validation_data=([develX,develM],develY),batch_size=batch_size)
	predictions=model.predict([develX,develM])
	model.save('my_model.h5')
	result[whichTest,:]=predictions

fun.evaluateD(result,allY)

