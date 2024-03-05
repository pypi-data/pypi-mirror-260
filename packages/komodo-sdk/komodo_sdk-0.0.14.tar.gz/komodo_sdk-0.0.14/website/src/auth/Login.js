import React, { useContext, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom';
import * as Yup from 'yup';
import { useFormik } from 'formik';
import Sidebar from '../components/Sidebar';
import { ApiGet } from '../API/API_data';
import { ErrorToast, SuccessToast } from '../helpers/Toast';
import { API_Path } from '../API/ApiComment';
import roleContext from '../contexts/roleContext';

const Login = () => {
    const navigate = useNavigate()
    const location = useLocation()
    const context = useContext(roleContext)
    const validationSchema = Yup.object().shape({
        email: Yup.string().email('Invalid email').required('Email is required'),
        password: Yup.string().required('Password is required'),
    });

    useEffect(() => {
        if (location.pathname === '/') {
            const token = JSON.parse(localStorage.getItem('komodoUser'))
            ![null, undefined, ''].includes(token?.email) && navigate('/chat')
        }
    }, [])

    const formik = useFormik({
        initialValues: {
            email: '',
            password: '',
        },
        validationSchema: validationSchema,
        onSubmit: async (values) => {
            try {
                const checkLogin = await ApiGet(API_Path.login, values.email)
                if (checkLogin?.status === 200) {
                    localStorage.setItem("komodoUser", JSON.stringify(checkLogin.data))
                    context?.setUser(checkLogin.data.email)
                    SuccessToast("Login successful")
                    navigate('/chat');
                }
            } catch (error) {
                console.log('user details get ::error', error)
                ErrorToast(error?.data?.detail || "Something went wrong")
            }
        },
    });

    return (
        <>
            <div className="grid grid-rows-1">
                <div className="grid grid-cols-12">
                    <div className='col-span-1'>
                        <Sidebar />
                    </div>
                    <div className='col-span-11'>
                        <form onSubmit={formik.handleSubmit} className='flex flex-col justify-center items-center h-[calc(100vh-57px)]'>
                            <div>
                                <h1 className='text-[#495057] text-[23px] font-cerebri leading-[30px]'>Email</h1>
                                <input
                                    type="text"
                                    placeholder='Enter Email'
                                    name="email"
                                    value={formik.values.email}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    className='text-[#495057] text-[16px] font-cerebriregular leading-[20.32px] border border-[#CFD4D8] rounded-md w-[513px] h-[50px] px-3 outline-none mt-1'
                                />
                                {formik.touched.email && formik.errors.email && <p className="text-red-500 mt-2">{formik.errors.email}</p>}
                            </div>
                            <div className='mt-5'>
                                <h1 className='text-[#495057] text-[23px] font-cerebri leading-[30px]'>Password</h1>
                                <input
                                    type="password"
                                    placeholder='Enter Password'
                                    name="password"
                                    value={formik.values.password}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    className='text-[#495057] text-[16px] font-cerebriregular leading-[20.32px] border border-[#CFD4D8] rounded-md w-[513px] h-[50px] px-3  outline-none mt-1'
                                />
                                {formik.touched.password && formik.errors.password && <p className="text-red-500 mt-2">{formik.errors.password}</p>}
                            </div>
                            <button type='submit' className='text-[#fff] text-[19px] font-cerebri leading-[24.13px] text-center bg-[#316FF6] w-[513px] h-[52px]  rounded-md mt-10'>Log In</button>
                        </form>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Login