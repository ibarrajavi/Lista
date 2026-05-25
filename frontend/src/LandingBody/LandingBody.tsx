// import React from "react";

import { Link } from "react-router-dom";


function LandingBody() {
    return (
        <div className="bg-bg fixed w-full min-h-screen py-40 justify-self-center justify-items-center text-center">
            <ul>
                <li className="text-xs font-sans text-ink-faint"> 
                LISTS, KEPT SIMPLY
                </li>

                <li className="font-serif italic text-[60px] text-ink leading-tight">
                A quieter way <br/>
                to keep a list.
                </li>

                <li className="py-3 text-sm font-sans text-ink">
                    Lista is a calm, considered place for the things you mean <br/>
                    to do - groceries, trips, the books you've been meaning <br/>
                    to read. No clutter. No noise. <br/>
                </li>

                <li className="py-3">
                    <button className="font-sans text-[13px] font-normal bg-[#161514] text-[#FFFFFF] py-2 px-[14px] rounded-ctrl rounded-[8px] cursor-pointer">
                        Create your first Lista
                    </button>
                    
                    <Link
                        to="/login" 
                        className="mx-3 outline-solid outline-1 outline-hairline bg-elev font-sans text-[13px] font-normal text-[#161514] py-2 px-[14px] rounded-ctrl rounded-[8px] cursor-pointer">
                        Login
                    </Link>
                </li>
                </ul>
            
        </div>

    );
}

export default LandingBody;