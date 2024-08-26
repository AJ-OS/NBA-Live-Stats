// components/Layout.js
import React from 'react';
import Footer from './Footer';

const Layout = ({ children }) => {
  return (
    <div>
      {/* Your header or navigation */}
      {children}
      <Footer />
    </div>
  );
};

export default Layout;
