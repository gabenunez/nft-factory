import Header from '../components/header';

function DefaultLayout({ children }) {
  return (
    <>
      <Header />
      <main>{children}</main>
    </>
  );
}

export default DefaultLayout;
