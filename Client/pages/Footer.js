import React from 'react';
import { FiGithub } from "react-icons/fi";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <a href='https://github.com/AJ-OS' target='_blank'><FiGithub className="footer-icon" /></a>
        <span>© 2024 AJ Morris. All rights reserved.</span>
      </div>
    </footer>
  );
};

export default Footer;
