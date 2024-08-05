import React, { useState, useEffect } from "react";
// import "../style/fadeIn.css";

interface FadeInProps {
  children: React.ReactNode;
  duration?: number;
}

export default function FadeIn({ children, duration = 500 }: FadeInProps) {
  return children;
  // const [visible, setVisible] = useState(false);

  // useEffect(() => {
  //   const timer = setTimeout(() => {
  //     setVisible(true);
  //   }, 100);
  //   return () => clearTimeout(timer);
  // }, []);

  // return (
  //   <div
  //     className={`fade-in ${visible ? "visible" : ""}`}
  //     style={{ transitionDuration: `${duration}ms` }}
  //   >
  //     {children}
  //   </div>
  // );
}
