import React from "react";

function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer>
      <p>Copyright ⓒ {year} MSiA Cloud Engineering Team 1</p>
    </footer>
  );
}

export default Footer;
