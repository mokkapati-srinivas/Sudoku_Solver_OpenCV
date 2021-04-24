from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Dense,Flatten
from keras.utils import np_utils


def get_data():
    
    (x_train,y_train),(x_test,y_test)=mnist.load_data()
    
    #print(x_train.shape)
    #Now we have to reshape the data
    x_train=x_train.reshape(x_train.shape[0],28,28,1).astype("float32")
    x_test=x_test.reshape(x_test.shape[0],28,28,1).astype("float32")
    
    #We convert the numbers to binary representations.
    #Example 0 is represented as [1,0,0,0,0,0,0,0,0,0]
    y_train=np_utils.to_categorical(y_train)
    y_test=np_utils.to_categorical(y_test)
    
    #print(y_train[0])
    
    #Now we convert the intensities of integers to floats
    x_train=x_train.astype("float32")
    x_test=x_test.astype("float32")
    
    #Now normalize them by dividing them by 255
    #Since max is 255. So range becomes 0-1
    x_train=x_train/255
    x_test=x_test/255
    
    
    return x_train,y_train,x_test,y_test


def build_model():
    
    #Specifying the model as sequential
    model=Sequential()
    
    #Building the model layer by layer
    model.add(Conv2D(32,(3,3),activation="relu",kernel_initializer="he_uniform",input_shape=(28,28,1)))
    model.add(MaxPooling2D((2,2)))
    model.add(Conv2D(32,(3,3),activation="relu",kernel_initializer="he_uniform"))
    model.add(Conv2D(32,(3,3),activation="relu",kernel_initializer="he_uniform"))
    model.add(MaxPooling2D((2,2)))
    model.add(Flatten())
    model.add(Dense(100,activation="relu",kernel_initializer="he_uniform"))
    model.add(Dense(10,activation="softmax"))
    
    #compile the model
    model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=["accuracy"])
    
    return model


def save_model_and_get_accuracy():
    
    #get the mnist data
    x_train,y_train,x_test,y_test=get_data()
    
    #Get the builded model
    model=build_model()
    
    #Start training the model using x_train,y_train
    model.fit(x_train,y_train,epochs=10)
    
    #evaluate and get the accuracy
    loss,accuracy=model.evaluate(x_test,y_test)
    #print(accuracy*100)
    
    model.save("model_digit_recognition.h5")


save_model_and_get_accuracy()