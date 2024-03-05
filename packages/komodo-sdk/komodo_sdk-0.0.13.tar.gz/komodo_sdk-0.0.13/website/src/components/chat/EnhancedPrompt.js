import React, { useState, useEffect, useContext } from 'react';
import roleContext from "../../contexts/roleContext"
import { API_Path } from '../../API/ApiComment';

const EnhancedPrompt = ({ prompt }) => {
    const user = JSON.parse(localStorage.getItem('komodoUser'))
    const chatContext = useContext(roleContext);
    const [fullMessage, setFullMessage] = useState('');



    useEffect(() => {
        if (prompt !== "") {
            setFullMessage("")
            const eventSource = new EventSource(`${API_Path.streamedApi}email=${user?.email}&agent_shortcode=${chatContext?.reactSelect?.shortcode}&prompt=${prompt}`);

            eventSource.onmessage = (event) => {
                const newMessage = (event.data);
                // setFullMessage((prvMsg) => prvMsg + newMessage)
                setFullMessage((prvMsg) => prvMsg + ' ' + newMessage);
            };

            eventSource.addEventListener('stream-complete', function (e) {
                eventSource.close();
                chatContext?.conversations()
            });

            eventSource.onopen = (event) => {
                console.log('Connection to server opened.');
            };

            eventSource.onclose = function () {
                console.log('Connection closed by the server.');
            };

            eventSource.onerror = (event) => {
                if (eventSource.readyState === EventSource.CLOSED) {
                    console.error('Connection was closed.');
                } else {
                    console.error('An error occurred:', event);
                }
                eventSource.close();
            };
            return () => {
                eventSource.close();
            };
        }
    }, [prompt]);

    return (
        <>
            <div className='w-fit text-[#495057]'>
                <p
                    className='font-cerebriregular text-[15px] leading-[34px] cursor-pointer'
                    dangerouslySetInnerHTML={{ __html: fullMessage.replace(/\n/g, '<br>') }}
                ></p>
            </div>
        </>
    );
};

export default EnhancedPrompt;