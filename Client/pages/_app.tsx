// pages/_app.jsx
import React from 'react';
import "@/styles/globals.css"; // Import global styles
import Footer from './Footer'; // Import your Footer component
import type { AppProps } from 'next/app';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <div>
      {/* Wrap your Component with the Layout component */}
      <Component {...pageProps} />
      {/* Add your Footer component */}
      <Footer />
    </div>
  );
}

export default MyApp;
