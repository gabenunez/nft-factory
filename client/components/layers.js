import ImageReel from '../components/imageReel';
import { arrayMoveImmutable } from 'array-move';

function Layers({ selectedImages, setSelectedImages }) {
  function moveLayerUp(currentLayerIndex) {
    setSelectedImages(arrayMoveImmutable(selectedImages(currentLayerIndex, currentLayerIndex + 1)));
  }

  function moveLayerDown(currentLayerIndex) {}

  return (
    <div className="mb-3 mt-3">
      {selectedImages.map((imageSet, index) => {
        return (
          <div key={index}>
            <ImageReel
              imageSet={imageSet}
              setImageSet={(newImageSetValue) => {
                const selectedImageCopy = [...selectedImages];
                selectedImageCopy[index] = { ...newImageSetValue };
                setSelectedImages(selectedImageCopy);
              }}
              currentLayerPosition={index}
              totalLayers={selectedImages.length}
              moveLayerUp={() =>
                setSelectedImages(arrayMoveImmutable(selectedImages, index, index - 1))
              }
              moveLayerDown={() =>
                setSelectedImages(arrayMoveImmutable(selectedImages, index, index + 1))
              }
            />
          </div>
        );
      })}
    </div>
  );
}

export default Layers;
