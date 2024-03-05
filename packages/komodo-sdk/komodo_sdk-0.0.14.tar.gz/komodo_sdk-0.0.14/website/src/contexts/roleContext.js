import { createContext, useEffect, useState } from 'react';
import { ApiGet, ApiPost } from '../API/API_data';
import { API_Path } from '../API/ApiComment';
import { ErrorToast } from "../helpers/Toast"

const Context = createContext("");

export function RoleStore(props) {
    const [reactSelect, setReactSelect] = useState();
    const [user, setUser] = useState("");
    const [agentList, setAgentList] = useState();
    const [list, setList] = useState([]);
    const [chatHistory, setChatHistory] = useState(false);

    useEffect(() => {
        if (user === "") {
            set_user_login_data()
        }
        if (user !== "") {
            agentDetails()
        }
    }, [user])


    useEffect(() => {
        if (user !== "") {
            conversations()
        }
    }, [reactSelect?.shortcode])

    const set_user_login_data = () => {
        const userDetails = JSON.parse(localStorage.getItem('komodoUser'))
        setUser(userDetails?.email || "")
    }

    const agentDetails = async () => {
        const user = JSON.parse(localStorage.getItem('komodoUser'))
        try {
            const agent = await ApiGet(API_Path.agentDetails)
            if (agent?.status === 200) {
                setAgentList(agent?.data)
                localStorage.setItem("komodoUser", JSON.stringify({ ...user, select: user.select || agent?.data?.agents[0] }))
                setReactSelect(user.select || agent?.data?.agents[0])
            }
        } catch (error) {
            console.log('user details get ::error', error)
            ErrorToast(error?.data?.detail || "Something went wrong")
        }
    }

    const conversations = async () => {
        try {
            const agent = await ApiPost(API_Path.getDeleteConversation, { agent_shortcode: reactSelect?.shortcode })
            if (agent?.status === 200) {
                let sortedArray = agent?.data.sort((item1, item2) => {
                    return new Date(item2.createdAt) - new Date(item1.createdAt);
                });

                setList(sortedArray)
            }
        } catch (error) {
            console.log('user details get ::error', error)
            setList([])
            ErrorToast(error?.data?.detail || "Something went wrong")
        }
    }
    return (
        <Context.Provider
            value={{
                reactSelect,
                agentList,
                list,
                chatHistory,
                ...{
                    setReactSelect,
                    setUser,
                    setList,
                    setChatHistory,
                    conversations,
                },
            }}
        >
            {props.children}
        </Context.Provider>
    )
}

export default Context;