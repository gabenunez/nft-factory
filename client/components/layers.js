import { useState, useEffect } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import styles from '../styles/Layers.module.css';
import { useDropzone } from 'react-dropzone';
import OnImagesLoaded from 'react-on-images-loaded';
import ImageReel from '../components/imageReel';
import image from 'next/image';

function Layers({ selectedImages, setSelectedImages }) {
  return (
    <div className="mb-3 mt-3">
      {selectedImages.map((imageSet, index) => {
        return (
          <div key={index}>
            <h4>
              Layer {index + 1} {imageSet.length > 0 && <>({imageSet.length} Images)</>}
            </h4>
            <ImageReel
              imageSet={imageSet}
              setImageSet={(images) => {
                const selectedImageCopy = [...selectedImages];
                selectedImageCopy[index] = images;
                setSelectedImages(selectedImageCopy);
              }}
            />
          </div>
        );
      })}
    </div>
  );
}

export default Layers;
