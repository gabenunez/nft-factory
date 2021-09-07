import { useState, useEffect } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import styles from '../styles/ImageReels.module.css';
import { useDropzone } from 'react-dropzone';
import OnImagesLoaded from 'react-on-images-loaded';
import { BsPencil, BsArrowDown, BsArrowUp } from 'react-icons/bs';
import { MdRemoveCircle } from 'react-icons/md';

function ImageReel({
  imageSet,
  setImageSet,
  currentLayerPosition,
  totalLayers,
  moveLayerUp,
  moveLayerDown
}) {
  const [imagePreviews, setImagePreviews] = useState([]);
  const { images: currentImages, name: layerName } = imageSet;

  const { acceptedFiles, getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: '.png',
    maxSize: 1000000,
    noClick: currentImages.length > 0,
    onDrop: (acceptedFiles) => {
      // Add attributeName as a default file property
      acceptedFiles.forEach((file) => {
        file.attributeName = '';
        file.previewUrl = URL.createObjectURL(file);
      });
      setImageSet({ ...imageSet, images: [...currentImages, ...acceptedFiles] });
    }
  });

  useEffect(() => {
    setImagePreviews(
      currentImages.map((image) => {
        return URL.createObjectURL(image);
      })
    );
  }, [imageSet.images]);

  function setLayerName(event) {
    setImageSet({ ...imageSet, name: event.target.value });
  }

  function removeImageFromReel(imgIndex) {
    setImageSet({ ...imageSet, images: currentImages.filter((_, i) => i !== imgIndex) });
  }

  function modifyAttributeName(imgIndex, newValue) {
    const imageSetCopy = { ...imageSet };
    imageSetCopy.images[imgIndex].attributeName = newValue;
    setImageSet(imageSetCopy);
  }

  return (
    <div>
      <Row className="mb-2">
        <Col className="d-flex align-items-end">
          <input
            className={styles.layerInput}
            type="text"
            value={layerName}
            onChange={setLayerName}
            placeholder="Layer name"
          />
          <BsPencil color="#989898" />
        </Col>

        {totalLayers > 1 && (
          <Col className="d-flex align-items-end" xs="auto">
            <button
              disabled={currentLayerPosition === totalLayers - 1}
              aria-label="Move layer down"
              className={styles.layerDirection}
              onClick={moveLayerDown}
            >
              <BsArrowDown size={20} />
            </button>

            <button
              disabled={currentLayerPosition === 0}
              aria-label="Move layer up"
              className={styles.layerDirection}
              onClick={moveLayerUp}
            >
              <BsArrowUp size={20} />
            </button>
          </Col>
        )}
      </Row>

      <div className={`${styles.imageReelContainer} d-flex mb-3`}>
        <div
          {...getRootProps({
            className: `w-100 ${!isDragActive && !currentImages.length && 'd-flex'}`
          })}
        >
          <input {...getInputProps()} />

          {!isDragActive && !currentImages.length && (
            <Col className="d-flex justify-content-center align-items-center">
              <p>Drop images here (1mb max, .png only)</p>
            </Col>
          )}

          {imagePreviews.map((imageSrc, index) => (
            <div key={'image-preview' + index} className={styles.reelImageWrapper}>
              <button
                onClick={() => removeImageFromReel(index)}
                aria-label="Remove image"
                className={styles.removeImageButton}
              >
                <MdRemoveCircle size={20} color="#ce1010" />
              </button>
              <OnImagesLoaded
                onLoaded={() => {
                  // Prevent memory leaks by removing the local blob after image loaded
                  URL.revokeObjectURL(imageSrc);
                }}
              >
                <img className={`img-fluid ${styles.imageReelImage}`} src={imageSrc} />
              </OnImagesLoaded>

              {imageSet.images[index] && (
                <input
                  className={styles.imageNameInput}
                  type="text"
                  value={imageSet.images[index].attributeName}
                  onChange={(event) => modifyAttributeName(index, event.target.value)}
                  placeholder={`Attribute name #${index + 1}`}
                />
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ImageReel;
