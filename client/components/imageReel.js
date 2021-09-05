import { useState, useEffect } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import styles from '../styles/Layers.module.css';
import { useDropzone } from 'react-dropzone';
import OnImagesLoaded from 'react-on-images-loaded';

function ImageReel({ imageSet, setImageSet }) {
  const [imagePreviews, setImagePreviews] = useState([]);

  const { acceptedFiles, getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: '.png',
    maxSize: 1000000,
    noClick: imageSet.length > 0,
    onDrop: (acceptedFiles) => setImageSet([...imageSet, ...acceptedFiles])
  });

  useEffect(() => {
    setImagePreviews(
      imageSet.map((image) => {
        return URL.createObjectURL(image);
      })
    );
  }, [imageSet]);

  return (
    <div className={`${styles.imageReelContainer} d-flex`}>
      <div {...getRootProps({ className: `${styles.dropzone} w-100 d-flex` })}>
        <input {...getInputProps()} />

        <Row className="w-100">
          {!isDragActive && !imageSet.length && (
            <Col className="d-flex justify-content-center align-items-center">
              <p className={styles.dragAndDropMessage}>Drop images here (1MB Max, .PNG Only)</p>
            </Col>
          )}

          {imagePreviews.map((imageSrc, index) => (
            <Col
              xs="4"
              md="2"
              key={imageSrc + index}
              className="d-flex align-items-center justify-content-center mb-3"
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
  );
}

export default ImageReel;
