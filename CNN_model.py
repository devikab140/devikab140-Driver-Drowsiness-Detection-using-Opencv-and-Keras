import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Define a simple CNN model
def create_drowsiness_model(input_shape):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy'])
    return model

def evaluate_model(model, test_generator):
    predictions = model.predict(test_generator)
    y_true = test_generator.classes
    y_pred = np.round(predictions).flatten()

    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', xticklabels=['Awake', 'Drowsy'], yticklabels=['Awake', 'Drowsy'])
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

    print(classification_report(y_true, y_pred))

# Train the model with a real image dataset
def train_model():
    train_data_dir = 'C:/Users/balan/M.sc/First year/SET paper/Project/project/dataset_new/train/'  
    test_data_dir = 'C:/Users/balan/M.sc/First year/SET paper/Project/project/dataset_new/test/'   
    input_shape = (24, 24, 3)
    model = create_drowsiness_model(input_shape)

    # Data augmentation for the training set
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    # Data augmentation for the test set (only rescaling)
    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(24, 24),
        batch_size=32,
        class_mode='binary'
    )

    test_generator = test_datagen.flow_from_directory(
        test_data_dir,
        target_size=(24, 24),
        batch_size=32,
        class_mode='binary'
    )

    print("Number of training samples:", len(train_generator.filenames))
    print("Number of testing samples:", len(test_generator.filenames))

    # Save the best model during training
    checkpoint = ModelCheckpoint('best_model.h5', monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)

    # Train the model
    model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // 32,
        epochs=10,
        validation_data=test_generator,
        validation_steps=test_generator.samples // 32,
        callbacks=[checkpoint]
    )

    # Save the trained model
    model.save('C:/Users/balan/M.sc/First year/SET paper/Project/project/CNN_model.h5')
    
    evaluate_model(model, test_generator)

if __name__ == "__main__":
    train_model()
