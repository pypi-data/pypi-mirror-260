import React, { useContext, useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import { IoDocumentTextOutline } from 'react-icons/io5';
import dots from '../images/dots.png'
import Header from '../components/Header';
import roleContext from "../contexts/roleContext"
import { API_Path } from '../API/ApiComment';
import { ErrorToast, SuccessToast } from '../helpers/Toast';
import { ApiDelete } from '../API/API_data';

const PrimaryLayout = ({ children, onNewChatClick = () => { }, setNewChat = () => { } }) => {
    const user = JSON.parse(localStorage.getItem('komodoUser'))
    const listData = useContext(roleContext)
    const navigate = useNavigate()
    const modalRef = useRef(null);
    const [deleteChat, setDeleteChat] = useState(false);
    const [deleteChatId, setDeleteChatId] = useState(null);
    const pathname = window.location.hash;
    const match = pathname.match(/\/details\/([^/]+)/);
    const id = match ? match[1] : null;

    const handleDetails = (val) => {
        setNewChat(false);
        navigate(`/details/${val?.guid}`);
    }

    const handleDelete = (chatId, e) => {
        e.stopPropagation();
        setDeleteChat(true)
        setDeleteChatId(chatId);
    }

    const handleChatDelete = async (id, i, e) => {
        e.stopPropagation();
        try {
            const agent = await ApiDelete(`${API_Path.getDeleteConversation}${id}`, { agent_shortcode: listData?.reactSelect?.shortcode })
            if (agent?.status === 200) {
                let temp = [...listData.list]
                temp.splice(i, 1)
                listData?.setList(temp)
                onNewChatClick();
                navigate('/chat');
                SuccessToast("Deleted successfully")
            }
        } catch (error) {
            console.log('user details get ::error', error)
            ErrorToast(error?.data?.detail || "Something went wrong")
        }
    };

    const handleClickOutside = (e) => {
        if (modalRef.current && !modalRef.current.contains(e.target)) {
            setDeleteChat(false)
        }
    };

    useEffect(() => {
        document.addEventListener('mousedown', handleClickOutside);

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const formatDate = (date) => {
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(today.getDate() - 1);
        const valDate = new Date(date);
        if (valDate.toDateString() === today.toDateString()) {
            return "Today";
        } else if (valDate.toDateString() === yesterday.toDateString()) {
            return "Yesterday";
        } else {
            return "Previous";
        }
    };

    const renderChatItems = () => {
        let todayDisplayed = false;
        let yesterdayDisplayed = false;
        let previousDisplayed = false;
        return listData?.list?.map((val, i) => {
            const formattedDate = formatDate(val?.createdAt);

            if (formattedDate === "Today" && !todayDisplayed) {
                todayDisplayed = true;
                return (
                    <React.Fragment key={`today-${i}`}>
                        <div className={`px-5 border-b-[0.5px] border-[#F6F6F9] py-5 text-[#C5C5C5] text-[12px] font-cerebri leading-[15.24px] tracking-[2px] uppercase`}>
                            Today
                        </div>
                        {renderChatItem(val, i)}
                    </React.Fragment>
                );
            } else if (formattedDate === "Yesterday" && !yesterdayDisplayed) {
                yesterdayDisplayed = true;
                return (
                    <React.Fragment key={`yesterday-${i}`}>
                        <div className={`px-5 border-b-[0.5px] border-[#F6F6F9] py-5 text-[#C5C5C5] text-[12px] font-cerebri leading-[15.24px] tracking-[2px] uppercase`}>
                            Yesterday
                        </div>
                        {renderChatItem(val, i)}
                    </React.Fragment>
                );
            } else if (formattedDate === "Previous" && !previousDisplayed) {
                previousDisplayed = true;
                return (
                    <React.Fragment key={`previous-${i}`}>
                        <div className={`px-5 border-b-[0.5px] border-[#F6F6F9] py-5 text-[#C5C5C5] text-[12px] font-cerebri leading-[15.24px] tracking-[2px] uppercase`}>
                            Previous
                        </div>
                        {renderChatItem(val, i)}
                    </React.Fragment>
                );
            } else {
                return renderChatItem(val, i);
            }
        });
    };
    const renderChatItem = (val, i) => (
        <div key={val?.guid} onClick={() => handleDetails(val)} className={`px-5 border-b-[0.5px] border-[#F6F6F9] py-5 text-[#5A636C] text-[14px] leading-[17.78px] flex justify-between items-center font-cerebriregular cursor-pointer ${id === val?.guid ? 'bg-[#F6F6F9]' : ''}`}>
            <div className="flex items-center gap-3">
                <span className='bg-[#eee5dc] p-1 rounded-full'>
                    <IoDocumentTextOutline className='text-[#316FF6] text-[15px]' />
                </span>
                <div>
                    {val?.title}
                </div>
            </div>
            <div className='relative'>
                <img src={dots} alt="dots" className='min-w-[16px]' onClick={(e) => handleDelete(val?.guid, e)} />
                {deleteChat && deleteChatId === val?.guid && (
                    <div ref={modalRef} className="absolute bg-white border rounded-md shadow-md text-center right-0" onClick={(e) => handleChatDelete(val?.guid, i, e)}>
                        <button className='text-[#5A636C] text-[13px] font-cerebri leading-[30px] px-4 py-[2px] mt-1 cursor-pointer'>
                            Delete
                        </button>
                    </div>
                )}
            </div>
        </div>
    );

    return (
        <div className="flex">
            <div className="w-1/5 font-cerebri flex border-r-[0.5px] border-[#CDCDCD]">
                <Sidebar />
                <div className="font-cerebri w-[-webkit-fill-available] flex flex-col justify-between">
                    <div>
                        <h1 className='text-[21px] font-cerebri text-[#495057] leading-[27px] mb-9 mt-5 mx-5'>Chat</h1>
                        <div className="text-center">
                            <button onClick={() => {
                                onNewChatClick();
                                navigate('/chat');
                            }} className='bg-[#316FF6] text-[#fff] rounded-md px-24 pb-2 pt-3 text-[15px] font-cerebriregular xxl:px-10'> New Chat</button>
                        </div>
                        <div className='h-[calc(100vh-180px)] overflow-auto scrollbar'>
                            <div className='mt-8'>
                                <div className='border-t-[0.5px] border-[#F6F6F9]'>
                                    {renderChatItems()}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="mx-5 mb-3">
                        <h1 className="text-[18px] leading-[25.4px] font-cerebri text-[#495057]">{user?.name}</h1>
                    </div>
                </div>
            </div>
            <div className="w-4/5">
                <Header />
                {children}
            </div>
        </div>
    )
}

export default PrimaryLayout