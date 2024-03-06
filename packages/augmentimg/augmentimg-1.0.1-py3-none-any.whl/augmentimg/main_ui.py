from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QFileDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QGridLayout)
import sys
import os
from torchvision import transforms
from PIL import Image


def get_transform(selected_augmentations):
        transformations = []
        # Basic transformations
        if selected_augmentations.get('rotation'):
            transformations.append(transforms.RandomRotation(degrees=(0, 360)))
        if selected_augmentations.get('flip'):
            transformations.append(transforms.RandomHorizontalFlip())
            transformations.append(transforms.RandomVerticalFlip())
        if selected_augmentations.get('blur'):
            transformations.append(transforms.GaussianBlur(5))
        if selected_augmentations.get('saturation'):
            transformations.append(transforms.ColorJitter(saturation=2))
        
        # Advanced transformations
        if selected_augmentations.get('contrast'):
            transformations.append(transforms.ColorJitter(contrast=2))
        if selected_augmentations.get('sharpness'):
            transformations.append(transforms.RandomAdjustSharpness(2))
        if selected_augmentations.get('random_crop'):
            transformations.append(transforms.RandomResizedCrop(224))
        if selected_augmentations.get('random_erase'):
            transformations.append(transforms.RandomErasing())
        if selected_augmentations.get('affine'):
            transformations.append(transforms.RandomAffine(degrees=(0, 360)))

        # Additional transformations
        if selected_augmentations.get('grayscale'):
            transformations.append(transforms.RandomGrayscale())
        if selected_augmentations.get('perspective'):
            transformations.append(transforms.RandomPerspective())
        if selected_augmentations.get('color_jitter'):
            transformations.append(transforms.ColorJitter())
        if selected_augmentations.get('equalize'):
            transformations.append(transforms.RandomEqualize())
        if selected_augmentations.get('invert'):
            transformations.append(transforms.RandomInvert())

        transform = transforms.Compose(transformations)
        return transform
def augment_image(image_path, save_dir, transform, count):
        image = Image.open(image_path)
        augmented_image = transform(image)
        save_path = os.path.join(save_dir, f'aug_{count}_{os.path.basename(image_path)}')
        augmented_image.save(save_path)


def augment_images_in_folder(folder_path, total_desired_images, selected_augmentations):
        original_images = [img for img in os.listdir(folder_path) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]
        num_original_images = len(original_images)
        if num_original_images == 0:
            raise Exception("No images found in the folder.")

        augmentations_needed = total_desired_images - num_original_images
        if augmentations_needed <= 0:
            raise Exception("The folder already contains the desired number of images or more.")

        save_dir = os.path.join(folder_path, 'augmented')
        os.makedirs(save_dir, exist_ok=True)

        transform = get_transform(selected_augmentations)

        for count in range(augmentations_needed):
            image_name = original_images[count % num_original_images]
            image_path = os.path.join(folder_path, image_name)
            augment_image(image_path, save_dir, transform, count)

class ImageAugmentationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selectedFolder = ''
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Image Augmentation Tool')
        self.setGeometry(100, 100, 800, 600)
        mainLayout = QVBoxLayout()

        # Label to show the selected directory and image count
        self.labelDirectory = QLabel('Select an image directory')
        mainLayout.addWidget(self.labelDirectory)
        
        self.labelCount = QLabel('Image Count: 0')
        mainLayout.addWidget(self.labelCount)

        # Horizontal layout for folder selection
        directoryLayout = QHBoxLayout()
        self.btnSelectFolder = QPushButton('Select Folder', self)
        self.btnSelectFolder.clicked.connect(self.openFolderDialog)
        directoryLayout.addWidget(self.btnSelectFolder)
        mainLayout.addLayout(directoryLayout)

        # Horizontal layout for desired image count input
        countLayout = QHBoxLayout()
        self.labelDesiredCount = QLabel('Desired Image Count:')
        countLayout.addWidget(self.labelDesiredCount)
        self.inputDesiredCount = QLineEdit(self)
        countLayout.addWidget(self.inputDesiredCount)
        mainLayout.addLayout(countLayout)

        # Grid layout for checkboxes
        gridLayout = QGridLayout()
        self.addAugmentationCheckboxes(gridLayout)
        mainLayout.addLayout(gridLayout)

        # Augment Images button
        self.btnAugmentImages = QPushButton('Augment Images', self)
        self.btnAugmentImages.clicked.connect(self.augmentImages)
        mainLayout.addWidget(self.btnAugmentImages)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

    def addAugmentationCheckboxes(self, layout):
        # First column
        self.cbRotation = QCheckBox('Rotation', self)
        layout.addWidget(self.cbRotation, 0, 0)
        self.cbFlip = QCheckBox('Flip', self)
        layout.addWidget(self.cbFlip, 1, 0)
        self.cbBlur = QCheckBox('Blur', self)
        layout.addWidget(self.cbBlur, 2, 0)
        self.cbSaturation = QCheckBox('Saturation', self)
        layout.addWidget(self.cbSaturation, 3, 0)
        self.cbContrast = QCheckBox('Contrast', self)
        layout.addWidget(self.cbContrast, 4, 0)
        self.cbSharpness = QCheckBox('Sharpness', self)
        layout.addWidget(self.cbSharpness, 5, 0)
        self.cbRandomCrop = QCheckBox('Random Crop', self)
        layout.addWidget(self.cbRandomCrop, 6, 0)

        # Second column
        self.cbRandomErase = QCheckBox('Random Erase', self)
        layout.addWidget(self.cbRandomErase, 0, 1)
        self.cbAffine = QCheckBox('Affine Transformations', self)
        layout.addWidget(self.cbAffine, 1, 1)
        self.cbGrayscale = QCheckBox('Random Grayscale', self)
        layout.addWidget(self.cbGrayscale, 2, 1)
        self.cbPerspective = QCheckBox('Random Perspective', self)
        layout.addWidget(self.cbPerspective, 3, 1)
        self.cbColorJitter = QCheckBox('Color Jitter', self)
        layout.addWidget(self.cbColorJitter, 4, 1)
        self.cbEqualize = QCheckBox('Equalize', self)
        layout.addWidget(self.cbEqualize, 5, 1)
        self.cbInvert = QCheckBox('Invert', self)
        layout.addWidget(self.cbInvert, 6, 1)

    def openFolderDialog(self):
        self.selectedFolder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if self.selectedFolder:
            self.labelDirectory.setText(f'Selected Folder: {self.selectedFolder}')
            self.updateImageCount()

    def updateImageCount(self):
        image_files = [img for img in os.listdir(self.selectedFolder) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]
        self.labelCount.setText(f'Image Count: {len(image_files)}')

    def getSelectedAugmentations(self):
        selected_augmentations = {
            'rotation': self.cbRotation.isChecked(),
            'flip': self.cbFlip.isChecked(),
            'blur': self.cbBlur.isChecked(),
            'saturation': self.cbSaturation.isChecked(),
            'contrast': self.cbContrast.isChecked(),
            'sharpness': self.cbSharpness.isChecked(),
            'random_crop': self.cbRandomCrop.isChecked(),
            'random_erase': self.cbRandomErase.isChecked(),
            'affine': self.cbAffine.isChecked(),
            'grayscale': self.cbGrayscale.isChecked(),
            'perspective': self.cbPerspective.isChecked(),
            'color_jitter': self.cbColorJitter.isChecked(),
            'equalize': self.cbEqualize.isChecked(),
            'invert': self.cbInvert.isChecked()
        }
        return selected_augmentations

    def augmentImages(self):
        if not self.selectedFolder or self.selectedFolder.startswith('Select an image directory'):
            self.labelDirectory.setText('Please select a folder first.')
            return

        try:
            desired_count = int(self.inputDesiredCount.text())
            selected_augmentations = self.getSelectedAugmentations()

            self.labelDirectory.setText('Loading...')
            QApplication.processEvents()

            augment_images_in_folder(self.selectedFolder, desired_count, selected_augmentations)

            self.labelDirectory.setText(f'Images have been augmented. Check the "augmented" folder within {self.selectedFolder}.')
            self.updateImageCount()
        except ValueError:
            self.labelDirectory.setText('Please enter a valid number for desired image count.')
        except Exception as e:
            self.labelDirectory.setText(f'Error during augmentation: {e}')

def main():
    app = QApplication(sys.argv)
    ex = ImageAugmentationApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
