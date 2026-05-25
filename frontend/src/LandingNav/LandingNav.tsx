//import { useState } from 'react'
//import reactLogo from '../assets/react.svg'
//import viteLogo from '../assets/vite.svg'
// import React from "react";
import { Link } from 'react-router-dom'

function LandingNav() {
  return (
    <nav className="bg-bg fixed w-full z-20 top-0 start-0 border-1 border-hairline border-default">
      <div className="flex flex-wrap items-center justify-between mx-8 py-4">

        {/* logo */}
        <Link
          to="/"
          className="flex items-center space-x-3 rtl:space-x-reverse"
        >
          <span className="self-center font-serif italic font-normal text-lg ">
            Lista
          </span>
        </Link>

        <div className="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">

        {/* login */}
        <Link
          to="/login"
          className="font-sans text-[13px] font-normal text-[#161514] py-2 px-[14px] rounded-ctrl rounded-[8px] cursor-pointer">
          Login
        </Link>

        {/* get started */}
        <button 
        type="button" className="font-sans text-[13px] font-normal bg-[#161514] text-[#FFFFFF] py-2 px-[14px] rounded-ctrl rounded-[8px] cursor-pointer">
            Get Started
        </button>
        </div>
      </div>
    </nav>
  );
}

export default LandingNav;
