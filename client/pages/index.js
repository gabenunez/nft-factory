import { useState } from 'react';
import axios from 'axios';
import Head from 'next/head';
import Image from 'next/image';
import styles from '../styles/Home.module.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Layers from '../components/layers';
import Button from 'react-bootstrap/Button';
import { BsQuestionOctagon } from 'react-icons/bs';
import FileToBase64 from 'dd-file-to-base64';
import { saveAs } from 'file-saver';

export default function Home() {
  const [selectedImages, setSelectedImages] = useState([{ name: '', images: [] }]);
  const [previewImage, setPreviewImage] = useState('');

  async function createImagePayload() {
    const requestPayload = {};

    const reversedLayers = [...selectedImages].reverse();
    for (const layer of reversedLayers) {
      let base64images = layer.images.map((image) => {
        return FileToBase64.convert(image);
      });

      try {
        base64images = await Promise.all(base64images);
      } catch (error) {
        alert('Wow. This is weird. We had a problem converting your images. Please try again.');
        throw new Error(error);
      }

      requestPayload[layer.name] = layer.images.map((image, imageIndex) => {
        return {
          name: image.attributeName,
          image: base64images[imageIndex].split('base64,')[1],
          chance: image.percentageChance
        };
      });

      return requestPayload;
    }
  }

  async function generateImageCollection() {
    try {
      const requestPayload = await createImagePayload();
      const response = await axios.post('/api/create_collectible?n=27', requestPayload, {
        responseType: 'arraybuffer'
      });

      const zipBlob = new Blob([response.data]);
      saveAs(zipBlob, 'collection.zip');
    } catch (err) {
      alert(
        "Sorry, we're having problems connecting to our internal server. Please try again later."
      );
      console.error(err);
    }
  }

  async function fetchExampleImage() {
    try {
      const requestPayload = await createImagePayload();
      const response = await axios.post('/api/preview', requestPayload);

      setPreviewImage(response.data.image);
    } catch (err) {
      alert(
        "Sorry, we're having problems connecting to our internal server. Please try again later."
      );
      console.error(err);
    }
  }

  return (
    <div>
      <Head>
        <title>NFT Factory - Generate a full collection of NFTs!</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <Container>
          <Row>
            <Col md={3}>
              <div className="d-flex justify-content-center mb-3">
                {previewImage && (
                  <img className="d-block img-fluid " alt="Preview image" src={previewImage} />
                )}

                {!previewImage && <BsQuestionOctagon color="#0d6efd" size="100px" />}
              </div>

              <div className="d-flex justify-content-center mb-3">
                <Button onClick={fetchExampleImage}>Generate example image</Button>
              </div>

              <div className="d-flex justify-content-center">
                <Button onClick={generateImageCollection}>Generate image collection</Button>
              </div>
            </Col>
            <Col md={9}>
              <Button
                onClick={() => setSelectedImages([{ name: '', images: [] }, ...selectedImages])}
              >
                + New Layer
              </Button>
              <Layers selectedImages={selectedImages} setSelectedImages={setSelectedImages} />
            </Col>
          </Row>
        </Container>
      </main>
    </div>
  );
}
