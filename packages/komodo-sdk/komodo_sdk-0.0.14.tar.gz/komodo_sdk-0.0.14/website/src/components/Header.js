'use client'
import React, { useContext } from 'react';
import Select from 'react-select';
import roleContext from "../contexts/roleContext"
import { useNavigate } from "react-router-dom";

const Header = () => {
    const navigate = useNavigate();
    const selectContext = useContext(roleContext)

    function handleChange(val) {
        const user = JSON.parse(localStorage.getItem('komodoUser'))
        localStorage.setItem("komodoUser", JSON.stringify({ ...user, select: val }))
        selectContext?.setReactSelect(val)
        selectContext?.setChatHistory(false)
        selectContext?.setList([])
        navigate("/chat")
    }

    const style = {
        control: base => ({
            ...base,
            cursor: 'pointer',
            border: "0",
            fontSize: "21px",
            fontFamily: "Cerebri Sans",
            boxShadow: "none",
            " &: hover": {
                border: "0",
            }
        }),
        option: (base, { isSelected }) => ({
            ...base,
            backgroundColor: isSelected ? "#316ff642" : "#ffffff",
            cursor: 'pointer',
            color: isSelected ? "#333" : "#000",
            " &:hover": {
                backgroundColor: "#316ff673"
            }
        }),
        placeholder: (defaultStyles) => {
            return {
                ...defaultStyles,
                fontSize: "5px"
            }
        }
    };
    return (
        <div className="flex justify-between border-b-[0.5px] border-[#CDCDCD] h-[93px] items-center px-5">
            <div className=''>
                {selectContext?.reactSelect?.purpose !== undefined ? <>
                    <div className='w-[230px]'>
                        <Select
                            className='font-cerebriregular'
                            value={selectContext?.reactSelect}
                            onChange={handleChange}
                            options={selectContext?.agentList?.agents}
                            styles={style}
                            getOptionLabel={(agent) => agent["name"]}
                            getOptionValue={(agent) => agent["email"]}
                        />
                    </div>
                    <p className='ms-1 mt-1 font-cerebriregular'>{selectContext?.reactSelect?.purpose || ""}</p>
                </> : null}
            </div>
            <div className='pr-1'>
                <div className="flex items-center justify-end space-x-2">
                    <h1 className='text-3xl font-cerebrisemibold'>KOMODO</h1>
                </div>
                <div className='text-[18px] mt-1 font-cerebriregular text-end'>
                    <p>{selectContext?.agentList?.name ? <span>{selectContext?.agentList?.name}</span> : <span className='opacity-0'>KOMODO</span>}</p>
                </div>
            </div>
        </div>
    );
};

export default Header;
