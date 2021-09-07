import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';

function Header() {
  return (
    <Navbar className="mb-3" bg="light">
      <Container>
        <Navbar.Brand href="#home">NFT Factory</Navbar.Brand>
      </Container>
    </Navbar>
  );
}

export default Header;
