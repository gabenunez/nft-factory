import { useState, useEffect } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import styles from '../styles/ImageReels.module.css';
import { useDropzone } from 'react-dropzone';
import OnImagesLoaded from 'react-on-images-loaded';
import { BsPencil } from 'react-icons/bs';

function ImageReel({ imageSet, setImageSet }) {
  const [imagePreviews, setImagePreviews] = useState([]);
  const { images: currentImages, name: layerName } = imageSet;

  const { acceptedFiles, getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: '.png',
    maxSize: 1000000,
    noClick: currentImages.length > 0,
    onDrop: (acceptedFiles) =>
      setImageSet({ ...imageSet, images: [...currentImages, ...acceptedFiles] })
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

  return (
    <div>
      <div>
        <Row className="mb-2">
          <Col className="d-flex align-items-end">
            <input
              className={styles.layerInput}
              placeholder=""
              type="text"
              value={layerName}
              onChange={setLayerName}
              placeholder="Layer name"
            />
            <BsPencil color="#989898" />
          </Col>
          <Col xs="auto" className="d-flex align-items-end">
            {imageSet.images.length > 0 && (
              <p className="mb-0">
                {imageSet.images.length} image{imageSet.images.length > 1 && 's'} selected
              </p>
            )}
          </Col>
        </Row>
      </div>

      <div className={`${styles.imageReelContainer} d-flex mb-3`}>
        <div {...getRootProps({ className: `${styles.dropzone} w-100 d-flex` })}>
          <input {...getInputProps()} />

          <Row className="w-100">
            {!isDragActive && !currentImages.length && (
              <Col className="d-flex justify-content-center align-items-center">
                <p>Drop images here (1mb max, .png only)</p>
              </Col>
            )}

            {imagePreviews.map((imageSrc, index) => (
              <Col
                xs="4"
                md="2"
                key={imageSrc + index}
                className="d-flex align-items-center justify-content-center mb-1 mt-1"
              >
                <OnImagesLoaded
                  onLoaded={() => {
                    // Prevent memory leaks by removing the local blob after image loaded
                    URL.revokeObjectURL(imageSrc);
                  }}
                >
                  <img className={`img-fluid ${styles.imageReelImage}`} src={imageSrc} />
                </OnImagesLoaded>
              </Col>
            ))}
          </Row>
        </div>
      </div>
    </div>
  );
}

export default ImageReel;
