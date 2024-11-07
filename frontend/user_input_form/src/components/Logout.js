import {useEffect, useState} from "react";
import axios from "axios";

export const Logout = () => {

    useEffect(() => {
        (async () => {
            try {
                // localhost:8000
                const {data} = await axios.post('http://106.14.184.241/logout/',{
                    refresh_token:localStorage.getItem('refresh_token')
                } ,{headers: {
                    'Content-Type': 'application/json'
                }}, {withCredentials: true});

                console.log('logout', data)
                localStorage.clear();
                axios.defaults.headers.common['Authorization'] = null;
                window.location.href = '/'
            } catch (e) {
                console.log('logout not working')
            }
        })();
    }, []);


        

        // console.log(data)
        // localStorage.clear();
        // localStorage.setItem('token', data.access);
        // localStorage.setItem('refresh_token', data.refresh);
        // axios.defaults.headers.common['Authorization'] = `Bearer ${data['access']}`;
        // window.location.href = '/'


    return (
        <div></div>
    )
}

export default Logout